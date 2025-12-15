-- 1. Create the Database if it doesn't exist
CREATE DATABASE IF NOT EXISTS jiomart_clone;
USE jiomart_clone;

-- 2. Create the User 'jio_user' with password '1234'
CREATE USER IF NOT EXISTS 'jio_user'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON jiomart_clone.* TO 'jio_user'@'localhost';
FLUSH PRIVILEGES;

-- 3. Create the Tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    original_price DECIMAL(10, 2),
    image_url VARCHAR(255),
    category VARCHAR(50) DEFAULT 'Cycles'
);

CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 4. Add Dummy Data
INSERT IGNORE INTO products (name, price, original_price, image_url) VALUES 
('HI-FAST 14inch Kids Cycle', 1999.00, 3379.00, 'https://m.media-amazon.com/images/I/71C7+iYmHlL._SX679_.jpg'),
('East Coast Single Speed', 3599.00, 9379.00, 'https://m.media-amazon.com/images/I/81wGn2TQJeL._SX679_.jpg'),
('UrbanStar Zoom BMX', 1999.00, 9999.00, 'https://m.media-amazon.com/images/I/61M5+4t4u0L._SX679_.jpg'),
('Leader Scout MTB 26T', 3399.00, 7039.00, 'https://m.media-amazon.com/images/I/81-s0cR8TXL._SX679_.jpg');