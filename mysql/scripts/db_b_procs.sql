-- USE DATABASE
USE ffft;

-- DROP AND CREATE STORED PROCS
-- File Upload Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_file_upload_status;
CREATE PROCEDURE sp_update_file_upload_status(IN file_upload_id INT, IN file_upload_status_id INT)
BEGIN
    UPDATE file_upload f SET f.file_upload_status_fk=file_upload_status_id WHERE f.file_upload_id=file_upload_id;
END$$
DELIMITER ;

-- Exchange Product Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_product_default_id;
CREATE PROCEDURE sp_get_exchange_product_default_id(OUT exchange_product_default_id INT)
BEGIN
    SELECT e.exchange_product_id INTO exchange_product_default_id FROM exchange_product e WHERE e.exchange_product_default=1 LIMIT 1;
END$$
DELIMITER ;

-- Exchange Query Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_exchange_query;
CREATE PROCEDURE sp_update_exchange_query(IN exchange_query_id INT, IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage INT, IN stop_sell_date VARCHAR(50), IN file_upload_id INT, IN exchange_query_status_id INT)
BEGIN
    UPDATE exchange_query e
    SET e.cli=cli,
        e.site_postcode=site_postcode,
        e.exchange_name=exchange_name,
        e.exchange_code=exchange_code,
        e.exchange_postcode=exchange_postcode,
        e.avg_data_usage=avg_data_usage,
        e.stop_sell_date=stop_sell_date,
        e.file_upload_fk=file_upload_id,
        e.exchange_query_status_fk=exchange_query_status_id
    WHERE e.exchange_query_id=exchange_query_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_exchange_query_status;
CREATE PROCEDURE sp_update_exchange_query_status(IN exchange_query_id INT, IN exchange_query_status_id INT)
BEGIN
    UPDATE exchange_query e SET e.exchange_query_status_fk=exchange_query_status_id WHERE e.exchange_query_id=exchange_query_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_query_by_file_upload_id;
CREATE PROCEDURE sp_get_exchange_query_by_file_upload_id(IN file_upload_id INT)
BEGIN
    SELECT e.* FROM exchange_query e WHERE e.file_upload_fk=file_upload_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_exchange_decom;
CREATE PROCEDURE sp_insert_exchange_decom(IN site_no VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_location VARCHAR(50), IN exchange_code VARCHAR(50), IN implementation_date VARCHAR(50), IN last_amended_date DATE, IN tranche VARCHAR(50), OUT exchange_decom_id INT)
BEGIN
    INSERT INTO exchange_decom (
        site_no, 
        exchange_name,         
        exchange_location,         
        exchange_code, 
        implementation_date, 
        last_amended_date, 
        tranche) 
        VALUES (
        site_no, 
        exchange_name, 
        exchange_location,         
        exchange_code, 
        implementation_date, 
        last_amended_date, 
        tranche
        );
    SET exchange_decom_id = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_count;
CREATE PROCEDURE sp_get_exchange_decom_count(OUT exchange_decom_count INT)
BEGIN
    SELECT COUNT(*) INTO exchange_decom_count FROM exchange_decom;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_truncate_exchange_decom;
CREATE PROCEDURE sp_truncate_exchange_decom()
BEGIN
    TRUNCATE TABLE exchange_decom;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_id;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_id(IN exchange_decom_id INT)
BEGIN
    SELECT * FROM exchange_decom e WHERE e.exchange_decom_id=exchange_decom_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_file_upload_by_status;
CREATE PROCEDURE sp_get_file_upload_by_status(IN file_upload_status VARCHAR(50))
BEGIN    
    SELECT f.file_upload_id, f.file_email_address FROM file_upload f WHERE f.file_upload_status=file_upload_status;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_product_pricing_by_limit;
CREATE PROCEDURE sp_get_exchange_product_pricing_by_limit(IN data_usage DECIMAL(19,2))
BEGIN       
    SELECT p.exchange_product_name, p.exchange_product_limit, p.exchange_product_unit, t.exchange_product_term_price, c.exchange_product_category, q.exchange_product_class, s.exchange_term FROM exchange_product p 
    INNER JOIN exchange_product_term t ON p.exchange_product_id=t.exchange_product_fk
    INNER JOIN exchange_product_category c ON p.exchange_product_category_fk=c.exchange_product_category_id
    INNER JOIN exchange_product_class q ON c.exchange_product_class_fk=q.exchange_product_class_id
    INNER JOIN exchange_term s ON t.exchange_term_fk = s.exchange_term_id
    WHERE p.exchange_product_limit IN (
        SELECT DISTINCT(q.exchange_product_limit) 
        FROM 
            (SELECT p1.exchange_product_limit FROM exchange_product p1 WHERE (p1.exchange_product_limit>data_usage) AND (p1.exchange_product_status_fk=1) AND (p1.exchange_product_default<>1)
            UNION ALL
            SELECT p2.exchange_product_limit FROM exchange_product p2 WHERE NOT EXISTS (SELECT * FROM exchange_product p1 WHERE (p1.exchange_product_limit>data_usage) AND (p1.exchange_product_status_fk=1) AND (p1.exchange_product_default<>1)) AND p2.exchange_product_default=1 AND p2.exchange_product_status_fk=1
            LIMIT 1) AS q
    )
    ORDER BY q.exchange_product_class, c.exchange_product_category, s.exchange_term;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_set_exchange_product_pricing_by_limit;
