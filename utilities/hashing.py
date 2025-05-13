from argon2 import PasswordHasher, exceptions

def hash_a_password(password:str)->str:
    """
    Hashes a password using Argon2 hashing algorithm.
    Args:
        password (str): The password to be hashed.
    Returns:
        str: The hashed password.
    """
    ph = PasswordHasher()
    return ph.hash(password)

async def verify_password(password:str, hashed_password:str)->bool:
    """
    Verifies a password against a hashed password.
    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.
    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except exceptions.VerifyMismatchError:
        return False