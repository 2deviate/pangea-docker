-- DROP AND CREATE DATABASE
DROP DATABASE IF EXISTS ffft;
CREATE DATABASE ffft;

-- USE DATABASE
USE ffft;

-- CREATE TABLES

DROP TABLE IF EXISTS file_upload;
DROP TABLE IF EXISTS file_upload_status;
DROP TABLE IF EXISTS exchange_query;
DROP TABLE IF EXISTS exchange_decom;
DROP TABLE IF EXISTS exchange_product;
DROP TABLE IF EXISTS exchange_product_status;
DROP TABLE IF EXISTS exchange_term;
DROP TABLE IF EXISTS exchange_product_term;
DROP TABLE IF EXISTS exchange_query_status;

CREATE TABLE IF NOT EXISTS exchange_query_status (
    exchange_query_status_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_query_status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS exchange_product_status (
    exchange_product_status_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_product_status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS exchange_term (    
    exchange_term_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_term INT NOT NULL
);

CREATE TABLE IF NOT EXISTS exchange_product_class (
    exchange_product_class_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_product_class VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS exchange_product_category (
    exchange_product_category_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_product_category VARCHAR(50) NOT NULL,    
    exchange_product_class_fk INT NOT NULL,    
    FOREIGN KEY (exchange_product_class_fk) REFERENCES exchange_product_class(exchange_product_class_id)
);

CREATE TABLE IF NOT EXISTS exchange_product (
    exchange_product_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_product_name VARCHAR(250) NOT NULL,
    exchange_product_limit DECIMAL(19,1) DEFAULT(0) NULL,
    exchange_product_unit VARCHAR(2) NOT NULL,
    exchange_product_url VARCHAR(250) NOT NULL,
    exchange_product_default BIT(1) DEFAULT(0) NOT NULL,
    exchange_product_status_fk INT NOT NULL,
    exchange_product_category_fk INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exchange_product_status_fk) REFERENCES exchange_product_status(exchange_product_status_id),
    FOREIGN KEY (exchange_product_category_fk) REFERENCES exchange_product_category(exchange_product_category_id)
);

CREATE INDEX idx_exchange_product_default ON exchange_product (exchange_product_default);
CREATE INDEX idx_exchange_product_limit ON exchange_product (exchange_product_limit);

CREATE TABLE IF NOT EXISTS exchange_product_term (    
    exchange_product_term_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_product_fk INT NOT NULL,
    exchange_term_fk INT NOT NULL,
    exchange_product_term_price DECIMAL(19,2) DEFAULT(0) NOT NULL,
    FOREIGN KEY (exchange_product_fk) REFERENCES exchange_product(exchange_product_id),
    FOREIGN KEY (exchange_term_fk) REFERENCES exchange_term(exchange_term_id)    
);

CREATE TABLE IF NOT EXISTS file_upload_status (
    file_upload_status_id INT AUTO_INCREMENT PRIMARY KEY,
    file_upload_status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS file_upload (
    file_upload_id INT AUTO_INCREMENT PRIMARY KEY,
    file_email_address VARCHAR(150) NOT NULL,
    file_name VARCHAR(50) NOT NULL,
    file_path VARCHAR(150) NOT NULL,
    file_size INT NOT NULL,    
    file_modified_date DATE,    
    file_upload_status_fk INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_upload_status_fk) REFERENCES file_upload_status(file_upload_status_id)
);

CREATE INDEX idx_file_upload_status_fk ON file_upload (file_upload_status_fk);

CREATE TABLE IF NOT EXISTS exchange_query (
    exchange_query_id INT AUTO_INCREMENT PRIMARY KEY,
    cli VARCHAR(50) NULL,
    site_postcode VARCHAR(50) NULL,
    exchange_name VARCHAR(50) NULL,
    exchange_code VARCHAR(50) NULL,
    exchange_postcode VARCHAR(50) NULL,
    avg_data_usage DECIMAL(19,2) NULL,    
    stop_sell_date VARCHAR(50) NULL,    
    file_upload_fk INT NOT NULL,
    exchange_query_status_fk INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_upload_fk) REFERENCES file_upload(file_upload_id),
    FOREIGN KEY (exchange_query_status_fk) REFERENCES exchange_query_status(exchange_query_status_id)
);

CREATE INDEX idx_file_upload_fk ON exchange_query (file_upload_fk);
CREATE INDEX idx_exchange_query_status_fk ON exchange_query (exchange_query_status_fk);
CREATE INDEX idx_exchange_name ON exchange_query (exchange_name);
CREATE INDEX idx_exchange_code ON exchange_query (exchange_code);

CREATE TABLE IF NOT EXISTS exchange_query_result (
    exchange_query_result_id INT AUTO_INCREMENT PRIMARY KEY,    
    exchange_query_fk INT NOT NULL,
    redis_cache_result_key VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exchange_query_fk) REFERENCES exchange_query(exchange_query_id)
);

