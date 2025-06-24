import pandas as pd
from colorama import Fore

from config import BOOK_STOCK
from csv_data_manager import CSVDataManager
from utils import style_text


class Catalog:

    def __init__(self):
        self.csvDataManager = CSVDataManager(BOOK_STOCK)
        self.csvDataManager.df.set_index("isbn", drop=False, inplace=True)
        self.csvDataManager.df = self.csvDataManager.df.astype({"reader": "string"})

    def get_book_by_isbn(self, isbn_code: str) -> dict | None:
        """
        Retrieve a book's details from the catalog using its ISBN code.
        Args:
            isbn_code (str): The ISBN code of the book to retrieve.
        Returns:
            dict | None: A dictionary containing the book's details if found, otherwise None.
        """
        try:
            book = self.csvDataManager.get_row_by_index(isbn_code)
            return book
        except KeyError:
            print(f"The book with the ISBN {isbn_code} was not found.")

    def get_book_status(self, book: dict) -> bool | None:
        """
        Determines the availability status of a book.
        Args:
            book (dict): A dictionary representing a book, expected to contain a "reader" key.
        Returns:
            bool | None: Returns True if the book is available (i.e., "reader" is NaN),
            False if the book is not available, or None if the status cannot be determined.
        """
        book_status = book["reader"]
        if pd.isna(book_status) or book_status == "nan":
            return True
        else:
            return False

    def display_book_status(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """
        Updates the 'reader' column of the given DataFrame to a 'status' column indicating book availability.
        The method renames the 'reader' column to 'status' and sets its value to a styled string:
        - "available" (in green) if the value is NaN (book is available)
        - "not available" (in red) otherwise (book is checked out)
        Args:
            df (pd.DataFrame): DataFrame containing book information with a 'reader' column.
        Returns:
            pd.DataFrame | None: A new DataFrame with the updated 'status' column, or None if an error occurs.
        """
        try:
            df_status = df.rename(columns={"reader": "status"}).copy()
            df_status["status"] = df_status["status"].apply(
                lambda x: (
                    style_text("available", Fore.GREEN)
                    if pd.isna(x)
                    else style_text("not available", Fore.RED)
                )
            )
            return df_status
        except KeyError:
            print("KeyError: column reader was not found")
        except AttributeError as e:
            print("AttributeError:", e)

    def search_book_by_title(self, title: str) -> pd.DataFrame | None:
        """
        Searches for books in the catalog by their title.
        Args:
            title (str): The title of the book to search for.
        Returns:
            pd.DataFrame | None: A DataFrame containing the search results with book status if matches are found,
            otherwise None.
        """
        results_df = self.csvDataManager.match_data("title", title)
        if results_df is not None:
            return self.display_book_status(results_df)

    def search_book_by_author(self, author: str) -> pd.DataFrame | None:
        """
        Searches for books by a given author.
        Args:
            author (str): The name of the author to search for.
        Returns:
            pd.DataFrame | None: A DataFrame containing the books by the specified author with their status displayed,
            or None if no books by that author are found.
        """
        results_df = self.csvDataManager.match_data("author", author)
        if results_df is not None:
            return self.display_book_status(results_df)

    def print_book_results(
        self, df: pd.DataFrame, columns=["title", "author", "isbn", "status"]
    ) -> None:
        """
        Prints the results of a DataFrame containing book information.
        Args:
            df (pd.DataFrame): The DataFrame containing book data to be printed.
            columns (list, optional): List of column names to display. Defaults to ["title", "author", "isbn", "status"].
        Returns:
            None
        """
        self.csvDataManager.print_df_results(df, columns)

    def borrow_book(self, isbn_code: str, card_no: str) -> dict | None:
        """
        Attempts to borrow a book from the catalog using its ISBN code and the reader's card number.
        Args:
            isbn_code (str): The ISBN code of the book to be borrowed.
            card_no (str): The card number of the reader borrowing the book.
        Returns:
            dict | None: The book's information as a dictionary if the book is available and successfully borrowed;
                         None if the book is not available or does not exist.
        """
        book = self.get_book_by_isbn(isbn_code)
        if book is not None:
            is_unassigned = self.get_book_status(book)
            if is_unassigned:
                self.csvDataManager.update_csv(isbn_code, "reader", card_no)
                return book
            else:
                print(f"The book with the ISBN {isbn_code} is not available.")
                return None

    def return_book(self, isbn_code: str) -> dict | None:
        """
        Returns a borrowed book to the catalog by clearing the reader information for the given ISBN code.
        Args:
            isbn_code (str): The ISBN code of the book to be returned.
        Returns:
            dict | None: The book's information as a dictionary if the book exists, otherwise None.
        """
        self.csvDataManager.update_csv(isbn_code, "reader", "")
