import pandas as pd
from database import ReadAndWrite


class Choice:
    """A class related to user input"""

    def is_string(self, value) -> bool:
        result = isinstance(value, str)
        return result

    def is_integer(self, value) -> bool:
        result = isinstance(value, int)
        return result

    def is_float(self, value) -> bool:
        result = isinstance(value, float)
        return result

    def name_input(self) -> str:
        try:
            name = str(input("Item Name: "))
            return name
        except (ValueError):
            print("Wrong input")
        except (Exception):
            print("Unexpected error. It's us, not you.")

    def quantity_input(self) -> int:
        try:
            quantity = int(input("Quantity: "))
            return quantity
        except (ValueError):
            print("Wrong input")
        except (Exception):
            print("Unexpected error. It's us, not you.")

    def price_input(self) -> float:
        try:
            price = float(input("Item Price: "))
            return price
        except (ValueError):
            print("Wrong input")
        except (Exception):
            print("Unexpected error. It's us, not you.")

    def choice_add_item(self) -> list[str, int, float]:
        name = self.name_input()
        quantity = self.quantity_input()
        price = self.price_input()
        return [name, quantity, price]

    def choice_update_item_name(self) -> list[str, str]:
        name = self.name_input()
        new_name = self.name_input()
        return [name, new_name]

    def choice_update_item_quantity(self) -> list[str, int]:
        name = self.name_input()
        new_quantity = self.quantity_input()
        return [name, new_quantity]

    def choice_update_item_price(self) -> list[str, float]:
        name = self.name_input()
        new_price = self.price_input()
        return [name, new_price]


