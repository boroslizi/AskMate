import bcrypt


def generate_salt():
    salt = bcrypt.gensalt()
    return salt


def hash_password(plain_text_password, salt):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_bytes.decode('utf-8')
