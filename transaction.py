from typing import Type, Any
import pandas as pd
from database import ReadAndWrite


class Choice:
    """A class related to user input"""

    def get_user_input(self, data_type: Type, prompt: str) -> Any:
        """Get user input and validate it

        Args:
            data_type (type): expected data type for the input

        Returns:
            any: user input of the specified data type
        """
        # Repeatedly prompt the user for input until they enter a value of the specified data type
        while True:
            # Get user input
            user_input = input(prompt)

            # Try to convert the user input to the specified data type
            try:
                user_input = data_type(user_input)
            # If the conversion fails, it means the input is not valid for the specified data type
            except ValueError:
                print(f"Wrong input. Please enter a valid {data_type.__name__}.")
            # If the conversion succeeds, return the converted value
            else:
                return user_input

    def get_product_name(self) -> str:
        """Get product name from user

        Returns:
            str: name of the product
        """
        return self.get_user_input(str, "Item Name: ")

    def get_product_quantity(self) -> int:
        """Get product quantity from user

        Returns:
            int: quantity of the product
        """
        return self.get_user_input(int, "Quantity: ")

    def get_product_price(self) -> float:
        """Get product price from user

        Returns:
            float: price of the product
        """
        return self.get_user_input(float, "Item Price: ")

    def choice_add_item(self) -> list[str, int, float]:
        """Get information about a product to be added

        Returns:
            list[str, int, float]: a list containing the product name, quantity, and price
        """
        name = self.get_product_name()
        quantity = self.get_product_quantity()
        price = self.get_product_price()
        return [name, quantity, price]

    def choice_update_item_name(self) -> list[str, str]:
        """Get the existing product name and the new product name

        Returns:
            list[str, str]: a list containing the existing product name and the new product name
        """
        name = self.get_product_name()
        new_name = self.get_product_name()
        return [name, new_name]

    def choice_update_item_quantity(self) -> list[str, int]:
        """Get the existing product name and the new product quantity

        Returns:
            list[str, int]: a list containing the existing product name and the new product quantity
        """
        name = self.get_product_name()
        new_quantity = self.get_product_quantity()
        return [name, new_quantity]

    def choice_update_item_price(self) -> list[str, float]:
        """Get the existing product name and the new product price

        Returns:
            list[str, float]: a list containing the existing product name and the new product price
        """
        name = self.get_product_name()
        new_price = self.get_product_price()
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
        try:
            df = pd.read_csv(
                self.file_path,
                encoding="utf-8",
                dtype={
                    "transaction_id": int,
                    "item_name": str,
                    "quantity": int,
                    "price": float,
                },
            )
            return df
        except FileNotFoundError:
            print(
                "The staging file was not found. Please check that the file exists and is in the correct location."
            )

        except IOError as error:
            print("Error.", error)
            return
        except UnicodeDecodeError as error:
            print("Error.", error)
            return
        except Exception as error:
            print("Error", error)
            return

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

        # check if the name is already in the staging file
        return df.item_name.eq(name).any()

    def product_not_exists(self, name: str) -> bool:
        """Check if the name of a product not in the staging file
        Usage:
            add_item
        Args:
            name (str): item name

        Returns:
            bool: True if the product name not in the staging file, False otherwise
        """
        # check if the name is not already in the staging file
        return not self.product_exists(name)

    def add_item(
        self, read_and_write: ReadAndWrite, choice: Choice, transaction_id
    ) -> None:
        """Add item to the staging file

        Args:
            read_and_write (ReadAndWrite): Instantiate ReadAndWrite class to access write_values (adding new items to the staging file)
            choice (Choice): Instantiate Choice class to access choice_add_item (user transaction input)
        """
        item = choice.choice_add_item()
        item.insert(0, transaction_id)
        product_not_exists = self.product_not_exists(item[0])
        if product_not_exists:
            read_and_write.write_values(item)
            print("Added")
        else:
            print("No changes made. The item is already exist.")

    def check_product_list(self, df: pd.DataFrame) -> bool:
        """Check if the staging file is not empty

        Returns:
            bool: True if the staging file is not empty, False otherwise
        """
        return df.item_name.notnull().any()

    def check_order(self) -> None:
        """Show the transaction order to the user by reading the staging file"""
        df = self.read_csv()
        not_empty = self.check_product_list(df)
        if not_empty:
            # import and drop nulls
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
            # no discount
            discount_percent = 1
            print("No Discount")
        elif 200_000 < total <= 300_000:
            # 5% discount
            discount_percent = 0.95
            print("Discount 5%")
        elif 300_000 < total <= 500_000:
            # 8% discount
            discount_percent = 0.92
            print("Discount 8%")
        elif total > 500_000:
            # 10% discount
            discount_percent = 0.90
            print("Discount 10%")
        else:
            discount_percent = 0

        return discount_percent

    def total_price(self) -> None:
        """Show the total price to the user"""
        df = self.read_csv()
        not_empty = self.check_product_list(df)
        if not_empty:
            # import and drop nulls
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
        # get the item name from the user using the Choice object
        name = choice.get_user_input(str, "Item name to be removed: ")
        # read the transaction table from the staging file
        df = self.read_csv()
        # check if the transaction table is empty
        if df.shape[0] == 0:
            print("The transaction table is empty. There are no items to remove.")
            return

        # check if the item name exists in the transaction table
        if self.product_not_exists(name):
            print(f"Item '{name}' does not exist in the transaction table.")
            return
        # create a new DataFrame with the rows that do not have the item name being removed
        df_after = df[df["item_name"] != name]
        # save the updated transaction table to the staging file
        self.to_csv(df_after)
        print("Successfully removed.")

    def reset_transaction(self, read_and_write: ReadAndWrite) -> None:
        """Delete all records from the staging file

        Args:
            read_and_write (ReadAndWrite): instantiate ReadAndWrite to access write_header (rewrite the file)
        """
        read_and_write.write_header()

    def update_value(self, col_name: str, value_list: Any) -> pd.DataFrame:
        # Check if the value_type parameter is a valid value
        if col_name in ("item_name", "item_quantity", "item_price"):
            # Use the first element of the value_list parameter as the name of the item to update
            name = value_list[0]
            # Use the second element of the value_list parameter as the new value for the item
            new_value = value_list[1]
        else:
            print("Invalid value_type. Please specify 'name', 'quantity', or 'price'.")
            return

        df = self.read_csv()
        # Use the .eq() method to compare the name variable with the values in the "item_name" column
        df.loc[df.item_name.eq(name), col_name] = new_value
        self.to_csv(df)

    def update_name(self, choice: Choice) -> None:
        """Update the name of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class to access choice_update_item_name (user transaction input)
        """
        df = self.read_csv()
        value_list = choice.choice_update_item_name()

        not_empty = self.check_product_list(df)
        product_exists = self.product_exists(value_list[0])

        if not_empty and product_exists:
            self.update_value("item_name", value_list)
            print("Successfully updated")
        else:
            print("Item not found. Try to add it first.")

    def update_quantity(self, choice: Choice) -> None:
        """Update the quantity of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class to access choice_update_item_quantity (user transaction input)
        """
        df = self.read_csv()
        value_list = choice.choice_update_item_quantity()

        not_empty = self.check_product_list(df)
        product_exists = self.product_exists(value_list[0])

        if not_empty and product_exists:
            self.update_value("item_quantity", value_list)
            print("Successfully updated")
        else:
            print("Item not found. Try to add it first.")

    def update_price(self, choice: Choice) -> None:
        """Update the price of an item in the staging file

        Args:
            choice (Choice): Instantiate Choice class
            to access choice_update_item_price (user transaction input)
        """
        df = self.read_csv()
        value_list = choice.choice_update_item_price()

        not_empty = self.check_product_list(df)
        product_exists = self.product_exists(value_list[0])

        if not_empty and product_exists:
            self.update_value("item_price", value_list)
            print("Successfully updated")
        else:
            print("Item not found. Try to add it first.")

    def drop_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop null values from the staging file
        Usage:

        Args:
            df (pd.DataFrame): transaction table
        """
        return df.dropna()
