from colorama import Fore, Style

from library import Library
from utils import style_text, style_text_multicolor

reader = None

print(
    style_text("Welcome in our library!", Fore.BLUE, Style.BRIGHT),
    "\nEnter a number of an action from listed below:",
)

actions = [
    "To register new reader",
    "To log in ",
    "To search a book by title",
    "To search a book by author",
    "To borrow a book",
    "To return a book",
    "To print all borrowed books",
    "To print the menu",
    "To leave an application",
]


def menu(actions_list):
    for i, action in enumerate(actions_list, start=1):
        print(f"{style_text(str(i), Fore.YELLOW)} - {action}")


def library_functions():
    stop = False

    while not stop:
        library = Library()
        global reader

        try:
            action_num = int(input("Enter an action number: "))
            match action_num:
                case 1:
                    if reader is None:
                        library.register_reader()
                    else:
                        print("You are already registered")
                case 2:
                    if reader is None:
                        card_no = input("Please enter your card number: ")
                        reader = library.login(card_no)
                    else:
                        print("You are already logged in.")
                case 3:
                    title = input("Enter book's title: ")
                    library.search_book_by_title(title)
                case 4:
                    author = input("Enter book's author: ")
                    library.search_book_by_author(author)
                case 5:
                    if reader is None:
                        print("Only logged user can boorow a book.")
                    else:
                        card_no = reader["card_no"]
                        isbn = input("To borrow a book, please enter an ISBN code: ")
                        library.borrow_book(isbn, card_no)
                case 6:
                    if reader is None:
                        print("Only logged user can return a book.")
                    else:
                        has_books = library.has_reader_books(reader["card_no"])
                        if has_books:
                            library.print_reader_books(reader["card_no"])
                            isbn = input(
                                "To return a book, please enter an ISBN code: "
                            )
                            library.return_book(isbn, reader["card_no"])
                        else:
                            print("You do not have any books on your account.")
                case 7:
                    if reader is None:
                        print("Please log in to print your books.")
                    else:
                        library.print_reader_books(reader["card_no"])
                case 8:
                    menu(actions)
                case 9:
                    stop = True
                    reader = None
                    style_text_multicolor("Good Bye!")
                case _:
                    print("Enter a number from the menu")
        except ValueError as e:
            print("Please enter a valid action number!")


menu(actions)
library_functions()
