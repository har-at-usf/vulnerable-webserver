from secrets import token_urlsafe
from session import SessionManager


class TokenManager:
    """Manage a list of tokens, which are accessed based on their cookies."""

    tokens: dict

    def __init__(self):
        self.tokens = {}

    def validate_token(self, token: str, cookie: str) -> str:
        return self.tokens[cookie] == token

    def update_token(self, cookie: str) -> str:
        self.tokens[cookie] = token_urlsafe()
        return self.tokens[cookie]

    def get_token(self, cookie: str) -> str:
        return self.tokens[cookie]


class TokenizedSessionManager(SessionManager, TokenManager):
    """Utilizes tokens to authorize requests. Prevents CSRF attacks."""

    def __init__(self):
        SessionManager.__init__(self)
        TokenManager.__init__(self)

    def update_email(self, cookie: str, token: str, new_email: str):

        if self.tokens[cookie] == token:
            print("[update_email] Token validated.")
            super().update_email(cookie, new_email)
