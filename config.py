import os

from dotenv import load_dotenv

load_dotenv()

BOOK_STOCK = os.getenv("BOOK_STOCK")
READERS = os.getenv("READERS")

if BOOK_STOCK is None:
    raise ValueError("BOOK_STOCK environment variable is not set.")
if READERS is None:
    raise ValueError("READERS environment variable is not set.")
