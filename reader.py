import uuid


class Reader:

    def __init__(self, first_name, last_name):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        # self.books have a book object and a return date
        self.books = []

    def print_reader_books(self):
        if not self.books:
            print("You don't currently have any books on loan")
        else:
            for book in self.books:
                print(book.title)
