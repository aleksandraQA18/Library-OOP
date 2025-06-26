# Bookshop OOP Library System

A simple object-oriented Python application for managing a library system.  
It allows users to register, log in, search for books, borrow and return books, and view their borrowed books.  
The system uses classes for library management, readers, and catalog, and supports basic error handling and user interaction.

## Features

- **Reader Registration & Login**  
  Register new readers and log in using a unique card number.

- **Book Search**  
  Search for books by title or author.

- **Borrow & Return Books**  
  Borrow books using ISBN codes and return them when finished.

- **View Borrowed Books**  
  Display a list of books currently borrowed by a reader.

- **Error Handling**  
  Handles invalid input and provides user-friendly messages.

## Technologies

- Python 3.x
- [colorama](https://pypi.org/project/colorama/) (for colored terminal output)
- pandas

## Project Structure

```
bookshop-oop/
│
├── library.py      # Main library management logic
├── catalog.py      # Book catalog management
├── reader.py       # Reader class and validation
├── readers.py      # Readers collection management
├── utils.py        # Utility functions (e.g., text styling)
└── ...
```

## Getting Started

1. **Clone the repository**

   ```sh
   git clone https://github.com/aleksandraQA18/Library-OOP.git
   cd Library-OOP
   ```

2. **Install dependencies**

   ```sh
   pip install colorama pandas
   ```

3. **Run the application**
   ```sh
   python main.py
   ```

## Example Usage

- Register as a new reader
- Log in with your card number
- Search for books by title or author
- Borrow a book using its ISBN code
- Return a borrowed book
- View your currently borrowed books

\*This project is for educational purposes and demonstrates basic OOP and library management concepts
