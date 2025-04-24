"""Module containing secure hashing of passwords."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user_password: str, crypt_password: str) -> bool:
    """Verify if provided password matches the stored hashed password.

    Args:
        user_password (str): The plain-text password provided by the user for verification.
        crypt_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the password match, False otherwise.
    """
    return pwd_context.verify(user_password, crypt_password)


def hash_password(password: str) -> str:
    """Generate a secure hash for the given password.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: A securely hashed version of the input password.
    """
    return pwd_context.hash(password)
