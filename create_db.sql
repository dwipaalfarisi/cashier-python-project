CREATE DATABASE cashier_db;
-- @block
CREATE TABLE IF NOT EXISTS transaction_history (
    transaction_number SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    item_quantity INTEGER NOT NULL,
    item_price NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
-- @block
DROP TABLE IF EXISTS transaction_history;
-- @block
SELECT *
FROM transaction_history;
-- @block
# test
SELECT SUM(item_price * item_quantity)
FROM transaction_history;
-- @block
DELETE FROM transaction_history;