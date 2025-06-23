import colorama
import pandas as pd
from colorama import Back, Style

from config import READERS
from csv_data_manager import CSVDataManager
from reader import Reader
from utils import style_text


class Readers:

    def __init__(self):
        self.csvDataManager = CSVDataManager(READERS)
        self.csvDataManager.df.set_index("card_no", drop=False, inplace=True)
        colorama.init(autoreset=True)

    def register_reader(self, reader: Reader) -> Reader | None:
        """
        Registers a new reader in the system if the username does not already exist.
        Args:
            reader (Reader): The Reader object containing the reader's information.
        Returns:
            Reader | None: The registered Reader object if registration is successful,
            otherwise None if a reader with the same username already exists.
        """
        data = [
            reader.card_no,
            reader.first_name,
            reader.last_name,
            reader.username,
            reader.email,
            "",
        ]
        try:
            readers = self.csvDataManager.df
            reader_df = self.search_reader(reader.username)
            if reader_df is not None:
                if not reader_df.empty:
                    raise ValueError(
                        f"Reader with username {reader.username} already exists."
                    )
                else:
                    self.csvDataManager.df.loc[len(readers)] = data
                    self.csvDataManager.save_to_csv()
                    print(f"Reader {reader.first_name} is successfully registered.")
                    text_msg = f"Now you can log in with your card number"
                    print(
                        text_msg,
                        style_text(reader.card_no, Back.LIGHTMAGENTA_EX, Style.DIM),
                    )
                    return reader
        except Exception as e:
            print(e)

    def search_reader(self, username: str) -> pd.DataFrame | None:
        """
        Searches for a reader in the dataset by their username.
        Args:
            username (str): The username of the reader to search for.
        Returns:
            pd.DataFrame | None: A DataFrame containing the reader's information if found, otherwise None.
        """
        reader_df = self.csvDataManager.search_exact_data("username", username)
        return reader_df

    def get_reader_by_card_no(self, card_no: str) -> dict | None:
        """
        Retrieve a reader's information by their card number.
        Args:
            card_no (str): The card number of the reader to look up.
        Returns:
            dict | None: A dictionary containing the reader's information if found, otherwise None.
        """
        try:
            reader = self.csvDataManager.df.loc[[card_no]]
            return reader.to_dict("records")[0]
        except KeyError:
            print(f"Reader with card number: {card_no} does not exist")

    def get_reader_books(self, card_no: str) -> list | None:
        """
        Retrieves the list of books associated with a reader by their card number.
        Args:
            card_no (str): The card number of the reader.
        Returns:
            list | None: A list of book identifiers (as strings) if the reader exists and has books,
            an empty list if the reader has no books, or None if an error occurs.
        """
        try:
            reader_df = self.get_reader_by_card_no(card_no)
            if reader_df is None:
                raise ValueError("Reader does not exists")
            else:
                books = reader_df["books"]
                if pd.isna(books):
                    return []
                return books.split(",")
        except Exception as e:
            print("An error occured: ", e)

    def assign_book(self, isbn_code, card_no: str) -> str | None:
        """
        Assigns a book to a reader by their card number and updates the CSV data.
        Args:
            isbn_code (str): The ISBN code of the book to assign.
            card_no (str): The card number of the reader.
        Returns:
            str | None: The updated list of assigned book ISBNs as a comma-separated string,
            or None if the reader had no books previously.
        """
        reader_books = self.get_reader_books(card_no)
        if reader_books is None:
            self.csvDataManager.update_csv(card_no, "books", isbn_code)
            return reader_books
        else:
            reader_books.append(isbn_code)
            reader_books = ",".join(reader_books)
            self.csvDataManager.update_csv(card_no, "books", reader_books)
            return reader_books

    def unassign_book(self, isbn_code, card_no: str) -> list | None:
        """
        Unassigns a book from a reader's list of borrowed books based on the provided ISBN code and reader's card number.
        Args:
            isbn_code (str): The ISBN code of the book to be unassigned.
            card_no (str): The card number of the reader.
        Returns:
            list | None: The updated list of the reader's borrowed books if the book was successfully unassigned,
            or None if the reader has no books or the specified book is not assigned to the reader.
        """
        reader_books = self.get_reader_books(card_no)
        if reader_books is None or len(reader_books) == 0:
            return None
        elif isbn_code in reader_books:
            return_book = reader_books.index(isbn_code)
            reader_books.pop(return_book)
            self.csvDataManager.update_csv(card_no, "books", ",".join(reader_books))
            return reader_books
        else:
            return None
