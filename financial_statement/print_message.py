import os
import pandas as pd
import chardet
import mysql.connector
from datetime import datetime

# MySQL配置
DB_CONFIG = {
    'host': '39.105.177.10',
    'port': 3388,
    'user': 'cloud',
    'password': 'cloud',  # 请替换为实际密码
    'database': 'cloud'   # 请替换为实际数据库名
}

def get_db_connection():
    """
    获取数据库连接
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def save_to_database(df, source, file_name):
    """
    将数据保存到数据库中
    
    Args:
        df: DataFrame对象，包含交易数据
        source: 数据来源（支付宝/微信/美团）
        file_name: 原始文件名
    """
    try:
        conn = get_db_connection()
        if not conn:
            return
        
        cursor = conn.cursor()
        
        # 1. 保存商家信息
        # merchant_names = df['交易对方'].unique() if '交易对方' in df.columns else df['订单标题'].str.split('(').str[0].unique()
        # for merchant in merchant_names:
        #     if merchant and str(merchant).strip():
        #         try:
        #             cursor.execute(
        #                 "INSERT IGNORE INTO financial_merchants (merchant_name) VALUES (%s)",
        #                 (str(merchant).strip(),)
        #             )
        #         except Exception as e:
        #             print(f"插入商家数据出错 {merchant}: {e}")
        
        # 2. 保存交易记录
        for _, row in df.iterrows():
            try:
                # 根据不同来源处理字段映射
                transaction_time = row.get('交易时间') or row.get('交易成功时间')
                merchant_name = row.get('交易对方') or row.get('订单标题', '').split('(')[0]
                description = row.get('商品说明') or row.get('商品') or row.get('订单标题')
                amount = format_amount(row.get('金额') or row.get('金额(元)') or row.get('实付金额'))
                status = row.get('交易状态') or row.get('当前状态') or row.get('支付方式')
                transaction_id = row.get('交易订单号') or row.get('交易单号')
                merchant_order_id = row.get('商家订单号') or row.get('商户单号')
                payment_method = row.get('支付方式', '')
                
                cursor.execute("""
                    INSERT IGNORE INTO financial_transactions 
                    (transaction_time, merchant_name, description, type, amount, 
                     status, transaction_id, merchant_order_id, payment_method, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    transaction_time, merchant_name, description, row['收/支'], amount,
                    status, transaction_id, merchant_order_id, payment_method, source
                ))
            except Exception as e:
                print(f"插入交易记录出错: {e}")
                print(f"问题数据: {row}")
        
        # 3. 保存原始账单记录
        # try:
        #     total_amount = df[df['收/支'] == '支出']['金额'].apply(format_amount).sum() if '金额' in df.columns else \
        #                   df[df['收/支'] == '支出']['金额(元)'].apply(format_amount).sum() if '金额(元)' in df.columns else \
        #                   df[df['收/支'] == '支出']['实付金额'].apply(format_amount).sum()
        #
        #     cursor.execute("""
        #         INSERT INTO financial_raw_bills
        #         (file_name, source, import_time, start_date, end_date, total_amount, record_count)
        #         VALUES (%s, %s, %s, %s, %s, %s, %s)
        #     """, (
        #         file_name,
        #         source,
        #         datetime.now(),
        #         df['交易时间'].min() if '交易时间' in df.columns else df['交易成功时间'].min(),
        #         df['交易时间'].max() if '交易时间' in df.columns else df['交易成功时间'].max(),
        #         total_amount,
        #         len(df)
        #     ))
        # except Exception as e:
        #     print(f"插入原始账单记录出错: {e}")
        
        conn.commit()
        print(f"成功将 {file_name} 的数据保存到数据库")
        
    except Exception as e:
        print(f"保存数据到数据库时出错: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def format_amount(amount_str):
    """
    统一金额格式
    """
    if isinstance(amount_str, str):
        # 移除￥符号、空格、引号和其他可能的特殊字符
        amount = amount_str.replace('￥', '').replace(' ', '').replace('"', '').strip()
        try:
            # 处理可能的科学记数法
            return float(amount)
        except ValueError:
            try:
                # 如果有逗号，先移除逗号再转换
                amount = amount.replace(',', '')
                return float(amount)
            except ValueError:
                return 0.0  # 如果无法转换，返回0
    elif isinstance(amount_str, (int, float)):
        return float(amount_str)
    return 0.0

def format_alipay_data(df):
    """
    格式化支付宝账单数据
    """
    # 选择需要显示的列
    columns = ['交易时间', '交易对方', '商品说明', '收/支', '金额', '交易状态', '交易订单号', '商家订单号']
    df_display = df[columns].copy()
    
    # 格式化金额
    df_display['金额'] = df_display['金额'].apply(format_amount)
    
    # 清理所有列中的制表符
    for col in df_display.columns:
        if col != '金额':  # 跳过已经格式化的金额列
            df_display[col] = df_display[col].astype(str).apply(
                lambda x: x.replace('\t', '').replace('\\t', '').strip()
            )
    
    return df_display

def format_wechat_data(df):
    """
    格式化微信账单数据
    """
    try:
        # 选择需要显示的列
        columns = ['交易时间', '交易对方', '商品', '收/支', '金额(元)', '当前状态', '交易单号', '商户单号']
        df_display = df[columns].copy()
        
        # 清理金额列中的特殊字符
        df_display['金额(元)'] = df_display['金额(元)'].astype(str).apply(
            lambda x: x.replace('¥', '').replace('￥', '').replace('"', '').replace(' ', '').strip()
        )
        
        # 转换为浮点数
        df_display['金额(元)'] = pd.to_numeric(df_display['金额(元)'], errors='coerce').fillna(0.0)
        
        # 清理其他列中的制表符和多余的引号
        for col in df_display.columns:
            if col != '金额(元)':
                df_display[col] = df_display[col].astype(str).apply(
                    lambda x: x.replace('\t', '').replace('\\t', '').replace('"', '').strip()
                )
        
        return df_display
    except Exception as e:
        print(f"格式化微信数据时出错: {e}")
        print("列名:", df.columns.tolist())
        print("金额列示例:", df['金额(元)'].head().to_list())
        raise e

def format_meituan_data(df):
    """
    格式化美团账单数据
    """
    try:
        # 选择需要显示的列
        columns = ['交易成功时间', '订单标题', '收/支', '实付金额', '支付方式', '交易单号', '商家单号']
        df_display = df[columns].copy()
        
        # 清理实付金额列中的特殊字符
        df_display['实付金额'] = df_display['实付金额'].astype(str).apply(
            lambda x: x.replace('¥', '').replace('￥', '').replace('"', '').replace(' ', '').strip()
        )
        
        # 转换为浮点数
        df_display['实付金额'] = pd.to_numeric(df_display['实付金额'], errors='coerce').fillna(0.0)
        
        # 清理其他列中的制表符和多余的引号，对订单标题特殊处理
        for col in df_display.columns:
            if col == '订单标题':
                df_display[col] = df_display[col].astype(str).apply(
                    lambda x: x.replace('\t', '').replace('"', '').replace(' 订单详情', '').replace('订单详情', '').strip()
                )
            elif col != '实付金额':
                df_display[col] = df_display[col].astype(str).apply(
                    lambda x: x.replace('\t', '').replace('"', '').strip()
                )
        
        return df_display
    except Exception as e:
        print(f"格式化美团数据时出错: {e}")
        print("列名:", df.columns.tolist())
        print("实付金额列示例:", df['实付金额'].head().to_list())
        raise e

def read_alipay_csv(file_path):
    """
    专门处理支付宝账单文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        DataFrame 或 None
    """
    try:
        # 首先尝试直接用二进制模式读取文件内容
        with open(file_path, 'rb') as file:
            # 读取前4096字节来检测编码
            raw_data = file.read(4096)
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # 如果检测到的编码可信度较低，使用默认编码列表
            if result['confidence'] < 0.8:
                encodings_to_try = ['gbk', 'gb18030', 'utf-8-sig', 'utf-8', 'gb2312']
            else:
                encodings_to_try = [encoding] + ['gbk', 'gb18030', 'utf-8-sig', 'utf-8', 'gb2312']

        # 尝试每种编码
        for enc in encodings_to_try:
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding=enc) as file:
                    lines = file.readlines()
                
                # 找到真正的数据开始位置
                header_index = -1
                for i, line in enumerate(lines):
                    if any(keyword in line for keyword in ['交易时间', '交易号', '商家订单号', '收/支']):
                        header_index = i
                        break
                
                if header_index != -1:
                    # 使用pandas读取，跳过前面的行
                    df = pd.read_csv(file_path, encoding=enc, skiprows=header_index)
                    
                    # 验证数据是否正确读取（检查是否有至少一列包含预期的关键字）
                    if any(col in df.columns for col in ['交易时间', '收/支', '金额']):
                        print(f"成功读取支付宝账单")
                        return format_alipay_data(df)
                    
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"尝试使用 {enc} 编码读取时出错: {str(e)}")
                continue
        
        print("尝试了所有可能的编码都无法正确读取文件")
        return None
            
    except Exception as e:
        print(f"处理支付宝账单时出错: {str(e)}")
        return None

