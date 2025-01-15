# coding:utf8
import csv
import numpy as np
import numpy_financial as npf

if __name__ == '__main__':
    # 用于读取CSV文件的文件路径

    # list_ = [-1000.0, -1000.0, -1000.0, 0.0, 0.0, 0.0, 0.0, 3371.59]
    # array_ = npf.irr(list_)
    # print(array_)

    # file_path = '/Users/xiang/Documents/work/company/昆仑/IRR利益/irr.txt'
    file_path = '/Users/xiang/Desktop/irr.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            cash_flow = [float(value) for value in line.strip('[]\n').split(', ')]
            irr = npf.irr(cash_flow)
            # IRR for cash flow [-1000.0, 136.2]: -86.3800%
            # print(f"IRR for cash flow {cash_flow}: {irr:.4%}")

            # -86.3800%
            # print(f"{irr:.4%}")

            # [-1000.0, 136.2]
            # print(f"{cash_flow}")