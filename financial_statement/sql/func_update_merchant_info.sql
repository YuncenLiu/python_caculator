DELIMITER //

CREATE PROCEDURE update_merchant_info()
BEGIN
    -- 声明变量
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_merchant_name VARCHAR(255);
    DECLARE v_total_amount DECIMAL(15,2);
    DECLARE v_transaction_count INT;
    DECLARE v_last_transaction_time DATETIME;
    DECLARE v_first_transaction_time DATETIME;
    DECLARE v_most_used_payment VARCHAR(50);

    -- 声明游标，用于获取商家统计信息
    DECLARE merchant_cursor CURSOR FOR
        SELECT
            merchant_name,
            SUM(amount) as total_amount,
            COUNT(*) as transaction_count,
            MAX(transaction_time) as last_transaction_time,
            MIN(transaction_time) as first_transaction_time,
            (
                SELECT payment_method
                FROM financial_transactions ft2
                WHERE ft2.merchant_name = ft1.merchant_name
                    AND payment_method IS NOT NULL
                    AND payment_method != ''
                GROUP BY payment_method
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ) as most_used_payment
        FROM financial_transactions ft1
        GROUP BY merchant_name;

    -- 声明继续处理的句柄
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- 开始事务
    START TRANSACTION;

    -- 打开游标
    OPEN merchant_cursor;

    -- 循环处理每个商家
    read_loop: LOOP
        -- 获取当前行数据
        FETCH merchant_cursor INTO
            v_merchant_name,
            v_total_amount,
            v_transaction_count,
            v_last_transaction_time,
            v_first_transaction_time,
            v_most_used_payment;

        -- 检查是否完成
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- 更新或插入商家信息
        INSERT INTO financial_merchants (
            merchant_name,
            total_amount,
            transaction_count,
            last_transaction_time,
            first_transaction_time,
            most_used_payment,
            updated_at
        ) VALUES (
            v_merchant_name,
            v_total_amount,
            v_transaction_count,
            v_last_transaction_time,
            v_first_transaction_time,
            v_most_used_payment,
            NOW()
        ) ON DUPLICATE KEY UPDATE
            total_amount = v_total_amount,
            transaction_count = v_transaction_count,
            last_transaction_time = v_last_transaction_time,
            first_transaction_time = v_first_transaction_time,
            most_used_payment = v_most_used_payment,
            updated_at = NOW();

    END LOOP;

    -- 关闭游标
    CLOSE merchant_cursor;

    -- 提交事务
    COMMIT;

    -- 输出更新完成信息
    SELECT CONCAT('商家信息更新完成，处理时间：', NOW()) as result;

END //

DELIMITER ;