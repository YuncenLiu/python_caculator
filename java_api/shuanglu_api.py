import requests
import json
from datetime import datetime

if __name__ == '__main__':
    # 获取今天的日期
    today = datetime.today()
    # 格式化日期为 yyyy-MM-dd 格式
    formatted_date = today.strftime("%Y年%m月%d日 %H时%M分%S秒")
    # 打印格式化后的日期
    print("今天的日期:", formatted_date)

    # 获取token
    url = "http://10.5.3.176:8082/api/xiang-auth/oauth/token?tenant_id=000000&username=admin&password=21232f297a57a5a743894a0e4a801fc3&grant_type=password&scope=all"

    payload = {}
    headers = {
        'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.text
    data = json.loads(token)
    acc_token = data.get('access_token', None)

    buss_url = "http://10.5.3.176:8082/api/xiang-shuanglu-report-interface/transaction/sync-all-api"

    buss_payload = {}
    buss_headers = {
        'Authorization': 'Basic c2FiZXI6c2FiZXJfc2VjcmV0',
        'Xiang-Auth': 'bearer ' + acc_token
    }

    buss_response = requests.request("POST", buss_url, headers=buss_headers, data=buss_payload)
    print("返回参数：", buss_response.text)
    response_data = json.loads(buss_response.text)

    # 提取 code 值并判断
    code_value = response_data.get('code')
    msg_value = response_data.get('msg')
    if code_value != 200 or msg_value.lower() != "ok":
        raise Exception(f"Error: Response code is {code_value} and message is not 'OK'")