def read_meituan_csv(file_path):
    """
    专门处理美团账单文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        DataFrame 或 None
    """
    try:
        # 首先尝试直接用二进制模式读取文件内容
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            
            # 如果检测到的编码可信度较低，使用默认编码列表
            if result['confidence'] < 0.8:
                encodings_to_try = ['gbk', 'gb18030', 'utf-8-sig', 'utf-8', 'gb2312']
            else:
                encodings_to_try = [encoding] + ['gbk', 'gb18030', 'utf-8-sig', 'utf-8', 'gb2312']

        for enc in encodings_to_try:
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding=enc) as file:
                    lines = file.readlines()
                
                # 找到数据表头行（包含"交易创建时间"的行）
                header_index = -1
                for i, line in enumerate(lines):
                    if "交易创建时间" in line and "交易成功时间" in line:
                        header_index = i
                        break
                
                if header_index != -1:
                    # 使用pandas读取，跳过前面的行
                    df = pd.read_csv(file_path, 
                                   encoding=enc, 
                                   skiprows=header_index,
                                   dtype=str)
                    print(f"成功读取美团账单")
                    return format_meituan_data(df)
                    
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"尝试使用 {enc} 编码读取时出错: {str(e)}")
                continue
        
        print("尝试了所有可能的编码都无法正确读取文件")
        return None
            
    except Exception as e:
        print(f"处理美团账单时出错: {str(e)}")
        return None

