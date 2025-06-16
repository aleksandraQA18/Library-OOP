from catalog import Catalog


class Library:
    def __init__(self):
        self.catalog = Catalog()

    def print_all_books(self):
        self.catalog.print_book_data()

    def search_book_by_title(self, title):
        self.search_book_by_title(title)

    def search_book_by_author(self, author):
        self.search_book_by_title(author)

    def borrow_book(self, isbn_code, reader):
        self.borrow_book(isbn_code, reader.id)

    def return_book(self, isbn_code):
        self.return_book(isbn_code)
