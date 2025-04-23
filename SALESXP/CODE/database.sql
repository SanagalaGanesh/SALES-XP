CREATE DATABASE saree_management;
USE saree_management;

CREATE TABLE sarees (
    saree_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fabric VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    stock_quantity INT NOT NULL,
    barcode VARCHAR(50) UNIQUE NOT NULL
);
ALTER TABLE sarees DROP INDEX barcode;

INSERT INTO sarees (name, fabric, color, price, stock_quantity, barcode) VALUES
('Banarasi Silk Saree', 'Silk', 'Maroon', 2500.00, 15, 'SAR8GJXKZPQR'),
('Kanchipuram Silk Saree', 'Silk', 'Gold', 3200.00, 12, 'SAR5YLHNRZVX'),
('Chiffon Saree', 'Chiffon', 'Pink', 1800.00, 20, 'SAR3TQPWNKYM'),
('Georgette Saree', 'Georgette', 'Blue', 1900.00, 18, 'SAR9KXJPLMQZ'),
('Cotton Saree', 'Cotton', 'Green', 1200.00, 25, 'SAR7YXRMQJNT'),
('Tussar Silk Saree', 'Silk', 'Beige', 2800.00, 10, 'SAR4PQKJZTXM'),
('Art Silk Saree', 'Silk', 'Orange', 1500.00, 30, 'SAR2XMRJQKNT'),
('Paithani Saree', 'Silk', 'Purple', 3500.00, 8, 'SAR6WPLTJKQX'),
('Linen Saree', 'Linen', 'Yellow', 1400.00, 22, 'SAR8LJKPQXRM'),
('Organza Saree', 'Organza', 'Silver', 2900.00, 9, 'SAR5XZMTJQLN'),
('Satin Saree', 'Satin', 'Lavender', 1700.00, 14, 'SAR3NTXJKLPQ'),
('Net Saree', 'Net', 'Black', 2000.00, 11, 'SAR7RQLKJXMT'),
('Crepe Saree', 'Crepe', 'Teal', 1600.00, 16, 'SAR9TXMRJQLK'),
('Silk Blend Saree', 'Silk Blend', 'Coral', 1750.00, 13, 'SAR4KXJLQMTN'),
('Printed Cotton Saree', 'Cotton', 'Magenta', 1300.00, 21, 'SAR2RJXKMTQL'),
('Kota Doria Saree', 'Cotton', 'Sky Blue', 1100.00, 26, 'SAR6PQXJTKMN'),
('Bhagalpuri Silk Saree', 'Silk', 'Ivory', 2600.00, 10, 'SAR8NQLJXTKM'),
('Jute Silk Saree', 'Jute', 'Brown', 2200.00, 17, 'SAR5XKJQLMTN'),
('Uppada Silk Saree', 'Silk', 'Peach', 2700.00, 12, 'SAR3MTJQLXNR'),
('Chanderi Silk Saree', 'Silk', 'Turquoise', 2400.00, 19, 'SAR7XJMTQLKN'),
('Kalamkari Saree', 'Cotton', 'Mustard', 1850.00, 23, 'SAR9PLJQXMTN'),
('Mysore Silk Saree', 'Silk', 'Wine', 2950.00, 7, 'SAR4XJMTQLPN'),
('Pochampally Saree', 'Silk', 'Olive Green', 3100.00, 11, 'SAR2NLJQXKMT'),
('Brasso Saree', 'Brasso', 'Off White', 1450.00, 20, 'SAR6KXJMTQLN'),
('Kota Silk Saree', 'Silk', 'Dark Green', 2300.00, 13, 'SAR8JXQMTNLK'),
('Designer Saree', 'Georgette', 'Gold', 3400.00, 10, 'SAR5XJMTLQNK'),
('Patola Saree', 'Silk', 'Navy Blue', 3750.00, 9, 'SAR3PLJXKQMT'),
('Kasavu Saree', 'Cotton', 'Cream', 1900.00, 18, 'SAR7XJMTLQPK'),
('Fancy Saree', 'Polyester', 'Silver', 1250.00, 24, 'SAR9XJMTQLKP'),
('Handloom Saree', 'Handloom', 'Red', 2050.00, 14, 'SAR4XJMTQLNP'),
('Supernet Saree', 'Supernet', 'Pink', 1550.00, 22, 'SAR2XJMTQLPK'),
('Kanchipuram Pure Silk Saree', 'Silk', 'Royal Blue', 4200.00, 6, 'SAR6XJMTQLPP'),
('Cotton Blend Saree', 'Cotton Blend', 'Grey', 1100.00, 28, 'SAR8XJMTQLPM'),
('Pure Georgette Saree', 'Georgette', 'Lemon Yellow', 2700.00, 11, 'SAR5XJMTQLPL'),
('Soft Silk Saree', 'Silk', 'Pastel Blue', 2800.00, 15, 'SAR3XJMTQLPB'),
('Banarasi Organza Saree', 'Organza', 'Golden', 3100.00, 10, 'SAR7XJMTQLPT'),
('Chikankari Saree', 'Cotton', 'Light Green', 2350.00, 12, 'SAR9XJMTQLPG'),
('Party Wear Saree', 'Net', 'Dark Red', 2600.00, 18, 'SAR4XJMTQLPD'),
('Jacquard Saree', 'Jacquard', 'Copper', 2250.00, 16, 'SAR2XJMTQLPF'),
('Traditional Saree', 'Silk', 'Multicolor', 3300.00, 9, 'SAR6XJMTQLPA'),
('Festival Wear Saree', 'Chiffon', 'Light Pink', 2100.00, 17, 'SAR8XJMTQLPC'),
('Occasion Wear Saree', 'Satin', 'Rose Gold', 2900.00, 14, 'SAR5XJMTQLPE'),
('Ethnic Saree', 'Silk', 'Dark Blue', 2750.00, 13, 'SAR3XJMTQLPH'),
('Weaving Saree', 'Handloom', 'Golden Brown', 3500.00, 7, 'SAR7XJMTQLPJ'),
('Casual Wear Saree', 'Linen', 'Mint Green', 1850.00, 25, 'SAR9XJMTQLPI'),
('Silk Cotton Saree', 'Silk Cotton', 'Sky Blue', 2150.00, 20, 'SAR4XJMTQLPK'),
('Lace Saree', 'Net', 'Champagne', 2400.00, 11, 'SAR2XJMTQLPN'),
('Sambalpuri Saree', 'Cotton', 'Black and White', 2700.00, 9, 'SAR6XJMTQLPO'),
('Ikat Saree', 'Silk', 'Crimson', 3500.00, 8, 'SAR8XJMTQLPZ'),
('Embroidered Saree', 'Net', 'Peach', 2900.00, 12, 'SAR5XJMTQLQ1'),
('Fusion Saree', 'Georgette', 'Rust', 1600.00, 22, 'SAR3XJMTQLQ2'),
('Contrast Border Saree', 'Silk', 'Red and Black', 3200.00, 10, 'SAR7XJMTQLQ3'),
('Mirror Work Saree', 'Chiffon', 'Dark Magenta', 2000.00, 17, 'SAR9XJMTQLQ4');

