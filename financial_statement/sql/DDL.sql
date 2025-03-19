-- 2025-03-19
-- root@39.105.177.10:3388
CREATE TABLE financial_transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    transaction_time DATETIME NOT NULL COMMENT '交易时间',
    merchant_name VARCHAR(255) NOT NULL COMMENT '交易对方/商家名称',
    description TEXT COMMENT '商品说明/订单标题',
    type ENUM('收入', '支出') NOT NULL COMMENT '收支类型',
    amount DECIMAL(10,2) NOT NULL COMMENT '交易金额',
    status VARCHAR(50) NOT NULL COMMENT '交易状态',
    transaction_id VARCHAR(100) NOT NULL COMMENT '交易单号',
    merchant_order_id VARCHAR(100) COMMENT '商家订单号',
    payment_method VARCHAR(50) COMMENT '支付方式',
    source ENUM('支付宝', '微信', '美团') NOT NULL COMMENT '账单来源',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    UNIQUE KEY uk_source_transaction_id (source, transaction_id) COMMENT '来源和交易单号唯一索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录主表';

CREATE TABLE financial_merchants (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `merchant_name` varchar(255) NOT NULL COMMENT '商家名称',
  `category` varchar(50) DEFAULT NULL COMMENT '商家类别',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  `total_amount` decimal(15,2) DEFAULT '0.00' COMMENT '总交易金额',
  `transaction_count` int DEFAULT '0' COMMENT '交易次数',
  `last_transaction_time` datetime DEFAULT NULL COMMENT '最后交易时间',
  `first_transaction_time` datetime DEFAULT NULL COMMENT '首次交易时间',
  `most_used_payment` varchar(50) DEFAULT NULL COMMENT '最常用支付方式',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_merchant_name` (`merchant_name`) COMMENT '商家名称唯一索引'
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商家信息表';

CREATE TABLE financial_raw_bills (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    file_name VARCHAR(255) NOT NULL COMMENT '账单文件名',
    source ENUM('支付宝', '微信', '美团') NOT NULL COMMENT '账单来源',
    import_time DATETIME NOT NULL COMMENT '导入时间',
    start_date DATE NOT NULL COMMENT '账单开始日期',
    end_date DATE NOT NULL COMMENT '账单结束日期',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '账单总金额',
    record_count INT NOT NULL COMMENT '记录数量',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原始账单记录表';


-- cloud.financial_transactions_result definition

CREATE TABLE `financial_transactions_result` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `transaction_time` datetime NOT NULL COMMENT '交易时间',
  `merchant_name` varchar(255) NOT NULL COMMENT '交易对方/商家名称',
  `description` text COMMENT '商品说明/订单标题',
  `type` enum('收入','支出') NOT NULL COMMENT '收支类型',
  `amount` decimal(10,2) NOT NULL COMMENT '交易金额',
  `status` varchar(50) NOT NULL COMMENT '交易状态',
  `transaction_id` varchar(100) NOT NULL COMMENT '交易单号',
  `merchant_order_id` varchar(100) DEFAULT NULL COMMENT '商家订单号',
  `payment_method` varchar(50) DEFAULT NULL COMMENT '支付方式',
  `source` enum('支付宝','微信','美团') NOT NULL COMMENT '账单来源',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='有效交易记录表';


CREATE TABLE `financial_merchants_define` (
 `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `merchant_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '商家名称',
  `source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账单来源',
  `pay_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账单类型',
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci  COLLATE=utf8mb4_0900_ai_ci COMMENT='商家信息定义表';