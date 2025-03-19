-- 商家信息表
select * from financial_merchants;
truncate table financial_merchants;
-- 原始账单记录表
select * from financial_raw_bills;
truncate table financial_raw_bills;

-- 交易记录主表
select * from financial_transactions where merchant_name ='静谧而安！！！';
truncate table financial_transactions;
-- 376
select count(0) from financial_transactions ;

-- 258
select count(0) from financial_transactions_result ;
select * from financial_transactions_del ;
-- 117
select count(0) from financial_transactions_del


create table financial_merchants_define as select * from financial_merchants;

select * from financial_merchants_define;


select * from financial_transactions where transaction_id not in (select transaction_id from financial_transactions_result ) and transaction_id not in (select transaction_id from financial_transactions_del ) ;


-- insert into financial_merchants_define(source,merchant_name) select source,merchant_name from financial_transactions_result group by source,merchant_name;
select * from financial_merchants_define;


drop table  financial_merchants_define ;
CREATE TABLE `financial_merchants_define` (
 `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `merchant_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '商家名称',
  `source` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账单来源',
  `pay_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账单类型',
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci  COLLATE=utf8mb4_0900_ai_ci COMMENT='商家信息定义表';

-- 餐饮
-- 日用
-- 零食
-- 购物
-- 服饰
-- 通讯
-- 住房
-- 交通
-- 学习
-- 医疗
-- 居家
-- 娱乐
-- 社交
-- 美容
-- 亲友
-- 水果


-- 调用存储过程
CALL process_transactions_with_result();
call update_merchant_info();

select * from financial_merchants_define;

select
	d.pay_type ,
	r.*
from
	financial_transactions_result r
left join financial_merchants_define d on
	r.merchant_name = d.merchant_name
where
	r.type = '支出'
	-- and d.pay_type is null
order by
	r.transaction_time asc;


-- -22634.00
select
	d.pay_type ,
	r.*
from
	financial_transactions_result r
left join financial_merchants_define d on
	r.merchant_name = d.merchant_name
where
	d.pay_type not in('不计入','妮妮','/','云')
order by
	r.result_amount asc;


-- 支出 8042.34
select
	d.pay_type ,
	r.*
from
	financial_transactions_result r
left join financial_merchants_define d on
	r.merchant_name = d.merchant_name
where
	r.type = '收入'
	and d.pay_type != '不计入'
order by
	r.result_amount asc;


-- 支出 --22634.00
select
	sum(r.result_amount)
from
	financial_transactions_result r
left join financial_merchants_define d on
	r.merchant_name = d.merchant_name
where
	r.type = '支出'
	and d.pay_type != '不计入'
order by
	r.result_amount asc;


select * from financial_transactions_result;

select pay_type,h.transaction_time,h.merchant_name,h.description,h.result_amount from financial_transactions_result_his h
where h.type = '支出' and pay_type not in ('/','妮妮','云','不计入');


select pay_type,h.transaction_time,h.merchant_name,h.description,h.result_amount from financial_transactions_result_his h
where h.type = '支出' and pay_type not in ('/','妮妮','云','不计入') and h.transaction_time < '2025-02-01' order by h.transaction_time desc;

select h.pay_type,sum(h.result_amount) from financial_transactions_result_his h
where h.type = '支出' and pay_type not in ('/','妮妮','云','不计入') and h.transaction_time > '2025-01-31' group BY  h.pay_type;

select h.pay_type,sum(h.result_amount) from financial_transactions_result_his h
where h.type = '支出' group BY  h.pay_type;


update financial_transactions_result r left join financial_merchants_define d on
	r.merchant_name = d.merchant_name  set r.pay_type = d.pay_type

select
	d.pay_type ,
	r.id
from
	financial_transactions_result r
left join financial_merchants_define d on
	r.merchant_name = d.merchant_name
order by
	r.result_amount asc;