CREATE INDEX idx_exchange_query_fk ON exchange_query_result (exchange_query_fk);
CREATE INDEX idx_created_at ON exchange_query_result (created_at);

CREATE TABLE IF NOT EXISTS exchange_decom (
    exchange_decom_id INT AUTO_INCREMENT PRIMARY KEY,
    site_no VARCHAR(50) NOT NULL,
    exchange_name VARCHAR(50) NOT NULL,
    exchange_location VARCHAR(50) NOT NULL,    
    exchange_code VARCHAR(50) NOT NULL,
    implementation_date VARCHAR(50) NOT NULL,
    last_amended_date DATE,
    tranche VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exchange_query_result_set (
    exchange_query_result_set_id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_query_result_set_key VARCHAR(100) NOT NULL,
    exchange_query_fk INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exchange_query_fk) REFERENCES exchange_query(exchange_query_id)
);

-- STORED PROCS

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
CREATE PROCEDURE sp_update_exchange_query(IN exchange_query_id INT, IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage DECIMAL(19,2), IN stop_sell_date VARCHAR(50), IN file_upload_id INT, IN exchange_query_status_id INT)
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
CREATE PROCEDURE sp_insert_exchange_query (IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage DECIMAL(19,2), IN stop_sell_date VARCHAR(50), IN file_upload_fk INT, IN exchange_query_status_fk INT, OUT exchange_query_id INT)
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
    DATE_ADD(q.stop_sell_date, INTERVAL 2 YEAR) as 'switch_off_date',
    r.redis_cache_result_key
    FROM file_upload p INNER JOIN exchange_query q ON q.file_upload_fk=p.file_upload_id
    INNER JOIN exchange_query_result r ON r.exchange_query_fk=q.exchange_query_id
    WHERE p.file_upload_id=p1() AND q.exchange_query_status_fk=p2() AND r.created_at IN
    (SELECT MAX(s.created_at) FROM exchange_query_result s GROUP BY s.exchange_query_fk)
    ORDER BY r.exchange_query_fk ASC;


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

-- STATIC DATA INTO TABLES

-- PRODUCT STATUS
INSERT INTO exchange_product_status (
    exchange_product_status_id,
    exchange_product_status
)
VALUES 
(1, "Available"),
(2, "Unavailable");

-- PRODUCT TERM
INSERT INTO exchange_term (
    exchange_term_id,
    exchange_term
)
VALUES
(1, 12),
(2, 24),
(3, 36);

-- FILE UPLOAD STATUS
INSERT INTO file_upload_status (
    file_upload_status_id,
    file_upload_status
)
VALUES 
(1, "New"),
(2, "Upload"),
(3, "Process"),
(4, "Notify"),
(5, "Sent"),
(6, "Complete"),
(7, "Exception");

-- EXCHANGE QUERY STATUS
INSERT INTO exchange_query_status (
    exchange_query_status_id,
    exchange_query_status
)
VALUES 
(1, "Wait"),
(2, "Busy"),
(3, "Done"),
(4, "Exception");

-- PRODUCT CLASS
INSERT INTO exchange_product_class (
    exchange_product_class_id,
    exchange_product_class
)
VALUES 
(1, "Single Net"),
(2, "Multi Net"),
(3, "Single Net Unlimited");

-- PRODUCT CATEGORY
INSERT INTO exchange_product_category (
    exchange_product_category_id,
    exchange_product_category, 
    exchange_product_class_fk
)
VALUES 
(1, "4G CAT 4", 1),
(2, "4G CAT 6", 1),
(3, "5G", 1),
(4, "4G CAT 4", 2),
(5, "4G CAT 6", 2),
(6, "5G", 2),
(7, "4G CAT 4", 3),
(8, "4G CAT 6", 3),
(9, "5G", 3);

