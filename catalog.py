import pandas as pd
from tabulate import tabulate

from csvDataManager import CSVDataManager


class Catalog:

    BOOK_STOCK_FILE = "book_stock.csv"

    def __init__(self):
        self.csvDataManager = CSVDataManager(self.BOOK_STOCK_FILE)
        self.csvDataManager.df.set_index("isbn", drop=False, inplace=True)

    def print_book_data(self, columns=["title", "author", "release_year", "pages"]):
        return self.csvDataManager.print_df_data(columns)

    def get_book_by_isbn(self, isbn_code):
        return self.csvDataManager.get_row_by_index(isbn_code)

    def print_book_info(self, isbn_code, columns=["title", "author", "reader"]):
        book_data = self.csvDataManager.get_all_data_by_index(isbn_code)
        if book_data is not None:
            book_dict = book_data[columns].to_dict("records")
            print(tabulate(book_dict, headers="keys", tablefmt="pretty"))
        else:
            print("🔴 Book not found.")

    def search_book_by_title(self, title):
        results_df = self.csvDataManager.search_data("title", title)
        results_dict = results_df.to_dict("records")
        print(tabulate(results_dict, headers="keys", tablefmt="pretty"))

    def search_book_by_author(self, author):
        results_df = self.csvDataManager.search_data("author", author)
        results_dict = results_df.to_dict("records")
        print(tabulate(results_dict, headers="keys", tablefmt="pretty"))

    def borrow_book(self, isbn_code, reader_id):
        book = self.get_book_by_isbn(isbn_code)
        if book is None:
            print("🔴 Book not found.")
            return
        is_unassigned = book[["reader"]].isnull().all()
        if is_unassigned:
            self.csvDataManager.update_cell(isbn_code, "reader", reader_id)
            self.csvDataManager.save_to_csv()
            print("🎉 A book is successfully borrowed")
            self.print_book_info(isbn_code)
        else:
            print("🔴 A book is not available right now.")

    def return_book(self, isbn_code):
        book = self.get_book_by_isbn(isbn_code)
        if book is None:
            print("🔴 Book not found.")
            return
        self.csvDataManager.update_cell(isbn_code, "reader", "")
        self.csvDataManager.save_to_csv()
        print("🎉 A book is successfully returned")
        self.print_book_info(isbn_code)
