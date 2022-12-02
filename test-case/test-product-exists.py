import unittest
from transaction import Transaction
import pandas as pd


class TestTransactionMethods(unittest.TestCase):
    def test_product_exists(self):
        # Set up test data
        transaction = Transaction()
        transaction.to_csv(
            pd.DataFrame(
                {
                    "item_name": ["apple", "banana", "orange"],
                    "item_quantity": [3, 4, 5],
                    "item_price": [0.99, 0.79, 0.89],
                }
            )
        )

        # Test that the method returns True for all products
        self.assertTrue(transaction.product_exists("apple"))
        self.assertTrue(transaction.product_exists("banana"))
        self.assertTrue(transaction.product_exists("orange"))


if __name__ == "__main__":
    unittest.main()
