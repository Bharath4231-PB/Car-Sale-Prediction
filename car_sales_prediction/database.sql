-- Create Database
CREATE DATABASE IF NOT EXISTS car_sales_db;
USE car_sales_db;

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    car_name VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    present_price FLOAT NOT NULL,
    kms_driven INT NOT NULL,
    fuel_type VARCHAR(50) NOT NULL,
    seller_type VARCHAR(50) NOT NULL,
    transmission VARCHAR(50) NOT NULL,
    owner INT NOT NULL,
    predicted_price FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Index for Better Performance
CREATE INDEX idx_user_id ON predictions(user_id);
CREATE INDEX idx_created_at ON predictions(created_at);

-- Insert Admin User (username: admin, password: admin123)
INSERT INTO users (username, email, password, is_admin) VALUES 
('admin', 'admin@carsales.com', 'pbkdf2:sha256:600000$xxxxxx$xxxxx', TRUE);