def read_csv_with_encoding(file_path):
    """
    尝试使用不同的编码和分隔符读取CSV文件
    """
    # 对于支付宝账单，使用专门的处理函数
    if "alipay_record" in file_path:
        return read_alipay_csv(file_path)
    # 对于美团账单，使用专门的处理函数
    elif "美团账单" in file_path:
        return read_meituan_csv(file_path)
    
    # 尝试不同的编码和分隔符组合
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
    separators = [',', '\t']
    
    for encoding in encodings:
        for sep in separators:
            try:
                # 对于微信支付账单，跳过前几行
                if "微信支付账单" in file_path:
                    df = pd.read_csv(file_path, encoding=encoding, sep=sep, skiprows=16, dtype=str)
                    return format_wechat_data(df)
                else:
                    df = pd.read_csv(file_path, encoding=encoding, sep=sep, dtype=str)
                    return df
            except Exception as e:
                continue
    
    return None

def scan_csv_files(directory_path):
    """
    扫描指定目录下的所有CSV文件并返回处理后的数据
    
    Returns:
        list: 包含元组 (DataFrame, source, filename) 的列表
    """
    try:
        # 确保目录存在
        if not os.path.exists(directory_path):
            print(f"错误：目录 '{directory_path}' 不存在")
            return []
            
        # 获取目录中的所有文件
        files = os.listdir(directory_path)
        csv_files = [f for f in files if f.lower().endswith('.csv')]
        
        if not csv_files:
            print(f"在目录 '{directory_path}' 中没有找到CSV文件")
            return []
            
        total_amount = 0
        processed_data = []
        
        # 遍历所有CSV文件
        for csv_file in csv_files:
            file_path = os.path.join(directory_path, csv_file)
            print(f"\n{'='*20} {csv_file} {'='*20}")
            
            try:
                # 尝试读取CSV文件
                df = read_csv_with_encoding(file_path)
                
                if df is not None:
                    print(f"共 {len(df)} 条交易记录")
                    print("\n交易明细:")
                    pd.set_option('display.max_columns', None)
                    pd.set_option('display.width', None)
                    pd.set_option('display.max_colwidth', None)
                    pd.set_option('display.max_rows', None)
                    print(df)
                    
                    # 确定数据来源
                    source = None
                    if "alipay_record" in csv_file:
                        source = "支付宝"
                    elif "微信支付账单" in csv_file:
                        source = "微信"
                    elif "美团账单" in csv_file:
                        source = "美团"
                    
                    if source:
                        processed_data.append((df, source, csv_file))
                    
                    # 计算支出总额
                    amount_column = None
                    if '金额' in df.columns:
                        amount_column = '金额'
                    elif '金额(元)' in df.columns:
                        amount_column = '金额(元)'
                    elif '实付金额' in df.columns:
                        amount_column = '实付金额'
                        
                    if amount_column:
                        try:
                            expenses = df[df['收/支'] == '支出'][amount_column].astype(str).apply(format_amount).sum()
                            print(f"\n支出总额: {expenses:.2f} 元")
                            total_amount += expenses
                        except Exception as e:
                            print(f"计算支出总额时出错: {e}")
                            print(f"问题数据: {df[df['收/支'] == '支出'][amount_column]}")
                    
                    print("\n")
                else:
                    print(f"无法读取文件 '{csv_file}'")
                    
            except Exception as e:
                print(f"读取文件出错: {e}")
            
            print("=" * (40 + len(csv_file)))
        
        print(f"\n所有账单支出总额: {total_amount:.2f} 元")
        return processed_data
                
    except Exception as e:
        print(f"扫描目录时出错: {e}")
        return []