class Transaction:
    """A class for all methods related to a transaction

    ...

    Attributes
    ----------
    file_path : path for the staging file
        Used for methods referring to the staging file.
        Usage:
            read and write csv
    """

    def __init__(self):
        self.file_path = "./transaction-staging.csv"

    def read_csv(self) -> pd.DataFrame:
        """Read CSV: the staging file

        Returns:
            pd.DataFrame: transaction table
        """
        df = pd.read_csv(self.file_path, encoding="utf-8")
        return df

    def to_csv(self, df: pd.DataFrame) -> None:
        """Export transaction to CSV: the staging file

        Args:
            df (pd.DataFrame): transaction table to be exported
        """
        df.to_csv(self.file_path, index=False)

    def product_exists(self, name: str) -> bool:
        """Check if the name of a product is already in the staging file
        Usage:
            update_name, update_quantity, update_price
        Args:
            name (str): item name

        Returns:
            bool: True if the product name is already in the staging file, False otherwise
        """
        df = self.read_csv()
        condition = name in df.item_name.values
        if condition:
            return True
        print("No changes made. Item does not exist.")
        return False

    def product_not_exists(self, name: str) -> bool:
        """Check if the name of a product not in the staging file
        Usage:
            add_item
        Args:
            name (str): item name

        Returns:
            bool: True if the product name not in the staging file, False otherwise
        """
        df = self.read_csv()

        # NOTE:  FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
        # not in expect the left and right operands to be the same type. Using astype would eliminate this issue
        condition = name not in df.item_name.values.astype(str)
        if condition:
            return True
        print("No changes made. The item is already exist.")
        return False

    def add_item(self, target: ReadAndWrite, choice: Choice) -> None:
        """_summary_

        Args:
            target (ReadAndWrite): Instantiate ReadAndWrite class to access write_values (adding new items to the staging file)
            choice (Choice): Instantiate Choice class to access choice_add_item (user transaction input)
        """
        item = choice.choice_add_item()
        product_not_exists = self.product_not_exists(item[0])
        if product_not_exists:
            target.write_values(item)
            print("Added")
        else:
            print("Not added")

    def check_product_list(self) -> bool:
        """Check if the staging file is not empty

        Returns:
            bool: True if the staging file is not empty, False otherwise
        """
        return len(self.read_csv()) > 0

    def check_order(self) -> None:
        """Show the transaction order to the user by reading the staging file"""
        not_empty = self.check_product_list()
        if not_empty:
            # import and drop nulls
            df = self.read_csv()
            self.drop_nulls(df)
            # display basket
            with pd.option_context(
                "expand_frame_repr", False, "display.max_rows", None
            ):
                print(df)
        else:
            print("Empty basket. Try to add an item first.")

    def discount(self, total_payment: float) -> float:
        """Apply discount to the total_price

        Args:
            total_payment (float): total billings

        Returns:
            float: discount rate
        """
        total = abs(total_payment)
        if 0 < total <= 200_000:
            discount_percent = 1
            print("No Discount")
        elif 200_000 < total <= 300_000:
            discount_percent = 0.95
            print("Discount 5%")
        elif 300_000 < total <= 500_000:
            discount_percent = 0.92
            print("Discount 8%")
        elif total > 500_000:
            discount_percent = 0.90
            print("Discount 10%")
        return discount_percent

    def total_price(self) -> None:
        """Show the total price to the user"""
        not_empty = self.check_product_list()
        if not_empty:
            # import and drop nulls
            df = self.read_csv()
            self.drop_nulls(df)
            # calculate
            total_payment = (df.item_quantity * df.item_price).sum()
            discount_rate = self.discount(total_payment)
            print("Total Bill:")
            print(f"Before discount: {total_payment}")
            print(f"After discount: {total_payment * discount_rate}")
        else:
            print("Empty basket. Please add item first.")

    def remove_item(self, choice: Choice) -> None:
        """Remove an item from the staging file

        Args:
            choice (Choice): Instantiate Choice class to access name_input (user transaction input)
        """
        not_empty = self.check_product_list()
        if not_empty:
            df = self.read_csv()
            name = choice.name_input()
            condition = df["item_name"] != str(name)
            df_after = df[condition]
            self.to_csv(df_after)
        else:
            print(
                "There's nothing to remove. Either it's empty or the item name isn't in the basket."
            )

    def reset_transaction(self, select: ReadAndWrite) -> None:
        """Delete all records from the staging file

        Args:
            select (ReadAndWrite): instantiate ReadAndWrite to access write_header (rewrite the file)
        """
        select.write_header()

    def update_value(
        self,
        df: pd.DataFrame,
        col: str,
        old_value: str | int | float,
        new_value: str | int | float,
    ) -> pd.DataFrame:
        """Update value of a record in the staging file

        Args:
            df (pd.DataFrame): transaction table
            col (str): column name (item_name or item_quantity or item_price)
            old_value (str | int | float): value to be replaced (item_name or item_quantity or item_price)
            new_value (str | int | float): new value (item_name or item_quantity or item_price)

        Returns:
            pd.DataFrame: transaction table
        """
        df[col] = df[col].replace([old_value], new_value)
        return df

    def update_name(self, choice: Choice) -> None:
        """Update the name of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class to access choice_update_item_name (user transaction input)
        """
        name_list = choice.choice_update_item_name()
        not_empty = self.check_product_list()
        product_exists = self.product_exists(name_list[0])

        if not_empty and product_exists:
            df = self.read_csv()
            df_after = self.update_value(
                df=df, col="item_name", old_value=name_list[0], new_value=name_list[1]
            )
            self.to_csv(df_after)
        else:
            print("Item not found. Try to add it first.")

    def update_quantity(self, choice: Choice) -> None:
        """Update the quantity of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class to access choice_update_item_quantity (user transaction input)
        """
        value_list = choice.choice_update_item_quantity()
        not_empty = self.check_product_list()
        product_exists = self.product_exists(value_list[0])

        if not_empty and product_exists:
            df = self.read_csv()
            condition = df.item_name == value_list[0]
            # replace
            df.loc[condition, "item_quantity"] = value_list[1]
            df.item_quantity.astype("int64")
            self.to_csv(df)
        else:
            print("Item not found. Try to add it first.")

    def update_price(self, choice: Choice) -> None:
        """Update the price of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class to access choice_update_item_price (user transaction input)
        """
        value_list = choice.choice_update_item_price()
        not_empty = self.check_product_list()
        product_exists = self.product_exists(value_list[0])

        if not_empty and product_exists:
            df = self.read_csv()
            condition = df.item_name == value_list[0]
            # replace
            df.loc[condition, "item_price"] = value_list[1]
            self.to_csv(df)
        else:
            print("Item not found. Try to add it first.")

    def drop_nulls(self, df: pd.DataFrame) -> None:
        """Drop null values from the staging file
        Usage:

        Args:
            df (pd.DataFrame): transaction table
        """
        df = df.dropna()
        # copy to prevent float dtype on quantity
        df_after = df.copy()
        df_after.item_quantity = df.item_quantity.astype("int64")
        self.to_csv(df_after)
