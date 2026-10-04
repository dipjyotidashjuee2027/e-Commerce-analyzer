-- ============================================================
-- E-Commerce Text-to-SQL Analytics — database schema
-- Run this first, then database/seed_data.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id  INT AUTO_INCREMENT PRIMARY KEY,
    first_name   VARCHAR(50)  NOT NULL,
    last_name    VARCHAR(50)  NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    phone        VARCHAR(20),
    city         VARCHAR(50),
    state        VARCHAR(50),
    country      VARCHAR(50)  DEFAULT 'India',
    signup_date  DATE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE products (
    product_id      INT AUTO_INCREMENT PRIMARY KEY,
    product_name    VARCHAR(150) NOT NULL,
    category        VARCHAR(50)  NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    stock_quantity  INT NOT NULL DEFAULT 0,
    created_at      DATE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE orders (
    order_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT NOT NULL,
    order_date    DATE NOT NULL,
    status        ENUM('Pending','Shipped','Delivered','Cancelled','Returned') NOT NULL DEFAULT 'Pending',
    total_amount  DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;

CREATE TABLE order_items (
    order_item_id  INT AUTO_INCREMENT PRIMARY KEY,
    order_id       INT NOT NULL,
    product_id     INT NOT NULL,
    quantity       INT NOT NULL,
    unit_price     DECIMAL(10,2) NOT NULL,
    subtotal       DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
) ENGINE=InnoDB;

CREATE TABLE payments (
    payment_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT NOT NULL,
    payment_date    DATE NOT NULL,
    payment_method  ENUM('Credit Card','Debit Card','UPI','Net Banking','COD','Wallet') NOT NULL,
    amount          DECIMAL(10,2) NOT NULL,
    payment_status  ENUM('Success','Failed','Refunded','Pending') NOT NULL DEFAULT 'Success',
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
) ENGINE=InnoDB;

CREATE INDEX idx_orders_customer      ON orders(customer_id);
CREATE INDEX idx_orders_date          ON orders(order_date);
CREATE INDEX idx_order_items_order    ON order_items(order_id);
CREATE INDEX idx_order_items_product  ON order_items(product_id);
CREATE INDEX idx_payments_order       ON payments(order_id);
