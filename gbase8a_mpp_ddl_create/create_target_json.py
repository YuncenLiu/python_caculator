import pandas as pd
import os
import json
import shutil

data_dict = {
    "VARCHAR2": "String",
    "DATE": "Date",
    "NUMBER": "double",
    "CHAR": "String",
    "TIMESTAMP(6)": "Date",
    "FLOAT": "double",
    "CLOB": "String",
    "LONG": "long",
}

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
    if os.path.exists(output_dir):
        # 如果存在，则删除该目录
        shutil.rmtree(output_dir)
        print(f"目录 {output_dir} 已删除")
    else:
        print(f"目录 {output_dir} 不存在")


def generate_json_and_save_to_file(df, input_json_path, output_dir):
    # 删除目录下所有现有的文件
    delete_existing_files(output_dir)

    # 按表名分组
    grouped = df.groupby('表名')

    # 读取原始 JSON 文件
    with open(input_json_path, 'r', encoding='utf-8') as input_file:
        data = json.load(input_file)

    for table_name, group in grouped:

        # 获取该表的所有字段
        fields = group['字段'].tolist()
        schame = group['目标库'].tolist()[0]
        new_table_name = group['目标表'].tolist()[0]

        # path = "/Users/xiang/xiang/compile/datax/target/gbase_source/" + schame + "/" + new_table_name
        # path = "/data/datax/datax/source/gbase_source/" + schame + "/" + new_table_name
        path = "/datasync/source/gbase_source/" + schame + "/" + new_table_name

        other_fields = group.drop(columns=['备注'])  # 排除 '字段' 列
        other_fields_info = other_fields.to_dict(orient='records')  # 转为字典格式，每行是一个字典


        columes = []
        for col in other_fields_info:
            if col["表名"] == table_name:
                if not pd.isna(col["顺序"]):
                    column_index = col["顺序"]
                    column_name = col["字段"]
                    column_type = col["类型"]
                    col_type = data_dict[column_type]

                    colume = {
                        "index": 0,
                        "name": "",
                        "type": "string"
                    }

                    if col_type == "Date":
                        colume = {
                            "index": 0,
                            "name": "",
                            "type": "Date",
                            "dateFormat": "yyyy-MM-dd HH:mm:ss"
                        }

                    colume["index"] = column_index - 1
                    colume["name"] = column_name
                    colume["type"] = col_type

                    columes.append(colume)


        reader = {
            "name": "txtfilereader",
            "parameter": {
                "path": path,
                "fieldDelimiter": "\u0001",
                "recordDelimiter": "\u001f",
                "encoding": "UTF-8",
                "nullFormat": "",
                "column": columes,  # 将字段列表加入column
            }
        }

        preSql = f"truncate table {schame}.{new_table_name}"

        schema_table_name = schame + "." + new_table_name

        writer = {
            "name": "rdbmswriter",
            "parameter": {
                "batchSize": 5000,
                "memstoreThreshold": "90",
                "username": "ods",
                "password": "M23sjx7w$@Eq@JY7",
                "column": fields,  # 将字段列表加入column
                "preSql": [preSql],
                "connection": [
                    {
                        "table": [schema_table_name],
                        "jdbcUrl": "jdbc:gbase://10.4.43.53:5258/ts?failoverEnable=true&hostList=10.4.43.57,10.4.43.61&gclusterId=gc1"
                    }
                ]
            }
        }

        # 修改 reader
        data["job"]["content"][0]["reader"] = reader

        # 修改 writer.parameter.fileName
        data["job"]["content"][0]["writer"] = writer

        table_folder = os.path.join(output_dir, schame)
        if not os.path.exists(table_folder):
            os.makedirs(table_folder)
        # 创建配置文件的路径
        output_file = os.path.join(table_folder, f"{new_table_name}.json")

        # # 将配置写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Generated config for table {schame}.{new_table_name} and saved to {output_file}")


# 主函数，执行读取和生成 DDL 语句并保存为文件
def main():
    # 指定 Excel 文件路径
    file_path = '/Users/xiang/Documents/work/company/昆仑/SVN/OM/3.0 日常需求工作/EAST2.0/贴源层数据表同步.xlsx'

    input_json_path = '/Users/xiang/xiang/study/Python/tools/caculator/gbase8a_mpp_ddl_create/FileToGbase.json'
    # 输出目录路径
    output_dir = '/Users/xiang/xiang/study/Python/tools/caculator/target/gbase8a_target_json'
    # 读取 Excel 文件
    df = read_excel(file_path)

    # 生成 DDL 语句并保存到文件
    generate_json_and_save_to_file(df, input_json_path, output_dir)


if __name__ == "__main__":
    main()
