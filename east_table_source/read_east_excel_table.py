import pandas as pd

def process_excel_sheets(excel_file_path):
    """
    读取Excel文件的所有Sheet页名称，检查第二行第一列是否为"数据项名称"，
    如果是则检查第四列"是否主键"，如果值为"Y"，则打印该行的第四列
    
    Args:
        excel_file_path: Excel文件的路径
        
    Returns:
        None，直接打印处理结果
    """
    try:
        # 使用pandas读取Excel文件
        excel_file = pd.ExcelFile(excel_file_path)
        
        # 获取所有Sheet页名称
        sheet_names = excel_file.sheet_names
        
        # 打印Sheet页名称和处理结果
        print("Excel文件中的Sheet页：")
        for i, name in enumerate(sheet_names, 1):
            print(f"{i}. {name}")
            
            try:
                # 读取第二行（索引从0开始，所以第二行是索引1）
                second_row = pd.read_excel(excel_file_path, sheet_name=name, skiprows=1, nrows=1)
                
                # 检查第二行第一列是否为"数据项名称"
                if len(second_row.columns) > 0 and second_row.iloc[0, 0] == "数据项名称":
                    # 读取整个sheet页的数据
                    sheet_data = pd.read_excel(excel_file_path, sheet_name=name)
                    
                    # 确保有足够的列
                    if len(sheet_data.columns) >= 5:
                        # 获取第五列（索引为4）
                        fifth_column = sheet_data.iloc[:, 4]
                        
                        print(f"   第五列内容:")
                        for j, value in enumerate(fifth_column):
                            if pd.notna(value):  # 只打印非空值
                                print(f"     {j+1}. {value}")
                        
                        # 检查第四列"是否主键"
                        print(f"\n   检查第四列'是否主键'，打印主键项：")
                        has_primary_key = False
                        for j in range(len(sheet_data)):
                            # 检查第四列（索引为3）是否为"Y"
                            if j < len(sheet_data) and 3 < len(sheet_data.columns) and pd.notna(sheet_data.iloc[j, 3]) and sheet_data.iloc[j, 3] == "Y":
                                # 只打印第四列
                                fourth_col_value = sheet_data.iloc[j, 3]
                                print(f"     行 {j+1}: 是主键 ({fourth_col_value})")
                                has_primary_key = True
                        
                        if not has_primary_key:
                            print("     没有找到主键")
                    else:
                        print(f"   该Sheet页列数不足，无法读取所需列")
                else:
                    print(f"   第二行第一列不是'数据项名称'")
            except Exception as e:
                print(f"   处理Sheet '{name}'时出错: {e}")
                
            print("-" * 50)
            
    except FileNotFoundError:
        print(f"错误：找不到文件 '{excel_file_path}'")
    except Exception as e:
        print(f"读取Excel文件时出错：{e}")

if __name__ == '__main__':
    # Excel文件路径
    excel_path = "/Users/xiang/Desktop/EAST/EAST2.0数据模型及分工0227.xlsx"
    
    # 处理Excel文件
    process_excel_sheets(excel_path)