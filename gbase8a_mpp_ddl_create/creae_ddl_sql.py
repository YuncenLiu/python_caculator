import pandas as pd
import os
import shutil

# 读取 Excel 文件
def read_excel(file_path):
    # 使用 pandas 读取 Excel 文件，读取所有工作表
    excel_data = pd.ExcelFile(file_path)

    # 获取第三个工作表的名称
    sheet_name = excel_data.sheet_names[2]  # sheet_names 是按顺序列出所有工作表的列表

    # 读取第三个工作表的数据
    df = pd.read_excel(excel_data, sheet_name=sheet_name)
    return df

# 删除目标目录下的所有文件
def delete_existing_files(output_dir):
    shutil.rmtree(output_dir)


def process_string(input_str):
    # 按 \n 截取字符串，获取第一行
    first_line = input_str.split('\n')[0]

    # 按空格分割第一行
    parts = first_line.split()

    for part in parts:
        # 如果部分包含 "."，按 "." 分割并获取第一个部分
        if '.' in part:
            first_part = part.split('.')[0]
            return first_part

# 根据 DataFrame 数据生成 DDL 语句
def generate_ddl_and_save_to_file(df, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 删除目录下所有现有的文件
    delete_existing_files(output_dir)


    # 用于保存生成的 DDL 语句
    ddl_statements = {}

    # 遍历数据框中的每一行，根据表名生成 DDL
    for _, row in df.iterrows():
        sch = row['目标库']
        table_name = row['目标表']
        field_name = row['字段']
        length = row['长度']
        length = f"({length})"

        # 判断类型并修改
        data_type = row['类型']
        if data_type.upper() == 'VARCHAR2':
            data_type = 'VARCHAR'
        elif data_type.upper() == 'NUMBER':
            data_type = 'DECIMAL'
        elif data_type.upper() == 'LONG':
            data_type = 'BIGINT'
        elif data_type.upper() == 'TIMESTAMP(6)':
            data_type = 'DATETIME'
            length = ""
        elif data_type.upper() == 'DATE':
            data_type = 'DATETIME'
            length = ""



        # is_nullable = 'NOT NULL' if row['为空约束'] == 'N' else 'DEFAULT NULL'
        # primary_key = 'PRIMARY KEY' if 'P' in str(row['主键约束']) else ''
        comment = f"COMMENT '{row.get('备注', '')}'" if pd.notna(row.get('备注', '')) else ''

        # 创建 DDL 语句
        if table_name not in ddl_statements:
            ddl_statements[table_name] = f"DROP TABLE IF EXISTS {sch}.{table_name};\nCREATE TABLE {sch}.{table_name} (\n"

        # ddl_statements[table_name] += f"    {field_name} {data_type}({length}) {is_nullable} {comment},\n"

        ddl_statements[table_name] += f"    {field_name} {data_type}{length} {comment},\n"

    # 将每个表的 DDL 语句整理成一个列表并输出
    for table_name, ddl in ddl_statements.items():
        # 格式化为正确的 DDL 语句
        ddl = ddl.strip(',\n') + "\n);"

        schame = process_string(ddl)

        # 打印 DDL 语句到控制台
        print(f"\nDDL for table  {schame}.{table_name}:\n")
        print(ddl)

        table_folder = os.path.join(output_dir, schame)
        if not os.path.exists(table_folder):
            os.makedirs(table_folder)



        # 创建文件路径
        file_path = os.path.join(table_folder, f"{table_name}.sql")

        # 写入 SQL 文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ddl)

        print(f"\nDDL for table {schame}.{table_name} saved to {file_path}")



# 主函数，执行读取和生成 DDL 语句并保存为文件
def main():
    # 指定 Excel 文件路径
    file_path = '/Users/xiang/Documents/work/company/昆仑/SVN/OM/3.0 日常需求工作/EAST2.0/贴源层数据表同步.xlsx'

    # 输出目录路径
    output_dir = '/Users/xiang/xiang/study/Python/tools/caculator/target/gbase8a_ddl'
    # 读取 Excel 文件
    df = read_excel(file_path)

    # 生成 DDL 语句并保存到文件
    generate_ddl_and_save_to_file(df, output_dir)


if __name__ == "__main__":
    main()