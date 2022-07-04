-- DROP AND CREATE DATABASE
DROP DATABASE IF EXISTS ffft;
CREATE DATABASE ffft;
USE ffft;

-- DROP AND CREATE TABLES
DROP TABLE IF EXISTS file_query;
DROP TABLE IF EXISTS file_stage;
DROP TABLE IF EXISTS exchange_decom;
DROP TABLE IF EXISTS exchange_product;
DROP TABLE IF EXISTS exchange_product_status;
DROP TABLE IF EXISTS file_stage_status;

CREATE TABLE IF NOT EXISTS exchange_product_status (    
    exchange_product_status_id VARCHAR(50) PRIMARY KEY    
);

CREATE TABLE IF NOT EXISTS exchange_product (
    exchange_product_id INT AUTO_INCREMENT PRIMARY KEY,    
    exchange_product_name VARCHAR(50) NOT NULL,
    exchange_product_limit INT NOT NULL,
    exchange_product_unit VARCHAR(2) NOT NULL,
    exchange_product_url VARCHAR(250) NOT NULL,    
    exchange_product_price DECIMAL(19,2) DEFAULT(0) NOT NULL,
    exchange_product_default BIT(1) DEFAULT(0) NOT NULL,
    exchange_product_status_fk VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exchange_product_status_fk) REFERENCES exchange_product_status(exchange_product_status_id)    
);

CREATE INDEX idx_1 ON exchange_product (exchange_product_default);
CREATE INDEX idx_2 ON exchange_product (exchange_product_limit);

CREATE TABLE IF NOT EXISTS file_stage_status (    
    file_stage_status_id VARCHAR(50) PRIMARY KEY    
);

CREATE TABLE IF NOT EXISTS file_stage (
    file_stage_id INT AUTO_INCREMENT PRIMARY KEY,
    email_address VARCHAR(150) NOT NULL,
    file_name VARCHAR(50) NOT NULL,
    file_path VARCHAR(150) NOT NULL,
    file_size INT NOT NULL,    
    file_modified_date DATE,    
    file_stage_status_fk VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    FOREIGN KEY (file_stage_status_fk) REFERENCES file_stage_status(file_stage_status_id)
);

CREATE INDEX idx_3 ON file_stage (file_stage_status_fk);

CREATE TABLE IF NOT EXISTS file_query (
    file_query_id INT AUTO_INCREMENT PRIMARY KEY,
    cli VARCHAR(50) NULL,
    site_postcode VARCHAR(50) NULL,
    exchange_name VARCHAR(50) NULL,
    exchange_code VARCHAR(50) NULL,
    exchange_postcode VARCHAR(50) NULL,
    avg_data_usage INT NULL,    
    stop_sell_date VARCHAR(50) NULL,    
    file_stage_fk INT NOT NULL,
    exchange_product_fk INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_stage_fk) REFERENCES file_stage(file_stage_id),
    FOREIGN KEY (exchange_product_fk) REFERENCES exchange_product(exchange_product_id)  
);

CREATE INDEX idx_4 ON file_query (file_stage_fk);

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

CREATE INDEX idx_5 ON file_query (exchange_name);
CREATE INDEX idx_6 ON file_query (exchange_code);

-- DROP AND CREATE STORED PROCS
-- File Stage Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_file_stage_status;
CREATE PROCEDURE sp_update_file_stage_status(IN file_stage_id INT, IN file_stage_status_id VARCHAR(50))
BEGIN
    UPDATE file_stage f SET f.file_stage_status_fk=file_stage_status_id WHERE f.file_stage_id=file_stage_id;
END$$
DELIMITER ;

-- Exchange Product Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_product_default_id;
CREATE PROCEDURE sp_get_exchange_product_default_id(OUT exchange_product_default_id INT)
BEGIN
    SELECT DISTINCT e.exchange_product_default_id INTO exchange_product_default_id FROM exchange_product e WHERE e.exchange_product_default=1;
END$$
DELIMITER ;

-- File Query Procs
DELIMITER $$
DROP PROCEDURE IF EXISTS sp_update_file_query;
CREATE PROCEDURE sp_update_file_query(IN file_query_id INT, IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage INT, IN stop_sell_date VARCHAR(50), IN exchange_product_id INT)
BEGIN
    UPDATE file_query f
    SET f.cli=cli,
        f.site_postcode=site_postcode,
        f.exchange_name=exchange_name,
        f.exchange_code=exchange_code,
        f.exchange_postcode=exchange_postcode,
        f.avg_data_usage=avg_data_usage,
        f.stop_sell_date=stop_sell_date,
        f.exchange_product_fk=exchange_product_id
    WHERE f.file_query_id=file_query_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_file_query_by_file_stage_id;
