-- ============================================================
-- E-Commerce Text-to-SQL Analytics — sample seed data
-- Run schema.sql first.
-- ============================================================

USE ecommerce_analytics;

-- ---------------------------------------------------------------
-- customers
-- ---------------------------------------------------------------
INSERT INTO customers (customer_id, first_name, last_name, email, phone, city, state, country, signup_date) VALUES
(1,  'Aarav',  'Sharma',    'aarav.sharma@example.com',    '9876543210', 'Kolkata',   'West Bengal',    'India', '2025-01-15'),
(2,  'Diya',   'Patel',     'diya.patel@example.com',      '9876543211', 'Mumbai',    'Maharashtra',    'India', '2025-01-20'),
(3,  'Vihaan', 'Mehta',     'vihaan.mehta@example.com',    '9876543212', 'Delhi',     'Delhi',          'India', '2025-02-02'),
(4,  'Ananya', 'Rao',       'ananya.rao@example.com',      '9876543213', 'Bangalore', 'Karnataka',      'India', '2025-02-10'),
(5,  'Kabir',  'Nair',      'kabir.nair@example.com',      '9876543214', 'Chennai',   'Tamil Nadu',     'India', '2025-02-18'),
(6,  'Ishita', 'Gupta',     'ishita.gupta@example.com',    '9876543215', 'Pune',      'Maharashtra',    'India', '2025-03-01'),
(7,  'Rohan',  'Verma',     'rohan.verma@example.com',     '9876543216', 'Hyderabad', 'Telangana',      'India', '2025-03-05'),
(8,  'Meera',  'Iyer',      'meera.iyer@example.com',      '9876543217', 'Ahmedabad', 'Gujarat',        'India', '2025-03-12'),
(9,  'Aditya', 'Joshi',     'aditya.joshi@example.com',    '9876543218', 'Jaipur',    'Rajasthan',      'India', '2025-03-20'),
(10, 'Sneha',  'Reddy',     'sneha.reddy@example.com',     '9876543219', 'Lucknow',   'Uttar Pradesh',  'India', '2025-04-02'),
(11, 'Arjun',  'Kapoor',    'arjun.kapoor@example.com',    '9876543220', 'Kolkata',   'West Bengal',    'India', '2025-04-10'),
(12, 'Priya',  'Malhotra',  'priya.malhotra@example.com',  '9876543221', 'Mumbai',    'Maharashtra',    'India', '2025-04-18'),
(13, 'Karan',  'Singh',     'karan.singh@example.com',     '9876543222', 'Delhi',     'Delhi',          'India', '2025-05-01'),
(14, 'Nisha',  'Agarwal',   'nisha.agarwal@example.com',   '9876543223', 'Bangalore', 'Karnataka',      'India', '2025-05-15'),
(15, 'Yash',   'Choudhary', 'yash.choudhary@example.com',  '9876543224', 'Chennai',   'Tamil Nadu',     'India', '2025-06-01');

-- ---------------------------------------------------------------
-- products
-- ---------------------------------------------------------------
INSERT INTO products (product_id, product_name, category, price, stock_quantity, created_at) VALUES
(1,  'Wireless Bluetooth Earbuds', 'Electronics',    1999.00, 120, '2025-01-01'),
(2,  'Smart Fitness Band',         'Electronics',    2499.00,  80, '2025-01-01'),
(3,  "Men's Running Shoes",        'Clothing',       3199.00,  60, '2025-01-01'),
(4,  "Women's Denim Jacket",       'Clothing',       2799.00,  45, '2025-01-01'),
(5,  'Non-Stick Frying Pan',       'Home & Kitchen', 899.00,  150, '2025-01-01'),
(6,  'Electric Kettle 1.5L',       'Home & Kitchen', 1299.00,  90, '2025-01-01'),
(7,  'The Silent Patient (Novel)', 'Books',          399.00,  200, '2025-01-01'),
(8,  'Atomic Habits',              'Books',          499.00,  250, '2025-01-01'),
(9,  'Herbal Face Wash',           'Beauty',         249.00,  300, '2025-01-01'),
(10, 'Matte Lipstick Set',         'Beauty',         599.00,  180, '2025-01-01'),
(11, 'Yoga Mat 6mm',               'Sports',         799.00,  100, '2025-01-01'),
(12, 'Adjustable Dumbbell Set',    'Sports',         4999.00,  30, '2025-01-01'),
(13, '4K Smart LED TV 43-inch',    'Electronics',   24999.00,  25, '2025-01-01'),
(14, 'Cotton Bedsheet Set',        'Home & Kitchen', 1499.00,  70, '2025-01-01'),
(15, 'Kids Storybook Bundle',      'Books',          899.00,   60, '2025-01-01');

