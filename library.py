import colorama
from colorama import Fore

from catalog import Catalog
from reader import Reader, ValidationError
from readers import Readers
from utils import style_text


class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.readers = Readers()
        colorama.init(autoreset=True)

    def register_reader(self) -> Reader | None:
        """
        Registers a new reader by prompting the user for personal information.
        Prompts the user to enter their first name, last name, username, and email address.
        Attempts to create a Reader instance with the provided information and registers the reader.
        If the input data is invalid and raises a ValidationError, the error is printed and None is returned.
        Returns:
            Reader | None: The registered Reader object if successful, otherwise None.
        """

        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        username = input("Enter your username: ")
        email = input("Enter your email: ")
        try:
            reader = Reader(first_name, last_name, username, email)
            self.readers.register_reader(reader)
            return reader
        except ValidationError as e:
            print(e)

    def login(self, card_no: str) -> dict | None:
        """
        Logs in a reader using their card number.
        Args:
            card_no (str): The card number of the reader attempting to log in.
        Returns:
            dict | None: The reader's information as a dictionary if the card number is found.
                         Returns an empty dictionary if the card number is not found.
        """
        reader_df = self.readers.get_reader_by_card_no(card_no)
        if reader_df is not None:
            print(f"Hello, {reader_df['first_name']}! You are logged in.")
            return reader_df
        else:
            return None

    def search_book_by_title(self, title: str) -> None:
        """
        Searches for books in the catalog by their title and prints the results.
        Args:
            title (str): The title of the book to search for.
        Returns:
            None
        """

        try:
            results_df = self.catalog.search_book_by_title(title)
            if results_df is not None:
                if results_df.empty:
                    raise KeyError(f"The book with title '{title}' was not found")
                else:
                    self.catalog.print_book_results(results_df)
        except Exception as e:
            print(e)

    def search_book_by_author(self, author: str) -> None:
        """
        Searches for books in the catalog by a given author and prints the results.
        Args:
            author (str): The name of the author to search for.
        Returns:
            None
        """

        try:
            results_df = self.catalog.search_book_by_author(author)
            if results_df is not None:
                if results_df.empty:
                    raise KeyError(f"The book with author {author} was not found")
                else:
                    self.catalog.print_book_results(results_df)
        except Exception as e:
            print(e)

    def borrow_book(self, isbn_code: str, card_no: str) -> None:
        """
        Allows a reader to borrow a book from the library using the book's ISBN code and the reader's card number.
        Args:
            isbn_code (str): The ISBN code of the book to be borrowed.
            card_no (str): The card number of the reader borrowing the book.
        Returns:
            None
        """
        book = self.catalog.borrow_book(isbn_code, card_no)
        if book is not None:
            self.readers.assign_book(isbn_code, card_no)
            print(f"The book '{book['title']}' is successfully borrowed.")

    def return_book(self, isbn_code: str, card_no: str) -> None:
        """
        Handles the process of returning a book to the library.
        Args:
            isbn_code (str): The ISBN code of the book to be returned.
            card_no (str): The library card number of the reader returning the book.
        Returns:
            None
        """
        readers_books = self.readers.get_reader_books(card_no)
        if readers_books is None or len(readers_books) == 0:
            print("You do not have any books on your account.")
        elif isbn_code in readers_books:
            self.readers.unassign_book(isbn_code, card_no)
            self.catalog.return_book(isbn_code)
            print(f"The book with the ISBN {isbn_code} was successfully returned.")
        else:
            print(f"The book was not found. Check the ISBN code.")

    def print_reader_books(self, card_no: str) -> None:
        """
        Prints the list of books currently borrowed by a reader identified by their card number.
        Args:
            card_no (str): The unique card number of the reader.
        Returns:
            None
        """

        reader_books = self.readers.get_reader_books(card_no)
        if reader_books is None or len(reader_books) == 0:
            print("You do not have any borrowed books.")
        else:
            for book in reader_books:
                book_dict = self.catalog.get_book_by_isbn(book)
                if book_dict is not None:
                    text_msg = f"- title: {book_dict['title']}, ISBN: {book_dict['isbn']}"
                    print(style_text(text_msg, Fore.GREEN))
