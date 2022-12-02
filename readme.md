The code defines three classes: `Choice`, `Transaction`, and `ReadAndWrite`.

### transaction.py
#### Choice class
The `Choice` class is a utility class that provides methods for getting user input and validating it. The `Choice` class has several methods that allow the user to enter different types of input, such as a string, integer, or float. These methods ensure that the input is of the correct data type and handle any errors that may occur during the conversion process.

The `Choice` class also has several methods for specific types of user input, such as product names, quantities, and prices. These methods provide a more user-friendly interface for entering these values, by prompting the user for the specific type of input and handling any errors that may occur.

In summary, the `Choice` class provides a convenient and user-friendly way of getting and validating user input for the transaction management system.

The `Choice` class defines methods for prompting the user for input and returning the input as a specific data type. These methods include:

- `get_user_input(self, data_type: Type, prompt: str) -> Any`: This method prompts the user for input and validates that the input is of the specified data type. If the input is not valid, the method displays an error message and prompts the user for input again.

- `get_product_name(self) -> str`: This method prompts the user for a product name and returns the user's input as a string.

- `get_product_quantity(self) -> int`: This method prompts the user for a product quantity and returns the user's input as an integer.

- `get_product_price(self) -> float`: This method prompts the user for a product price and returns the user's input as a float.

- `choice_add_item(self) -> list[str, int, float]`: This method prompts the user for a product name, quantity, and price, and returns a list containing the user's input for each of these values.

- `choice_update_item_name(self) -> list[str, str]`: This method prompts the user for a product name and a new product name, and returns a list containing the user's input for each of these values.

- `choice_update_item_quantity(self) -> list[str, int]`: This method prompts the user for a product name and a new product quantity, and returns a list containing the user's input for each of these values.

- `choice_update_item_price(self) -> list[str, float]`: This method prompts the user for a product name and a new price, and returns a list containing the user's input for each of these values.
- 

The Transaction class contains methods that are related to a transaction. This class has the following attributes:

- `file_path`: This is the file path for the transaction file. It is used by the methods that refer to the transaction file.
The Transaction class has the following methods:

- `__init__(self)`: This is the constructor method that is called when a Transaction object is instantiated. It sets the `file_path` attribute to the path of the transaction file.

#### Helper Methods:
There are several helper methods in the Transaction class. These methods perform specific tasks that are used by other methods in the class. These helper methods are used by other methods in the Transaction class to perform specific tasks related to transactions, such as checking for the existence of a product, reading the transaction from a file, or exporting the transaction to a file. Some examples of helper methods in the Transaction class are:

- `read_csv(self) -> pd.DataFrame`: This method reads the transaction file and returns the transaction data as a Pandas DataFrame object.

- `to_csv(self, df: pd.DataFrame)` -> None: This method exports the transaction data to the transaction file as a CSV. It takes a Pandas DataFrame object containing the transaction data as a parameter and saves the data to the transaction file.

- `product_exists(self, name: str) -> bool`: This method checks whether a product with a given name exists in a transaction. It takes a single argument, the name of the product, and returns a boolean value indicating whether the product exists in the transaction. The method first reads the transaction from the CSV file using the `read_csv` method. It then checks if the product exists in the transaction by checking if its name is in the list of item names in the transaction. If the product exists, the method returns `True`, otherwise it returns `False`.

- `product_not_exists(self, name: str) -> bool`: This method checks whether a product with a given name does not exist in a transaction. It takes a single argument, the name of the product, and returns a boolean value indicating whether the product does not exist in the transaction. The method uses the product_exists method to check if the product exists in the transaction. If the product exists, the method returns `False`, otherwise it returns `True`.

- `check_product_list(self, df: pd.DataFrame) -> bool`: This method takes a dataframe containing transaction data as input and checks whether the dataframe is empty. It does this by using the df.item_name.notnull().any() method to check if the item_name column of the dataframe contains any non-null values. If the item_name column contains any non-null values, the check_product_list method returns True, indicating that the transaction data is not empty and contains at least one item. If the item_name column contains only null values, the check_product_list method returns False, indicating that the transaction data is empty and does not contain any items.

- `drop_nulls(self, df: pd.DataFrame) -> pd.DataFrame`: This method takes a dataframe containing transaction data as input and removes all null values from the dataframe. The drop_nulls method iterates through the rows and columns of the dataframe, and it removes any rows or columns that contain null values. After removing all null values from the dataframe, the drop_nulls method returns the modified dataframe without any null values. This modified dataframe can then be used in other methods to perform calculations on the transaction data without having to worry about null values. The drop_nulls method is typically used to ensure that calculations are performed accurately and reliably on the transaction data.

- `update_name(self, read_and_write: ReadAndWrite, choice: Choice) -> None`: This method updates the name of an existing item in the transaction. It prompts the user for the current product name and the new product name, and then passes these values to the `choice.choice_update_item_name` method to get the user's input. It then updates the item's name in the transaction file using the `update_value` method.

- `update_quantity(self, read_and_write: ReadAndWrite, choice: Choice) -> None`: This method updates the quantity of an existing item in the transaction. It prompts the user for the product name and the new quantity, and then passes these values to the choice.choice_update_item_quantity method to get the user's input. It then updates the item's quantity in the transaction file using the read_and_write.update_item_quantity method.

