CREATE DATABASE cashier_db;
-- @block
CREATE TABLE IF NOT EXISTS transaction_history (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_name VARCHAR(255) NOT NULL,
    item_quantity INT NOT NULL,
    item_price NUMERIC(12, 2) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT NOW()
);
-- @block
DROP TABLE IF EXISTS transaction_history;
-- @block
SELECT *
FROM transaction_history;
-- @block
INSERT INTO transaction_history (item_name, item_quantity, item_price)
VALUES ('coffee', 2, 15000.99);
-- @block
# test
SELECT SUM(item_price * item_quantity)
FROM transaction_history;
-- @block
DELETE FROM transaction_history;