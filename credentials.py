from bcrypt import hashpw, checkpw, gensalt


class Credential:
    """Define an object that holds the same data that you would expect in a
    credential data store."""

    username: str
    email: str
    pwd_hash: bytes

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.pwd_hash = hashpw(password.encode(), gensalt())

    def __str__(self):
        return "Email: " + self.email


class CredentialManagerAPI:
    """Mock API to imitate a database API. Credentials are hardcoded. They can
    be modified during runtime. They are reset whenever the webserver
    application ends. Define all methods as static (`cls`) since all
    instances of this object should use the same set of valid users."""

    valid_users = {
        1: Credential("admin", "admin@mail.tld", "password123"),
        2: Credential("sysadmin", "sysadmin", "password1")    
    }

    @classmethod
    def validate_user(cls, email: str, password: str):

        for pk, credential in cls.valid_users.items():

            if credential.email == email and checkpw(
                password.encode(), credential.pwd_hash
            ):
                return pk

        return None

    @classmethod
    def update_email(cls, pk: int, new_email: str):
        cls.valid_users[pk].email = new_email

    @classmethod
    def get_credential_info(cls, pk: int) -> str:
        return str(cls.valid_users[pk]) if cls.valid_users.get(pk) else None
