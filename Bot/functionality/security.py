from jose import JWTError, jwt
from passlib.context import CryptContext
import datetime
import os


# run openssl rand -hex 32
# get key from dotenv
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(key):
    """
    Create a new access token
    :param user_id:
    :return:
    """
    payload = {
        "sub": key,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def getKey(token):
    """
    Verify the token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    return payload.get("sub")

# create access token for notion db and api key
# create a script to migrate existing database to encrypted one. 
# decryption at the time of storing stuff in guild_info is required