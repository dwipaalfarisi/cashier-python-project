# To write the staging file
from csv import DictWriter, writer
import psycopg2
import db_variables


class ReadAndWrite:
    def __init__(self):
        self.file_path = "./transaction-staging.csv"

    # def read(self) -> None:

    #     file_path = self.file_path
    #     try:
    #         with open(file_path, "r", encoding="utf-8") as file_object:
    #             csv_reader = reader(file_object)
    #             for lines in csv_reader:
    #                 print(lines)
    #     except FileNotFoundError:
    #         print("File Not found.")
    #     except Exception:
    #         print("Unexpected error.")

    def write_header(self) -> None:
        """Write CSV header, create a new CSV file if not exists
        Usage:
            reset_transaction and create the staging file
        """
        file_path = "./transaction-staging.csv"
        header = ["item_name", "item_quantity", "item_price"]
        try:
            with open(file_path, "w+", encoding="utf-8", newline="") as file_object:
                dict_writer = DictWriter(file_object, fieldnames=header)
                dict_writer.writeheader()
        except FileNotFoundError:
            print("File Not found.")
        except Exception:
            print("Unexpected error.")

    def write_values(self, row_values: list[str, int, float]):
        """Write the transaction records
        Usage:
            add_item
        Args:
            row_values (list[str, int, float]): transaction records (item_name, item_quantity, item_price)
        """
        file_path = self.file_path
        try:
            with open(file_path, "a", encoding="utf-8", newline="") as file_object:
                writer_object = writer(file_object)  # skip header
                writer_object.writerow(row_values)
                print("Successfully write values to the staging file")
        except FileNotFoundError:
            print("File Not found.")
        except Exception:
            print("Unexpected error.")


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
            cursor = connection.cursor()
            with open(file_path, "r", encoding="utf-8") as file_object:
                next(file_object)
                cursor.copy_from(
                    file_object,
                    "transaction_history",
                    sep=",",
                    columns=["item_name", "item_quantity", "item_price"],
                )

            connection.commit()
            print("Record inserted successfully into transaction history table.")

        except (Exception, psycopg2.Error) as error:
            # try to catch a more specific exceptions
            connection.rollback()
            print("Failed to insert record into transaction history table.", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")
