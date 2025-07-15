-- 创建包含多种数据类型的表
DROP TABLE IF EXISTS khzsxjyb;
CREATE TABLE khzsxjyb (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id CHAR(10),                -- 字符串 (允许NULL)
    name VARCHAR(50),                    -- 字符串
    gender CHAR(1),                      -- 字符 (M/F)
    age INT,                             -- 整数 (允许NULL)
    credit_score DECIMAL(5,2),           -- 小数
    is_verified BOOLEAN,                 -- 布尔值
    last_contact DATE,                   -- 日期
    create_time datetime default CURRENT_TIMESTAMP ,                -- 创建时间
    balance DECIMAL(10,2),               -- 小数 (允许NULL)
    notes TEXT                           -- 包含特殊字符的文本
);

-- 插入示例数据（包含NULL值）
INSERT INTO khzsxjyb
(customer_id, name, gender, age, credit_score, is_verified, last_contact, balance, notes)
VALUES
('CUST10001', '张明', 'M', 35, 78.50, TRUE, '2025-01-15', 12000.00, 'VIP客户"推荐"'),
('CUST10002', '李芳', 'F', NULL, 92.25, FALSE, '2025-02-20', -500.00, '特殊处理|案例'),
('CUST10003', '王伟', 'M', 28, 65.00, TRUE, '2025-03-10', NULL, '新客户'),
('CUST10004', '赵燕', 'F', 42, 85.75, FALSE, '2025-04-05', 7500.00, '"信用良好"'),
('CUST10005', NULL, 'M', 50, 70.25, TRUE, '2025-05-12', 3200.00, '需电话跟进'),
('CUST10006', '孙丽', 'F', 31, 95.00, TRUE, '2025-06-30', 15000.00, '重要客户'),
('CUST10007', '周强', 'M', NULL, 55.50, FALSE, '2025-07-01', -1200.00, '临时\"优惠\"'),
(NULL, '钱东', 'M', 45, 81.00, TRUE, '2025-08-22', 9800.00, '长期合作'),
('CUST10009', '吴芳', 'F', 29, 77.75, NULL, NULL, NULL, NULL);

select * from khzsxjyb;