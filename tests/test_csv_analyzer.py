from tools import analyze_csv

def test_analyze_csv_valid(tmp_path):
    # 1. 使用 tmp_path 构造 students.csv 文件路径
    file_path = tmp_path / "students.csv"
    # 2. 使用 write_text() 写入包含表头和两行数据的 CSV
    file_path.write_text(
        "name,age,gpa\nAlice,22,3.8\nBob,23,3.9\n",
        encoding="utf-8"
    )
    # 3. 调用 analyze_csv()
    result = analyze_csv(file_path)
    # 4. assert 返回的字典是否符合预期
    assert result == {
        "row_count" : 2,
        "column_count" : 3,
        "columns" : ['name', 'age', 'gpa']
    }