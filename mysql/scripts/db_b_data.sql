USE ffft;
-- STATIC DATA INTO TABLES
-- PRODUCT STATUS
INSERT INTO exchange_product_status (exchange_product_status_id)
VALUES ("Available");
INSERT INTO exchange_product_status (exchange_product_status_id)
VALUES ("Unavailable");
-- PRODUCT TERM
INSERT INTO exchange_product_term (exchange_product_term_id)
VALUES (12);
INSERT INTO exchange_product_term (exchange_product_term_id)
VALUES (24);
INSERT INTO exchange_product_term (exchange_product_term_id)
VALUES (36);

-- FILE STATUS
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("New");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Upload");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Process");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Notify");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Sent");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Complete");
INSERT INTO file_stage_status (file_stage_status_id)
VALUES ("Exception");
-- PRODUCT
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,
    exchange_product_price,    
    exchange_product_default,
    exchange_product_status_fk,
    exchange_product_term_fk
)
VALUES (
    "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP",
    0.5,
    "MB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",        
    16.70,    
    0,
    "Available",
    12
);
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,    
    exchange_product_price,    
    exchange_product_default,
    exchange_product_status_fk,
    exchange_product_term_fk
)
VALUES (
    "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP",
    0.5,
    "MB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    9.50,
    0,
    "Available",
    24
);
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,    
    exchange_product_price,    
    exchange_product_default,
    exchange_product_status_fk,
    exchange_product_term_fk    
)
VALUES (
    "4G Cat 4 PSTN Replacement Single Net (O2 / VF / EE / 3) incl Static IP",
    0.5,
    "MB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    7.10,
    0,
    "Available",
    36
);
