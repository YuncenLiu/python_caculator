# Author:yun
# -*- coding: utf-8 -*-  
# @Time     : 2025/7/15 09:40
# @Author   : xiang
# @Site     : 
# @File     : generate_files.py.py
# @Software : PyCharm

import mysql.connector
import datetime
import os
import csv
import time



def generate_files():
    # 数据库连接配置（按需修改）
    config = {
        'user': 'root',
        'password': 'root',
        'host': '10.10.91.158',
        'database': 'api_json',
        'raise_on_warnings': True
    }

    # 获取当前日期
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 文件名参数 (按需修改)
    org_code = "000001"
    system_code = "GZYQ2CDPP"
    table_code = "KHZSXJYB"
    filename_txt = f"{org_code}-{system_code}-{table_code}-{current_date}.txt"
    filename_log = filename_txt.replace('.txt', '.log')
    zip_filename = filename_txt.replace('.txt', '.zip')

    try:
        # 连接数据库并读取数据
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM KHZSXJYB")

        # 生成数据文件
        file_path = filename_txt
        row_count = 0

        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f, delimiter='\x01', quoting=csv.QUOTE_NONE, escapechar='\\')

            for row in cursor:
                # 转换None为空字符串
                cleaned_row = [str(item) if item is not None else '' for item in row]
                writer.writerow(cleaned_row)
                row_count += 1

        # 获取文件大小
        file_size = os.path.getsize(file_path)

        # 生成日志文件
        with open(filename_log, 'w', encoding='utf-8') as log_file:
            log_content = [
                file_path,
                str(file_size),
                current_time,
                'Y',
                str(row_count)
            ]
            log_file.write('\n'.join(log_content))

        print(f"数据文件 {file_path} 生成成功，包含 {row_count} 条记录")
        print(f"日志文件 {filename_log} 生成成功")

        # 压缩文件 (Windows需手动安装zip工具)
        os.system(f'zip -q {zip_filename} {file_path} {filename_log}')
        print(f"压缩文件 {zip_filename} 生成成功")

    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        if os.path.exists(file_path):
            os.remove(file_path)
        # 创建异常日志
        with open(filename_log, 'w', encoding='utf-8') as log_file:
            log_content = [
                file_path,
                "0",
                current_time,
                'N',
                "0"
            ]
            log_file.write('\n'.join(log_content))
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    generate_files()