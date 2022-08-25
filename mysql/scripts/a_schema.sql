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

-- FUNCTION AND VIEWS

-- FUNCTION DETERMINING EXCHANGE STATUS
DROP FUNCTION IF EXISTS p1;
CREATE FUNCTION p1() RETURNS INTEGER DETERMINISTIC NO SQL RETURN @p1;

DROP FUNCTION IF EXISTS p2;
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
