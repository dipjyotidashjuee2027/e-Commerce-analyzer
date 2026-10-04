"""
Static fallback description of the database schema.

DatabaseHelper.get_schema_summary() introspects the live MySQL database
first (SHOW TABLES / DESCRIBE), so this text is only used when the
database is unreachable at the moment a query is generated. Keeping a
written-out copy also makes the prompt easier to read/debug and doubles
as documentation of the data model.
"""

STATIC_SCHEMA_DESCRIPTION = """
Table `customers`: customer_id (INT, PK), first_name (VARCHAR), last_name (VARCHAR),
  email (VARCHAR), phone (VARCHAR), city (VARCHAR), state (VARCHAR), country (VARCHAR),
  signup_date (DATE)

Table `products`: product_id (INT, PK), product_name (VARCHAR), category (VARCHAR),
  price (DECIMAL), stock_quantity (INT), created_at (DATE)

Table `orders`: order_id (INT, PK), customer_id (INT, FK -> customers.customer_id),
  order_date (DATE), status (ENUM: Pending, Shipped, Delivered, Cancelled, Returned),
  total_amount (DECIMAL)

Table `order_items`: order_item_id (INT, PK), order_id (INT, FK -> orders.order_id),
  product_id (INT, FK -> products.product_id), quantity (INT), unit_price (DECIMAL),
  subtotal (DECIMAL)

Table `payments`: payment_id (INT, PK), order_id (INT, FK -> orders.order_id),
  payment_date (DATE), payment_method (ENUM: Credit Card, Debit Card, UPI, Net Banking, COD, Wallet),
  amount (DECIMAL), payment_status (ENUM: Success, Failed, Refunded, Pending)

Relationships:
- orders.customer_id references customers.customer_id (one customer has many orders)
- order_items.order_id references orders.order_id (one order has many line items)
- order_items.product_id references products.product_id
- payments.order_id references orders.order_id (one order usually has one payment)
"""

SAMPLE_QUESTIONS = [
    "What are the top 5 best-selling products by revenue?",
    "Show total revenue by month",
    "Which 10 customers have spent the most money overall?",
    "How many orders were cancelled or returned?",
    "What is the average order value by city?",
    "List products that are low on stock, below 10 units",
    "Which payment method is used most often?",
    "Show the number of orders for each order status",
    "What is the total revenue by product category?",
    "Which customers signed up in the last 90 days?",
]