def save_all_to_database(processed_data):
    """
    将所有处理后的数据保存到数据库
    
    Args:
        processed_data: list of (DataFrame, source, filename) tuples
    """
    print("\n开始保存数据到数据库...")
    success_count = 0
    total_count = len(processed_data)
    
    for df, source, filename in processed_data:
        try:
            save_to_database(df, source, filename)
            success_count += 1
        except Exception as e:
            print(f"保存文件 {filename} 时出错: {e}")
    
    print(f"\n数据库保存完成！成功：{success_count}/{total_count}")

def print_welcome_message():
    """
    打印一条欢迎消息
    """
    print("欢迎使用财务报表处理系统！")

if __name__ == '__main__':
    print_welcome_message()
    
    # 指定要扫描的目录
    directory = "/Users/xiang/Library/Mobile Documents/com~apple~CloudDocs/刘云岑/管理/财政/2025-01至2025-02/"
    
    # 第一步：扫描并处理CSV文件
    print("第一步：扫描并处理CSV文件...")
    processed_data = scan_csv_files(directory)
    
    if processed_data:
        # 第二步：保存到数据库
        print("\n第二步：保存数据到数据库...")
        save_all_to_database(processed_data)
    else:
        print("\n没有找到可处理的CSV文件，跳过数据库保存步骤。") 