CREATE PROCEDURE sp_set_exchange_product_pricing_by_limit(IN exchange_query_fk INT, redis_cache_result_key VARCHAR(100))
BEGIN       
    INSERT INTO exchange_query_result (exchange_query_fk, redis_cache_result_key)
    VALUES (exchange_query_fk, redis_cache_result_key);
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_uploaded_files;
CREATE PROCEDURE sp_get_uploaded_files(IN file_upload_status VARCHAR(50))
BEGIN    
    SELECT f.* FROM file_upload f WHERE f.file_upload_status_fk=file_upload_status;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_limit;
CREATE PROCEDURE sp_get_exchange_decom_by_limit(IN no INT)
BEGIN    
    SELECT e.* FROM exchange_decom e LIMIT no;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_site;
CREATE PROCEDURE sp_get_exchange_decom_by_site(IN site_no VARCHAR(50))
BEGIN    
    SELECT e.* FROM exchange_decom e WHERE e.site_no=site_no;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_name;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_name(IN exchange_name VARCHAR(50))
BEGIN    
    SELECT e.* FROM exchange_decom e WHERE e.exchange_name=exchange_name;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_code;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_code(IN exchange_code VARCHAR(50))
BEGIN    
    SELECT e.* FROM exchange_decom e WHERE e.exchange_code=exchange_code;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_location;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_location(IN exchange_location VARCHAR(50))
BEGIN    
    SELECT e.* FROM exchange_decom e WHERE e.exchange_location=exchange_location;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_product_by_limit;
CREATE PROCEDURE sp_get_exchange_product_by_limit(IN data_usage DECIMAL(19,2))
BEGIN
    SELECT p1.* FROM exchange_product p1 WHERE (p1.exchange_product_limit>data_usage) AND (p1.exchange_product_status_fk=1) AND (p1.exchange_product_default<>1)
    UNION ALL 
    SELECT p2.* FROM exchange_product p2
    WHERE NOT EXISTS (SELECT p1.* FROM exchange_product p1 WHERE (p1.exchange_product_limit>data_usage) AND (p1.exchange_product_status_fk=1) AND (p1.exchange_product_default<>1)) 
    AND p2.exchange_product_default=1 AND p2.exchange_product_status_fk=1 LIMIT 1;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_file_upload;
CREATE PROCEDURE sp_insert_file_upload (IN file_email_address VARCHAR(150), IN file_name VARCHAR(50), IN file_path VARCHAR(150), IN file_size INT, IN file_modified_date DATE, IN file_upload_status_fk INT, OUT file_upload_id INT)
BEGIN
    INSERT INTO file_upload (
        file_email_address, 
        file_name, 
        file_path, 
        file_size, 
        file_modified_date, 
        file_upload_status_fk) 
        VALUES (
        file_email_address, 
        file_name,
        file_path,
        file_size,
        file_modified_date,
        file_upload_status_fk
        );
    SET file_upload_id = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_exchange_query;
CREATE PROCEDURE sp_insert_exchange_query (IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage INT, IN stop_sell_date VARCHAR(50), IN file_upload_fk INT, IN exchange_query_status_fk INT, OUT exchange_query_id INT)
BEGIN
    INSERT INTO exchange_query (
        cli,
        site_postcode,
        exchange_name,
        exchange_code,
        exchange_postcode,
        avg_data_usage,    
        stop_sell_date,    
        file_upload_fk,
        exchange_query_status_fk
        ) 
        VALUES (
        cli,
        site_postcode,
        exchange_name,
        exchange_code,
        exchange_postcode,
        avg_data_usage,    
        stop_sell_date,    
        file_upload_fk,
        exchange_query_status_fk
        );

    SET exchange_query_id = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_execute_sql;
CREATE PROCEDURE sp_execute_sql(IN theSQL VARCHAR(4096))
BEGIN
    SET @theSQL = theSQL;
    PREPARE dynamic_statement FROM @theSQL;
    EXECUTE dynamic_statement;
    DEALLOCATE PREPARE dynamic_statement;    
END$$
DELIMITER ;

-- FUNCTION AND VIEWS

-- FUNCTION DETERMINING EXCHANGE STATUS
DROP FUNCTION IF EXISTS p1();
CREATE FUNCTION p1() RETURNS INTEGER DETERMINISTIC NO SQL RETURN @p1;

DROP FUNCTION IF EXISTS p2();
CREATE FUNCTION p2() RETURNS INTEGER DETERMINISTIC NO SQL RETURN @p2;

DROP VIEW IF EXISTS vw_get_exchange_query_results;
CREATE VIEW vw_get_exchange_query_results AS
    SELECT
    p.file_email_address,
    q.exchange_query_id,
    q.cli,
    q.site_postcode,
    q.exchange_name,
    q.exchange_code,
    q.avg_data_usage,
    q.stop_sell_date,
    r.redis_cache_result_key
    FROM file_upload p INNER JOIN exchange_query q ON q.file_upload_fk=p.file_upload_id
    INNER JOIN exchange_query_result r ON r.exchange_query_fk=q.exchange_query_id
    WHERE p.file_upload_id=p1() AND q.exchange_query_status_fk=p2() AND r.created_at IN
    (SELECT MAX(s.created_at) FROM exchange_query_result s GROUP BY s.exchange_query_fk)
    ORDER BY r.exchange_query_fk ASC;

-- SELECT * FROM (SELECT @p1:=4, @p2:=3) param, vw_get_exchange_query_results;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_query_results;
CREATE PROCEDURE sp_get_exchange_query_results(IN file_upload_id INT)
BEGIN
    SELECT DISTINCT exchange_query_status_id 
    INTO @exchange_query_status_id 
    FROM exchange_query_status 
    WHERE exchange_query_status='Done';
    SELECT * FROM (SELECT @p1:=file_upload_id, @p2:=@exchange_query_status_id) param, vw_get_exchange_query_results;    
END$$
DELIMITER ;

