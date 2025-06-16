from csvDataManager import CSVDataManager


class Readers:

    READERS_DB_FILE = "readers.csv"

    def __init__(self):
        self.csvDataManager = CSVDataManager(self.READERS_DB_FILE)
        self.csvDataManager.df.set_index("id", drop=False, inplace=True)

    def register_reader(self, reader):
        data = [reader.id, reader.first_name, reader.last_name, reader.books]
        readers = self.csvDataManager.df
        readers.loc[len(readers)] = data
        self.csvDataManager.save_to_csv()

    def search_user(self, first_name, last_name):
        results_df = self.csvDataManager.search_data("first_name", first_name)
        results_dict = results_df.to_dict("records")
        print(tabulate(results_dict, headers="keys", tablefmt="pretty"))

    def assign_book(self, reader, isbn_code):
        reader_row = self.csvDataManager.get_row_by_index(reader.id)
        print(self.csvDataManager.df.index)
        if reader_row is None:
            print("Reader not found")
            return
        reader_books = self.csvDataManager.df.loc[reader_row, "books"]
        print(type(reader_books))
        print(reader_books)
        update_books = reader_books
        self.csvDataManager.update_cell(reader.id, "books", isbn_code)
