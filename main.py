from library import Library
from reader import Reader
from readers_db import Readers

library = Library()
# library.print_all_books()

reader_db = Readers()

ola = Reader("Ola", "Test")
# reader_db.register_reader(ola)
print(ola.id)
reader_db.assign_book(ola, "12456")
