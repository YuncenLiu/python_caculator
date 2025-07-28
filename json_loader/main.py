# Author:yun
# -*- coding: utf-8 -*-  
# @Time     : 2025/7/25 17:51
# @Author   : xiang
# @Site     : 
# @File     : main.py.py
# @Software : PyCharm
import csv
import json
from collections import OrderedDict


def convert_csv_to_json(csv_path):
    # 存储最终结果
    result = []

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 读取首行作为字段名
        headers = next(reader)

        # 处理数据行
        for row in reader:
            # 创建有序字典以保持字段顺序
            content = OrderedDict()
            for i, value in enumerate(row):
                # 处理值长度限制（根据实际需求调整）
                processed_value = value if len(value) < 100 else value[:97] + "..."
                content[headers[i]] = processed_value

            # 构造条目
            entry = {
                "CONTENT": dict(content),  # 转为普通字典
                "NAME": "XIBAO3"  # 固定值
            }
            result.append(entry)

    return json.dumps(result, ensure_ascii=False, indent=2)


# 文件路径
csv_path = "/Users/xiang/Desktop/Result_6.csv"

# 执行转换
try:
    json_output = convert_csv_to_json(csv_path)
    print(json_output)
except FileNotFoundError:
    print(f"错误：文件未找到 - {csv_path}")
except Exception as e:
    print(f"处理文件时出错: {str(e)}")