# Author:yun
# -*- coding: utf-8 -*-  
# @Time     : 2025/6/23 14:25
# @Author   : xiang
# @Site     : 
# @File     : 01_yanglaoToBank.py
# @Software : PyCharm
def calculate_investments():
    # 投资参数设置
    initial_capital = 88000.0  # 初始本金
    pension_monthly_income = 827.09  # 养老金月收益
    annual_interest_rate = 0.025  # 年利率
    years = 30  # 投资年限
    total_months = years * 12  # 总月份数

    # 创建数据列表
    data = []

    # 初始化银行投资变量
    bank_principal = initial_capital  # 银行本金
    term_years = 3  # 定期年限
    term_months = term_years * 12  # 定期月份数
    term_interest_factor = (1 + annual_interest_rate * term_years)  # 定期利息因子

    # 初始化养老金账户
    pension_balance = 0.0

    # 按月计算
    for month in range(total_months + 1):  # 包括第0个月
        # 方案1: 个人养老金
        pension_balance = month * pension_monthly_income

        # 方案2: 银行定期存款
        if month % term_months == 0 and month > 0:
            # 定期到期，计算复利并自动转存
            bank_principal *= term_interest_factor
            bank_balance = bank_principal
        else:
            # 定期存期内，余额不变
            bank_balance = bank_principal

        # 添加到数据列表
        data.append({
            "month": month,
            "pension": pension_balance,
            "bank": bank_balance
        })

    return data


def save_to_csv(data, filename):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['month', 'pension', 'bank']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"数据已保存至 {filename}")


# 计算并保存结果
data = calculate_investments()
save_to_csv(data, 'investment_comparison_30y.csv')

# 输出最后一年摘要
years = 30
print(f"\n投资方案30年末最终结果 (单位:元):")
print(f"方案1 个人养老金: {data[-1]['pension']:.2f}")
print(f"方案2 银行定存   : {data[-1]['bank']:.2f}")