INSERT INTO sarees (name, fabric, color, price, stock_quantity, barcode) VALUES
('Digital Print Saree', 'Georgette', 'Aqua Blue', 1750.00, 18, 'SARX6WHSORYP'),
('Dola Silk Saree', 'Silk', 'Blush Pink', 2600.00, 12, 'SAR1CVO5M3L4'),
('Matka Silk Saree', 'Silk', 'Champagne Gold', 2800.00, 10, 'SARPB4WU9BD3'),
('Kora Silk Saree', 'Silk', 'Rosewood', 3200.00, 9, 'SARVW7E6NIAS'),
('Velvet Saree', 'Velvet', 'Burgundy', 5000.00, 7, 'SAR00P8E37NF'),
('Raw Silk Saree', 'Silk', 'Saffron', 3100.00, 8, 'SARCELAS9ZRM'),
('Paithani Cotton Saree', 'Cotton', 'Pale Yellow', 1800.00, 20, 'SAR5E5GX98NE'),
('Muga Silk Saree', 'Silk', 'Off White', 4000.00, 5, 'SAR98GXXLJAK'),
('Soft Banarasi Saree', 'Silk', 'Rust Red', 2700.00, 15, 'SAR7USIJUWTJ'),
('Satin Border Saree', 'Satin', 'Sea Green', 1950.00, 17, 'SARQAWM0DDD1'),
('Patola Cotton Saree', 'Cotton', 'Caramel Brown', 2350.00, 14, 'SAR2EXHNG9WC'),
('Tissue Saree', 'Tissue', 'Lavender', 2750.00, 11, 'SAR3JZ05NCQX'),
('Woven Silk Saree', 'Silk', 'Ash Grey', 3300.00, 8, 'SAR7A9WV4RMS'),
('Leheriya Saree', 'Georgette', 'Orange-Pink', 2150.00, 19, 'SARLKYQG57WA'),
('Half and Half Saree', 'Silk Blend', 'Blue-White', 2450.00, 13, 'SARM5ZW8YX0J'),
('Batik Print Saree', 'Cotton', 'Chocolate Brown', 1700.00, 21, 'SARHJZK7QMV9'),
('Block Print Saree', 'Cotton', 'Beige-Grey', 1850.00, 22, 'SARNCG5WAQ78'),
('Jamawar Saree', 'Silk', 'Black-Gold', 4200.00, 6, 'SAR9GJXLRP0N'),
('Shimmer Saree', 'Net', 'Golden Glow', 2500.00, 18, 'SAR6WNJMAYQX'),
('Litchi Silk Saree', 'Silk', 'Pale Pink', 2800.00, 12, 'SAR0WPGRM9XL'),
('Banarasi Tissue Saree', 'Silk', 'Ivory Gold', 3100.00, 10, 'SARJZLX9RMW8'),
('Gadwal Saree', 'Silk', 'Indigo', 3800.00, 8, 'SARWNGAYX0JP'),
('Maheshwari Saree', 'Cotton Silk', 'Charcoal Grey', 2750.00, 14, 'SARJMK7ZWXQP'),
('Baluchari Saree', 'Silk', 'Brick Red', 3350.00, 9, 'SAR7NGZ5JWXM'),
('Zari Work Saree', 'Silk', 'Olive Green', 2900.00, 13, 'SARXZGMW9JLP'),
('Ajrakh Print Saree', 'Cotton', 'Deep Maroon', 2400.00, 16, 'SAR9WZMK7LGX'),
('Chanderi Cotton Saree', 'Cotton', 'Sky Blue', 1750.00, 20, 'SAR0LX7JMWNG'),
('Floral Print Saree', 'Georgette', 'Pastel Green', 1950.00, 23, 'SARQW7M9ZJGL'),
('Silk Zari Weave Saree', 'Silk', 'Dark Teal', 3600.00, 7, 'SARX9JLWMGZ7'),
('Banarasi Kora Saree', 'Silk', 'Lilac', 3250.00, 11, 'SAR7M9LGXWJZ'),
('Organza Zari Saree', 'Organza', 'Peach-Pink', 2850.00, 12, 'SARW9L7XZJMG'),
('Festive Silk Saree', 'Silk', 'Burnt Orange', 3450.00, 9, 'SARMLJZGX7WN'),
('Dual Tone Saree', 'Silk', 'Violet-Blue', 3300.00, 10, 'SAR9JWM7LZXG'),
('Modern Digital Print Saree', 'Georgette', 'Multicolor', 1600.00, 25, 'SARW7LGXJZ9M'),
('Hand Batik Saree', 'Cotton', 'Rust Brown', 2250.00, 18, 'SARJ9GWLXM7Z'),
('Banarasi Jaal Saree', 'Silk', 'Light Gold', 3850.00, 6, 'SAR7XLJ9ZMWG'),
('Antique Weave Saree', 'Silk', 'Dusty Rose', 2750.00, 12, 'SARWZGLX9J7M'),
('Embroidered Net Saree', 'Net', 'Pastel Blue', 3200.00, 11, 'SARLJ7WMGZX9'),
('Contrast Weave Saree', 'Silk Blend', 'Wine-Gold', 2900.00, 14, 'SAR9ZJMWXG7L'),
('South Cotton Saree', 'Cotton', 'Light Brown', 1900.00, 20, 'SARW7XZJLMG9'),
('Artistic Kalamkari Saree', 'Cotton', 'Off White-Black', 2150.00, 17, 'SARJ9GWM7XLZ'),
('Abstract Printed Saree', 'Georgette', 'Lavender-Mustard', 1850.00, 22, 'SARW7XZJMLG9'),
('Fancy Lace Saree', 'Net', 'Soft Pink', 2450.00, 13, 'SAR9LJXWM7ZG'),
('Mysore Art Silk Saree', 'Silk', 'Indigo-Red', 2700.00, 15, 'SARW7XZJMLG9'),
('Paithani Silk Blend Saree', 'Silk Blend', 'Emerald Green', 3100.00, 10, 'SAR9JMW7LXZG'),
('Designer Net Saree', 'Net', 'Fuchsia', 1800.00, 23, 'SARJMW7LZX9G'),
('Banarasi Handloom Saree', 'Silk', 'Reddish Brown', 3500.00, 9, 'SAR9JMWX7LZG'),
('Boho Chic Saree', 'Cotton Blend', 'Yellow-Pink', 1700.00, 25, 'SARW7XZJMLG9');





CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_number VARCHAR(15) NOT NULL,
    salesperson_id VARCHAR(50) NOT NULL,
    payment_method ENUM('cash', 'card', 'upi') NOT NULL,
    total float NOT NULL,
    transaction_date DATETIME NOT NULL
);

CREATE TABLE transaction_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    saree_id INT NOT NULL,
    quantity INT NOT NULL,
    price float NOT NULL,
    discount float NOT NULL DEFAULT 0,
    amount float NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (saree_id) REFERENCES sarees(saree_id)
);



CREATE TABLE transactions_encrypted (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_number VARCHAR(15),
    salesperson_id VARCHAR(50),
    payment_method VARCHAR(20),
    total DOUBLE,
    transaction_date DATETIME
);


CREATE TABLE transaction_items_encrypted (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    saree_id INT,
    quantity INT,
    price DOUBLE,
    discount DOUBLE,
    amount_encrypted BLOB,
    FOREIGN KEY (transaction_id) REFERENCES transactions_encrypted(transaction_id),
    FOREIGN KEY (saree_id) REFERENCES sarees(saree_id)
);

select * from transaction_items_encrypted;

ALTER TABLE transactions_encrypted
CHANGE COLUMN total total_encrypted BLOB;


ALTER TABLE sarees MODIFY COLUMN price float;
ALTER TABLE transactions MODIFY COLUMN total float;
ALTER TABLE transaction_items MODIFY COLUMN price float;
ALTER TABLE transaction_items MODIFY COLUMN discount float;
ALTER TABLE transaction_items MODIFY COLUMN amount float;







CREATE TABLE users (
    emp_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('admin', 'billingdesk', 'salesperson') NOT NULL,
    password VARCHAR(255) NOT NULL
);

ALTER TABLE users MODIFY COLUMN role ENUM('admin', 'salesperson', 'billing_desk');

delete from users where emp_id='SP001';
select * from sarees;

select * from users;

delete from users where empid='SP001';
drop table transactions;
select * from transactions;

select * from transaction_items;