-- PRODUCT
INSERT INTO exchange_product (
    exchange_product_id,
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,
    exchange_product_default,
    exchange_product_status_fk,
    exchange_product_category_fk
)
VALUES 
(1, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(2, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(3, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(4, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(5, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(6, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 1),
(7, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(8, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(9, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(10, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(11, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(12, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 2),
(13, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(14, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(15, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(16, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(17, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(18, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 3),
(19, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(20, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(21, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(22, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(23, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(24, "4G Cat 4 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 4),
(25, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(26, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(27, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(28, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(29, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(30, "4G Cat 6 PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 5),
(31, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 0.5, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(32, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 1.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(33, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 2.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(34, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 3.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(35, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 4.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(36, "5G N/R PSTN Replacement Multi Net (O2 / VF / EE / 3) incl Static IP", 5.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 0, 1, 6),
(37, "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 1, 1, 7),
(38, "4G Cat 6 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 1, 1, 8),
(39, "5G N/R PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP", 0.0, "GB", "https://pangea-group.ne/pangea-5g-connectivity-enterprise-router/2", 1, 1, 9);

-- PRODUCT TERM
INSERT INTO exchange_product_term (
    exchange_product_term_id,
    exchange_product_fk,
    exchange_term_fk,
    exchange_product_term_price
)
VALUES
(1, 1, 1, 16.7),
(2, 2, 1, 17.3),
(3, 3, 1, 18.9),
(4, 4, 1, 20.5),
(5, 5, 1, 22.2),
(6, 6, 1, 23.8),
(7, 1, 2, 9.5),
(8, 2, 2, 10.1),
(9, 3, 2, 11.8),
(10, 4, 2, 13.3),
(11, 5, 2, 15),
(12, 6, 2, 16.7),
(13, 1, 3, 7.1),
(14, 2, 3, 7.7),
(15, 3, 3, 9.4),
(16, 4, 3, 10.9),
(17, 5, 3, 12.6),
(18, 6, 3, 14.3),
(19, 7, 1, 21.1),
(20, 8, 1, 21.7),
(21, 9, 1, 23.3),
(22, 10, 1, 24.9),
(23, 11, 1, 26.6),
(24, 12, 1, 28.2),
(25, 7, 2, 11.7),
(26, 8, 2, 12.3),
(27, 9, 2, 13.9),
(28, 10, 2, 15.5),
(29, 11, 2, 17.2),
(30, 12, 2, 18.8),
(31, 7, 3, 8.6),
(32, 8, 3, 9.2),
(33, 9, 3, 10.8),
(34, 10, 3, 12.4),
(35, 11, 3, 14.1),
(36, 12, 3, 15.7),
(37, 13, 1, 44.8),
(38, 14, 1, 45.8),
(39, 15, 1, 47.1),
(40, 16, 1, 48.6),
(41, 17, 1, 50.3),
(42, 18, 1, 52.0),
(43, 13, 2, 23.6),
(44, 14, 2, 24.6),
(45, 15, 2, 25.8),
(46, 16, 2, 27.4),
(47, 17, 2, 29.1),
(48, 18, 2, 30.7),
(49, 13, 3, 16.5),
(50, 14, 3, 17.5),
(51, 15, 3, 18.7),
(52, 16, 3, 20.3),
(53, 17, 3, 22.0),
(54, 18, 3, 23.6),
(55, 19, 1, 16.4),
(56, 20, 1, 19.2),
(57, 21, 1, 22.1),
(58, 22, 1, 25.0),
(59, 23, 1, 28.0),
(60, 24, 1, 30.9),
(61, 19, 2, 9.2),
(62, 20, 2, 12.0),
(63, 21, 2, 14.9),
(64, 22, 2, 17.8),
(65, 23, 2, 20.8),
(66, 24, 2, 23.7),
(67, 19, 3, 6.8),
(68, 20, 3, 9.6),
(69, 21, 3, 12.5),
(70, 22, 3, 15.5),
(71, 23, 3, 18.4),
(72, 24, 3, 21.3),
(73, 25, 1, 20.8),
(74, 26, 1, 23.6),
(75, 27, 1, 26.5),
(76, 28, 1, 29.4),
(77, 29, 1, 32.3),
(78, 30, 1, 35.3),
(79, 25, 2, 11.4),
(80, 26, 2, 14.2),
(81, 27, 2, 17.1),
(82, 28, 2, 20.0),
(83, 29, 2, 23.0),
(84, 30, 2, 25.9),
(85, 25, 3, 8.3),
(86, 26, 3, 11.1),
(87, 27, 3, 14.0),
(88, 28, 3, 16.9),
(89, 29, 3, 19.8),
(90, 30, 3, 22.8),
(91, 31, 1, 44.5),
(92, 32, 1, 263.2),
(93, 33, 1, 50.2),
(94, 34, 1, 53.2),
(95, 35, 1, 56.1),
(96, 36, 1, 59.0),
(97, 31, 2, 23.3),
(98, 32, 2, 134.2),
(99, 33, 2, 29.0),
(100, 34, 2, 31.9),
(101, 35, 2, 34.8),
(102, 36, 2, 37.8),
(103, 31, 3, 16.2),
(104, 32, 3, 91.2),
(105, 33, 3, 21.9),
(106, 34, 3, 24.8),
(107, 35, 3, 27.8),
(108, 36, 3, 30.7),
(109, 37, 1, 38.4),
(110, 38, 1, 60.0),
(111, 39, 1, 75.0),
(112, 37, 2, 31.2),
(113, 38, 2, 55.0),
(114, 39, 2, 65.0),
(115, 37, 3, 28.8),
(116, 38, 3, 50.0),
(117, 39, 3, 55.0);

DELIMITER ;