-- ---------------------------------------------------------------
-- orders
-- ---------------------------------------------------------------
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount) VALUES
(1,  1,  '2025-04-01', 'Delivered', 4247.00),
(2,  2,  '2025-04-03', 'Delivered', 24999.00),
(3,  3,  '2025-04-05', 'Shipped',   3998.00),
(4,  4,  '2025-04-07', 'Delivered', 1397.00),
(5,  5,  '2025-04-10', 'Cancelled', 2499.00),
(6,  6,  '2025-04-12', 'Delivered', 2198.00),
(7,  7,  '2025-04-15', 'Delivered', 4999.00),
(8,  8,  '2025-04-18', 'Returned',  2799.00),
(9,  9,  '2025-04-20', 'Delivered', 1696.00),
(10, 10, '2025-04-22', 'Delivered', 1499.00),
(11, 11, '2025-05-01', 'Delivered', 2498.00),
(12, 12, '2025-05-03', 'Pending',   24999.00),
(13, 13, '2025-05-05', 'Delivered', 1798.00),
(14, 14, '2025-05-08', 'Delivered', 3998.00),
(15, 15, '2025-05-10', 'Shipped',   4998.00),
(16, 1,  '2025-05-15', 'Delivered', 2046.00),
(17, 2,  '2025-05-18', 'Delivered', 5798.00),
(18, 3,  '2025-05-20', 'Cancelled', 399.00),
(19, 4,  '2025-05-25', 'Delivered', 848.00),
(20, 5,  '2025-06-01', 'Delivered', 5997.00),
(21, 6,  '2025-06-05', 'Delivered', 2998.00),
(22, 7,  '2025-06-08', 'Delivered', 2295.00),
(23, 8,  '2025-06-10', 'Shipped',   24999.00),
(24, 9,  '2025-06-15', 'Delivered', 3398.00),
(25, 10, '2025-06-18', 'Pending',   2499.00);

-- ---------------------------------------------------------------
-- order_items
-- ---------------------------------------------------------------
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(1,  1,  2, 1999.00, 3998.00),
(1,  9,  1,  249.00,  249.00),
(2,  13, 1, 24999.00, 24999.00),
(3,  3,  1, 3199.00, 3199.00),
(3,  11, 1,  799.00,  799.00),
(4,  8,  2,  499.00,  998.00),
(4,  7,  1,  399.00,  399.00),
(5,  2,  1, 2499.00, 2499.00),
(6,  6,  1, 1299.00, 1299.00),
(6,  5,  1,  899.00,  899.00),
(7,  12, 1, 4999.00, 4999.00),
(8,  4,  1, 2799.00, 2799.00),
(9,  10, 2,  599.00, 1198.00),
(9,  9,  2,  249.00,  498.00),
(10, 14, 1, 1499.00, 1499.00),
(11, 1,  1, 1999.00, 1999.00),
(11, 8,  1,  499.00,  499.00),
(12, 13, 1, 24999.00, 24999.00),
(13, 15, 2,  899.00, 1798.00),
(14, 3,  1, 3199.00, 3199.00),
(14, 11, 1,  799.00,  799.00),
(15, 2,  2, 2499.00, 4998.00),
(16, 6,  1, 1299.00, 1299.00),
(16, 9,  3,  249.00,  747.00),
(17, 12, 1, 4999.00, 4999.00),
(17, 11, 1,  799.00,  799.00),
(18, 7,  1,  399.00,  399.00),
(19, 10, 1,  599.00,  599.00),
(19, 9,  1,  249.00,  249.00),
(20, 1,  3, 1999.00, 5997.00),
(21, 14, 2, 1499.00, 2998.00),
(22, 8,  3,  499.00, 1497.00),
(22, 7,  2,  399.00,  798.00),
(23, 13, 1, 24999.00, 24999.00),
(24, 4,  1, 2799.00, 2799.00),
(24, 10, 1,  599.00,  599.00),
(25, 2,  1, 2499.00, 2499.00);

-- ---------------------------------------------------------------
-- payments
-- ---------------------------------------------------------------
INSERT INTO payments (order_id, payment_date, payment_method, amount, payment_status) VALUES
(1,  '2025-04-01', 'Credit Card',  4247.00, 'Success'),
(2,  '2025-04-03', 'UPI',         24999.00, 'Success'),
(3,  '2025-04-05', 'Debit Card',   3998.00, 'Success'),
(4,  '2025-04-07', 'COD',         1397.00, 'Success'),
(5,  '2025-04-10', 'Wallet',      2499.00, 'Refunded'),
(6,  '2025-04-12', 'Net Banking', 2198.00, 'Success'),
(7,  '2025-04-15', 'Credit Card', 4999.00, 'Success'),
(8,  '2025-04-18', 'Debit Card',  2799.00, 'Refunded'),
(9,  '2025-04-20', 'UPI',         1696.00, 'Success'),
(10, '2025-04-22', 'COD',         1499.00, 'Success'),
(11, '2025-05-01', 'Credit Card', 2498.00, 'Success'),
(12, '2025-05-03', 'Net Banking', 24999.00, 'Pending'),
(13, '2025-05-05', 'UPI',         1798.00, 'Success'),
(14, '2025-05-08', 'Wallet',      3998.00, 'Success'),
(15, '2025-05-10', 'Credit Card', 4998.00, 'Success'),
(16, '2025-05-15', 'UPI',         2046.00, 'Success'),
(17, '2025-05-18', 'Debit Card',  5798.00, 'Success'),
(18, '2025-05-20', 'COD',          399.00, 'Refunded'),
(19, '2025-05-25', 'UPI',          848.00, 'Success'),
(20, '2025-06-01', 'Credit Card', 5997.00, 'Success'),
(21, '2025-06-05', 'Net Banking', 2998.00, 'Success'),
(22, '2025-06-08', 'UPI',         2295.00, 'Success'),
(23, '2025-06-10', 'Credit Card', 24999.00, 'Success'),
(24, '2025-06-15', 'Debit Card',  3398.00, 'Success'),
(25, '2025-06-18', 'Wallet',      2499.00, 'Failed');
