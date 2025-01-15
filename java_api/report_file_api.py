import requests
import json
from datetime import datetime
import sys

if __name__ == '__main__':

    # 获取今天的日期
    today = datetime.today()
    # 格式化日期为 yyyy-MM-dd 格式
    formatted_date = today.strftime("%Y-%m-%d")
    # 打印格式化后的日期
    print("今天的日期:", formatted_date)

    # 检查是否提供了足够的参数
    if len(sys.argv) < 2:
        print("没有传入参数，格式：python script.py [arg1]")
    else:
        # 获取第一个命令行参数
        formatted_date = sys.argv[1]

        # 打印第一个参数
        print("手动传入参数:", formatted_date)


    # 获取token
    url = "http://cloud-app-10-5-1-236:8080/api/xiang-auth/oauth/token?tenant_id=000000&username=admin&password=21232f297a57a5a743894a0e4a801fc3&grant_type=password&scope=all"

    payload = {}
    headers = {
      'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.text
    data = json.loads(token)
    acc_token = data.get('access_token',None)


    # 恒盈保单打印 获取 PDF 路径
    buss_url = "http://cloud-app-10-5-1-236:8080/api/xiang-deliver-report/report-file/get-sftp-catalogue?flag=true&time="+formatted_date

    buss_payload = {}
    buss_headers = {
        'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0',
        'Xiang-Auth': 'bearer ' + acc_token
    }
    buss_response = requests.request("GET", buss_url, headers=buss_headers, data=buss_payload)

    print("返回参数：", buss_response.text)
