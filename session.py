from credentials import CredentialManagerAPI
from secrets import token_urlsafe
from hashlib import sha256


class SessionManager:
    """Implement a session manager that does not use tokens. This is vulnerable
    to CSRF attacks."""

    session: dict

    def __init__(self):
        self.session = {}

    def set_cookie(self, key: str) -> str:

        new_cookie = self._get_nonce()
        self.session[new_cookie] = key

        return new_cookie

    def update_email(self, cookie: str, new_email: str):

        if cookie in self.session.keys():
            print("[update_email] Cookie validated.")
            CredentialManagerAPI.update_email(self.session[cookie], new_email)

    def get_credential_info(self, cookie: str) -> str:
        return CredentialManagerAPI.get_credential_info(self.session[cookie])

    def validate_login(self, email: str, password: str) -> bool:
        return CredentialManagerAPI.validate_user(email, password)

    def is_logged_in(self, cookie: str) -> bool:
        return self.session.get(cookie)

    def _get_nonce(self):
        return sha256(token_urlsafe().encode()).hexdigest()
