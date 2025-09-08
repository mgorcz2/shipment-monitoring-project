"""Module containing secure hashing of passwords."""

import bcrypt


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify if provided password matches the stored hashed password.

    Args:
        user_password (str): The plain-text password provided by the user for verification.
        crypt_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password match, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_password(password: str) -> str:
    """Generate a secure hash for the given password.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: A securely hashed version of the input password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
