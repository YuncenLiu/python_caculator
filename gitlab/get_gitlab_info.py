# Author:yun
# -*- coding: utf-8 -*-  
# @Time     : 2025/7/4 09:12
# @Author   : xiang
# @Site     : 
# @File     : get_gitlab_info.py
# @Software : PyCharm

# http://10.5.1.160:9980/cv/cv
# root
# admin123.


import requests
import csv

# GitLab 地址和 API token
GITLAB_URL = "http://10.5.1.160:9980"
PRIVATE_TOKEN = "EXBF7wuEv8XkxzRDWL5G"  # 替换为你的 GitLab 私人令牌

# 获取所有项目（仓库）信息
def get_all_projects():
    projects = []
    page = 1
    per_page = 100  # 每页项目数

    while True:
        url = f"{GITLAB_URL}/api/v4/projects"
        params = {
            "private_token": PRIVATE_TOKEN,
            "page": page,
            "per_page": per_page
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Failed to fetch projects:", response.json())
            break

        project_list = response.json()
        if not project_list:
            break

        projects.extend(project_list)
        page += 1

    return projects

# 打印项目信息
def print_projects(projects):
    # 定义CSV文件路径
    csv_file = "gitlab_projects.csv"

    # 定义表头字段
    fieldnames = [
        'id', 'name', 'path_with_namespace', 'created_at', 'last_activity_at',
        'namespace_id', 'namespace_name', 'namespace_path', 'default_branch', 'description'
    ]

    # 写入CSV文件
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for project in projects:
            row = {
                'id': project['id'],
                'name': project['name'],
                'path_with_namespace': project['path_with_namespace'],
                'created_at': project['created_at'],
                'last_activity_at': project['last_activity_at'],
                'namespace_id': project['namespace']['id'],
                'namespace_name': project['namespace']['name'],
                'namespace_path': project['namespace']['path'],
                'default_branch': project['default_branch'],
                'description': project['description']
            }
            writer.writerow(row)

    print(f"项目信息已成功导出到 {csv_file}")




if __name__ == "__main__":
    projects = get_all_projects()
    print_projects(projects)