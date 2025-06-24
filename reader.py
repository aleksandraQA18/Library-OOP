import string
from random import choice, randint


class ValidationError(Exception):
    pass


class Reader:

    def __init__(self, first_name: str, last_name: str, username: str, email: str):
        self.card_no = self.generate_card_no()
        self.first_name = self.input_validation(first_name)
        self.last_name = self.input_validation(last_name)
        self.username = self.input_validation(username)
        self.email = self.email_validation(email)

    def input_validation(self, field: str) -> str:
        if len(field) < 3 or not field.strip():
            raise ValidationError(
                "First name, last name and username must be at least 3 characters long."
            )
        return field

    def email_validation(self, email: str) -> str:
        if len(email) < 3 or not email.strip():
            raise ValidationError("Email must be at least 3 characters long.")
        if "@" not in email:
            raise ValidationError('email should contain "@"')
        return email

    def generate_card_no(self) -> str:
        """
        Generates a random card number for the reader.
        Format: 4 digits + uppercase letter / uppercase letter + 2 digits (e.g., 1234A/B56)
        """
        letters = string.ascii_uppercase
        return (
            f"{randint(1000, 9999)}{choice(letters)}/{choice(letters)}{randint(10, 99)}"
        )
