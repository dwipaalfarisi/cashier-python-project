# Exit the app using main_menu with input 11
from sys import exit as close_app
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
    choice = str(input("(y/n): "))
    if choice.lower() == "y":
        database.csv_to_postgresql()
    elif choice.lower() == "n":
        main_menu()
    else:
        print("Wrong input.")
        main_menu()


def main_menu() -> None:
    """Control the user flow"""

    transact_123 = create_transaction()
    choices = create_choice()

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

    try:
        if select == "1":
            print("No 1 selected")
            transact_123.add_item(ReadAndWrite(), Choice())

        elif select == "2":
            print("No 2 selected")
            transact_123.update_name(Choice())

        elif select == "3":
            print("No 3 selected")
            transact_123.update_quantity(Choice())

        elif select == "4":
            print("No 4 selected")
            transact_123.update_price(Choice())

        elif select == "5":
            print("No 5 selected")
            transact_123.remove_item(choice=Choice())

        elif select == "6":
            print("No 6 selected")
            transact_123.reset_transaction(ReadAndWrite())

        elif select == "7":
            print("No 7 selected")
            transact_123.check_order()

        elif select == "8":
            transact_123.total_price()
            print("No 8 selected")

        elif select == "9":
            print("No 9 selected")
            confirm_payment(SendToDatabasePostgreSQL())
            print("Confirmed.")

        elif select == "10":
            transact_123.reset_transaction(ReadAndWrite())
            print("Bye.")
            close_app()

        else:
            print("Wrong input. Try 1-10.\n")
            main_menu()

        main_menu()
    except ValueError:
        print("Wrong input. Try 1-10.\n")
        main_menu()
    except Exception:
        print("Unexpected error. It's us, not you.\n")
        main_menu()


def main() -> None:
    """Call main_menu function"""
    main_menu()


if __name__ == "__main__":
    main()
