# Exit the app using main_menu with input 11
from sys import exit as exit_application
from transaction import Transaction, Choice
from database import ReadAndWrite, SendToDatabasePostgreSQL


def create_transaction() -> Transaction:
    """Instantiate Transaction class

    Returns:
        Transaction object
    """
    transact_id = Transaction()
    return transact_id


def create_choice() -> Choice:
    """Instantiate Choice class

    Returns:
        Choice object
    """
    choice = Choice()
    return choice


def confirm_payment(database: SendToDatabasePostgreSQL) -> None:
    """Confirm transaction by user and load the staging file to PostgreSQL

    Args:
        database (SendToDatabasePostgreSQL): Instantiate the class to access csv_to_postgresql method
    """
    print("Confirm transaction?")
    choice = input("Enter 'y' to confirm or 'n' to cancel: ")

    # validate user input
    # Check if the user's input is valid
    if choice.lower() not in ("y", "n"):
        # If the input is invalid, display an error message and call the function again
        print("Invalid input. Please try again.")
        confirm_payment(database)
    elif choice.lower() == "y":
        # If the input is 'y', load the staging file to PostgreSQL
        database.csv_to_postgresql()
    else:
        # If the input is 'n', return to the main menu
        main_menu()


def main_menu() -> None:
    """Control the user flow"""

    transact_123 = create_transaction()

    print("-" * 20)
    print("SELF SERVICE CASHIER")
    print("-" * 20)
    print(
        """
    1. Add New Item
    2. Update Item Name
    3. Update Item Quantity
    4. Update Item Price
    5. Remove an Item
    6. Reset Transaction
    7. Check Order
    8. Total Price
    9. Confirm Transaction
    10. Exit
        """
    )
    print("-" * 20)

    select = str(input("Enter task No. : "))
    if not select.isdigit() or not 1 <= int(select) <= 10:
        print("Wrong input. Try 1-10.\n")
        main_menu()

    # Define a dictionary with menu options as keys and functions as values
    menu_options = {
        "1": transact_123.add_item,
        "2": transact_123.update_name,
        "3": transact_123.update_quantity,
        "4": transact_123.update_price,
        "5": transact_123.remove_item,
        "6": transact_123.reset_transaction,
        "7": transact_123.check_order,
        "8": transact_123.total_price,
        "9": confirm_payment,
    }

    # Use the `get` method to get the function associated with the selected menu option
    selected_function = menu_options.get(select)

    # Check for special cases where the selected function is not in the menu_options dictionary
    # not included in the menu_options cause we need to reset the transaction before closing the app
    if select == "10":
        transact_123.reset_transaction(ReadAndWrite())
        exit_application()
    elif not selected_function:
        print("Invalid menu option. Please try again.")

    # Call the selected function if it exists, passing any necessary arguments
    else:
        if select in ("1"):
            # Menu option 1 requires the ReadAndWrite and Choice classes as parameters
            selected_function(ReadAndWrite(), Choice())
            main_menu()
        elif select in ("6"):
            # Menu options 6 requires the ReadAndWrite class as a parameter
            selected_function(ReadAndWrite())
            main_menu()
        elif select in ("7", "8"):
            selected_function()
            main_menu()
        elif select == "9":
            # Menu option 9 requires the SendToDatabasePostgreSQL class as a parameter
            selected_function(SendToDatabasePostgreSQL())
            main_menu()
        else:
            # All other menu options require the Choice class as a parameter
            selected_function(Choice())
            main_menu()


def main() -> None:
    """Call main_menu function"""
    main_menu()


if __name__ == "__main__":
    main()