CREATE PROCEDURE sp_get_file_query_by_file_stage_id(IN file_stage_id INT)
BEGIN
    SELECT * FROM file_query f WHERE f.file_stage_fk=file_stage_id;
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
DROP PROCEDURE IF EXISTS sp_get_file_stage_by_status;
CREATE PROCEDURE sp_get_file_stage_by_status(IN file_stage_status VARCHAR(50))
BEGIN    
    SELECT f.file_stage_id, f.email_address FROM file_stage f WHERE f.file_stage_status=file_stage_status;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_recommendations;
CREATE PROCEDURE sp_get_recommendations(IN file_stage_id INT)
BEGIN
    SELECT q.cli,
        q.site_postcode,
        q.exchange_name,
        q.exchange_code,
        q.exchange_postcode,
        q.avg_data_usage,
        q.stop_sell_date,    
        p.exchange_product_name,
        p.exchange_product_limit,
        p.exchange_product_unit,
        p.exchange_product_url,    
        p.exchange_product_price,
        f.created_at
    FROM file_stage f 
    INNER JOIN file_query q ON q.file_stage_fk=f.file_stage_id
    INNER JOIN exchange_product p ON p.exchange_product_id=q.exchange_product_fk
    WHERE f.file_stage_id=file_stage_id;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_uploaded_files;
CREATE PROCEDURE sp_get_uploaded_files(IN file_stage_status VARCHAR(50))
BEGIN    
    SELECT * FROM file_stage f WHERE f.file_stage_status_fk=file_stage_status;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_limit;
CREATE PROCEDURE sp_get_exchange_decom_by_limit(IN no INT)
BEGIN    
    SELECT * FROM exchange_decom e LIMIT no;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_site;
CREATE PROCEDURE sp_get_exchange_decom_by_site(IN site_no VARCHAR(50))
BEGIN    
    SELECT * FROM exchange_decom e WHERE e.site_no=site_no;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_name;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_name(IN exchange_name VARCHAR(50))
BEGIN    
    SELECT * FROM exchange_decom e WHERE e.exchange_name=exchange_name;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_code;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_code(IN exchange_code VARCHAR(50))
BEGIN    
    SELECT * FROM exchange_decom e WHERE e.exchange_code=exchange_code;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_get_exchange_decom_by_exchange_location;
CREATE PROCEDURE sp_get_exchange_decom_by_exchange_location(IN exchange_location VARCHAR(50))
BEGIN    
    SELECT * FROM exchange_decom e WHERE e.exchange_location=exchange_location;
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_exchange_product_find_by_limit;
CREATE PROCEDURE sp_exchange_product_find_by_limit(IN exchange_product_limit INT, IN exchange_product_status VARCHAR(50))
BEGIN    
    SELECT * FROM exchange_product p1 WHERE p1.exchange_product_limit >= exchange_product_limit AND p1.exchange_product_status_fk=exchange_product_status
    UNION ALL 
    SELECT * FROM exchange_product p2
    WHERE NOT EXISTS (SELECT * FROM exchange_product p3 WHERE p3.exchange_product_limit >= exchange_product_limit AND p3.exchange_product_status_fk=exchange_product_status) 
    AND p2.exchange_product_default=1 AND p2.exchange_product_status_fk=exchange_product_status LIMIT 1;
END$$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_file_stage;
CREATE PROCEDURE sp_insert_file_stage (IN email_address VARCHAR(150), IN file_name VARCHAR(50), IN file_path VARCHAR(150), IN file_size INT, IN file_modified_date DATE, IN file_stage_status_fk VARCHAR(50), OUT file_stage_id INT)
BEGIN
    INSERT INTO file_stage (
        email_address, 
        file_name, 
        file_path, 
        file_size, 
        file_modified_date, 
        file_stage_status_fk) 
        VALUES (
        email_address, 
        file_name,
        file_path,
        file_size,
        file_modified_date,
        file_stage_status_fk
        );
    SET file_stage_id = LAST_INSERT_ID();
END$$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS sp_insert_file_query;
CREATE PROCEDURE sp_insert_file_query (IN cli VARCHAR(50), IN site_postcode VARCHAR(50), IN exchange_name VARCHAR(50), IN exchange_code VARCHAR(50), IN exchange_postcode VARCHAR(50), IN avg_data_usage INT, IN stop_sell_date VARCHAR(50), IN file_stage_fk INT, IN exchange_product_fk INT, OUT file_query_id INT)
BEGIN
    INSERT INTO file_query (
        cli,
        site_postcode,
        exchange_name,
        exchange_code,
        exchange_postcode,
        avg_data_usage,    
        stop_sell_date,    
        file_stage_fk,
        exchange_product_fk
        ) 
        VALUES (
        cli,
        site_postcode,
        exchange_name,
        exchange_code,
        exchange_postcode,
        avg_data_usage,    
        stop_sell_date,    
        file_stage_fk,
        exchange_product_fk
        );

    SET file_query_id = LAST_INSERT_ID();
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
