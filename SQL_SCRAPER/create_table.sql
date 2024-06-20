-- sql_scripts/create_tables.sql
CREATE TABLE SCRAPERDATA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    social_media_links TEXT,
    tech_stack TEXT,
    meta_title VARCHAR(255),
    meta_description TEXT,
    payment_gateways TEXT,
    language VARCHAR(50),
    category VARCHAR(100)
);


