from werkzeug.security import check_password_hash, generate_password_hash


class Pwd_encryption_decrypt(object):
    def encryption(self, password) -> str:
        p = generate_password_hash(password)
        return p

    def decrypt(self, encryption_passwd, password) -> bool:
        bool_value = check_password_hash(encryption_passwd, password)
        return bool_value
