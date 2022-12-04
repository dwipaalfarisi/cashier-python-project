# To write the staging file
from csv import DictWriter, writer
import psycopg2
import db_variables


class ReadAndWrite:
    """A class for reading, writing header, and values to the staging file."""

    def __init__(self):
        self.file_path = "./transaction-staging.csv"

    def write_header(self) -> None:
        """Write CSV header, create a new CSV file if not exists
        Usage:
            reset_transaction and create the staging file
        """
        file_path = self.file_path
        header = ["transaction_id", "item_name", "item_quantity", "item_price"]
        try:
            with open(file_path, "w+", encoding="utf-8", newline="") as file_object:
                dict_writer = DictWriter(file_object, fieldnames=header)
                dict_writer.writeheader()
        except FileNotFoundError:
            print("The file was not found. Please check the file path and try again.")
        except PermissionError:
            print(
                "You do not have permission to write to the file. Please check your permissions and try again."
            )
        except Exception as error:
            print(f"An unexpected error occurred: {error}")

    def write_values(self, row_values: list[int, str, int, float]):
        """Write the transaction records
        Usage:
            add_item
        Args:
            row_values (list[int, str, int, float]): transaction records (transaction_history, item_name, item_quantity, item_price)
        """
        file_path = self.file_path
        try:
            with open(file_path, "a", encoding="utf-8", newline="") as file_object:
                writer_object = writer(file_object)  # skip header
                writer_object.writerow(row_values)
                print("Successfully write values to the staging file")
        except FileNotFoundError:
            print("The file was not found. Please check the file path and try again.")
        except PermissionError:
            print(
                "You do not have permission to write to the file. Please check your permissions and try again."
            )
        except Exception as error:
            print(f"An unexpected error occurred: {error}")


class SendToDatabasePostgreSQL:
    """A class for PostgreSQL adapter: loading staging file cotaining records to PostgreSQL"""

    def __init__(self):
        self.file_path = "./transaction-staging.csv"

    def csv_to_postgresql(self) -> None:
        """
        Load data from staging table to the database (postgresql)
        """

        try:
            file_path = self.file_path
            # secret this
            connection = psycopg2.connect(
                user=db_variables.USER,
                password=db_variables.PASSWORD,
                host=db_variables.HOST,
                port=db_variables.PORT,
                database=db_variables.DATABASE,
            )

        except psycopg2.Error as error:
            print("Failed to establish connection to the database", error)
            return

        try:
            cursor = connection.cursor()

        except psycopg2.Error as error:
            print("Failed to create cursor:", error)
            connection.close()
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file_object:
                next(file_object)
                cursor.copy_from(
                    file_object,
                    "transaction_history",
                    sep=",",
                    columns=[
                        "transaction_id",
                        "item_name",
                        "item_quantity",
                        "item_price",
                    ],
                )

            connection.commit()
            print("Record inserted successfully into transaction history table.")

        except FileNotFoundError as error:
            print("The File was not found:", error)
            connection.rollback()
            return

        except psycopg2.DataError as error:
            print("The data in the file is not in the expected format:", error)
            connection.rollback()
            return

        except psycopg2.Error as error:
            # try to catch a more specific exceptions
            connection.rollback()
            print("Failed to insert record into transaction history table.", error)
            return

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")
