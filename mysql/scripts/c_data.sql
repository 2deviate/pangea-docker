-- USE DATABASE
USE ffft;

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

