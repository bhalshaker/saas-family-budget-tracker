from argon2 import PasswordHasher, exceptions

def hash_a_password(password:str):
    ph = PasswordHasher()
    return ph.hash(password)

async def verify_password(password:str, hashed_password:str):
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except exceptions.VerifyMismatchError:
        return False