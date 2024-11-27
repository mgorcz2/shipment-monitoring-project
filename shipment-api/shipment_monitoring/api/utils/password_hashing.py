from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

from shipment_monitoring.api.utils import consts



def verify_password(user_password, crypt_password) -> bool:
    return pwd_context.verify(user_password, crypt_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)