- `update_price(self, read_and_write: ReadAndWrite, choice: Choice) -> None`: This method updates the price of an existing item in the transaction. It prompts the user for the product name and the new price, and then passes these values to the `choice.choice_update_item_price` method to get the user's input. It then updates the item's price.

- `check_order(self) -> None`: This method prints the current transaction to the user. It uses the self.read_csv method to read the transaction file and then prints the contents of the file to the user.
  
- `reset_transaction(self, read_and_write: ReadAndWrite) -> None`: This method resets the transaction by removing all items from the transaction file. It uses the read_and_write.reset_transaction method to reset the transaction.

- `discount(self, total_payment: float) -> float`: The discount method is a function that takes a total price as input and returns a discount rate based on the value of the total price. The discount method compares the total price to a set of predetermined ranges, and it returns a different discount rate depending on which range the total price falls into. For example, if the total price is greater than 200,000 and less than or equal to 300,000, the discount method will return a discount rate of 0.95, indicating that a discount of 5% should be applied.

- `total_price(self) -> None`: This method calculates the total price of the current transaction. It uses the self.read_csv method to read the transaction file and then calculates the total price of all items in the transaction. It then prints the total price to the user.

#### Primary Methods
The primary methods in the Transaction class are the methods that define the core functionality of the class. These methods are the main methods that allow you to perform actions related to transactions, such as adding, updating, or removing items from a transaction. Some examples of primary methods in the Transaction class are:

- `add_item(self, read_and_write: ReadAndWrite, choice: Choice) -> None`: This method adds a new item to the transaction. It prompts the user for the product name, quantity, and price, and then passes these values to the `choice.choice_add_item` method to get the user's input. It then adds the item to the transaction file using the `read_and_write.write_values` method.

- `update_value(self, col_name: str, value_list: Any) -> pd.DataFrame`: This method allows you to update a value in a transaction. It takes three arguments: the name of the item to be updated, the name of the column to be updated, and the new value for the column. It then updates the value in the transaction and returns the updated transaction. This is used to replace the new values in `update_name`, `update_quantity`, and `update_price`.  

- `remove_item(self, choice: Choice) -> None`: This method removes an item from the transaction. It prompts the user for the product name and then uses the `choice.get_product_name` method to get the user's input. It then removes the item from the transaction file using the `remove_item` method.  


The `ReadAndWrite` class defines methods for reading and writing CSV files. These methods include:

- `write_header`: writes a header row to a CSV file. This method is used to create a new CSV file if one does not already exist.
- `write_values`: writes one or more rows of data to a CSV file. This method is used to add new items to the transaction.
The code also defines a main_menu function, which provides the user with a menu of options for managing transactions. The user can choose from the following options:

1. Add a new item
2. Update an item's name
3. Update an item's quantity
4. Update an item's price
5. Remove an item
6. Reset the transaction
7. Check the order
8. Calculate the total price
9. Confirm the transaction
10. Exit the application
    
Each menu option corresponds to a specific method from the `Transaction` or `ReadAndWrite` classes. When the user selects a menu option, the corresponding method is called and the results are displayed to the user.

The code also defines a `confirm_payment` function, which prompts the user to confirm the transaction and then loads the transaction data from the CSV file into a PostgreSQL database.

To use the code, you will need to create a `db_variables.py` file that contains the following variables:
```
USER = "<your_user_name>"
PASSWORD = "<your_password>"
HOST = "<your_host>"
PORT = "<your_port>"
DATABASE = "<your_database>"
```

You will also need to install the required Python packages: `pandas`, `psycopg2`. To do this, run the following command:
```
pip install pandas psycopg2 db_variables
```
### main.py
The `main.py` file is the entry point for the application. It defines the `main_menu` function, which provides a menu of options for managing transactions. When the user selects an option, the `main_menu` function calls the corresponding method from the Transaction or ReadAndWrite classes to perform the desired action.

The `main_menu` function also handles user input validation and error handling. For example, if the user enters an invalid menu option, the function will display an error message and prompt the user to try again.

The `main_menu` function also contains the logic for calling the confirm_payment function, which prompts the user to confirm the transaction and then loads the transaction data from the CSV file into a PostgreSQL database.

In order to run the `main.py` file, you will need to have the required Python packages installed and have created the db_variables.py file. You can install the required packages using the pip install -r requirements.txt command, where requirements.txt is a file containing a list of the required packages.

Once you have installed the required packages and created the `db_variables.py` file, you can run the code by calling the `main_menu` function from the terminal in the directory where the `main.py` file is located. To do this, enter the following command:

You can run the `main.py` file by calling the `python main.py` command in the terminal. This will execute the `main_menu` function and display the menu of options for managing transactions. You can then follow the prompts to select an option and perform the corresponding action.

Alternatively, you can also run the code by calling the `main_menu` function directly from the terminal. To do this, open the terminal in the directory where the `main.py` file is located, and enter the following command:
```
python -c "from main import main_menu; main_menu()"
```
This will execute the `main_menu` function and display the menu of options for managing transactions. You can then follow the prompts to select an option and perform the corresponding action.
