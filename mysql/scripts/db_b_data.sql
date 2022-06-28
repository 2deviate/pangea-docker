USE ffft;
-- STATIC DATA INTO TABLES
-- PRODUCT STATUS
INSERT INTO exchange_product_status (exchange_product_status_id)
VALUES ("Available");
INSERT INTO exchange_product_status (exchange_product_status_id)
VALUES ("Unavailable");
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
    exchange_product_status_fk
)
VALUES (
    "INSTANET",
    300,
    "GB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    900.00,
    1,
    "Available"
);
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,
    exchange_product_price,
    exchange_product_default,
    exchange_product_status_fk
)
VALUES (
    "GRAVENET",
    300,
    "GB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    900.00,
    0,
    "Available"
);
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,
    exchange_product_price,
    exchange_product_default,
    exchange_product_status_fk
)
VALUES (
    "INSTANET",
    1000,
    "GB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    1200.00,
    0,
    "Available"
);
INSERT INTO exchange_product (
    exchange_product_name,
    exchange_product_limit,
    exchange_product_unit,
    exchange_product_url,
    exchange_product_price,
    exchange_product_default,
    exchange_product_status_fk
)
VALUES (
    "STAGNET",
    300,
    "GB",
    "https://pangea-group.net/pangea-5g-connectivity-enterprise-router/2",    
    900.00,
    0,
    "Unavailable"
);
