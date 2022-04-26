from secrets import token_urlsafe
from hashlib import sha256

from credentials import CredentialManagerAPI


class CsrfTokens:
    
    def validate(self, key: str, token: str) -> bool:
        pass
    
    def update_token(self, key: str) -> str:
        pass

    def get_token(self, key: str) -> str:
        pass


class NoCsrfTokens(CsrfTokens):
    
    def __init__(self):
        pass 
    
    def validate(self, key: str, token: str) -> bool:
        print("validate_token: Tokens are disabled Returning `True` unconditionally.")
        return True
    
    def update_token(self, key: str) -> str:
        print("NOTE: update_token: Tokens are disabled.")
        return "no_token"
        
    def get_token(self, key: str) -> str:
        print("NOTE: get_token: Tokens are disabled.")    
        return "no_token"


class BasicCsrfTokens(CsrfTokens):

    tokens: dict

    def __init__(self):
        self.tokens = {}

    def validate(self, key: str, token: str) -> bool:
        return self.tokens.get(key) == token if token else None

    def update_token(self, key: str) -> str:
        self.tokens[key] = token_urlsafe()
        return self.tokens[key]

    def get_token(self, key: str) -> str:
        return self.tokens.get(key)


class Session:
    
    def set_cookie(self, key: str) -> str:
        pass 
    
    def get_cookie(self, cookie: str) -> str:
        pass
            
class BasicSession(Session):

    session: dict

    def __init__(self):
        self.session = {}

    def set_cookie(self, key: str) -> str:

        new_cookie = self._get_nonce()
        self.session[new_cookie] = key

        return new_cookie  
    
    def get_key(self, cookie: str) -> str:
        return cookie in self.session.values() 

    def get_user(self, cookie: str) -> str:
        return self.session.get(cookie)
    
    def validate(self, cookie: str) -> str:
        return cookie in self.session.keys()

    def _get_nonce(self):
        return sha256(token_urlsafe().encode()).hexdigest()


class Authorization:
    """Implement a session manager that does not use tokens. This is vulnerable
    to CSRF attacks."""

    credential_manager: CredentialManagerAPI
    session_manager: Session
    token_manager: CsrfTokens
    
    def __init__(self, session_manager: Session, token_manager: CsrfTokens, credential_manager: CredentialManagerAPI):
        self.token_manager = token_manager
        self.session_manager = session_manager
        self.credential_manager = credential_manager

    def create_session(self, key: str) -> tuple:
        new_cookie = self.session_manager.set_cookie(key)
        new_token = self.token_manager.update_token(new_cookie)
        return new_cookie, new_token

    def update_email(self, cookie: str, token: str, new_email: str):
        print("Trying to update email with", cookie, token)
        
        if self.token_manager.validate(cookie, token):
            
            if self.session_manager.validate(cookie):
                
                print("Cookie and token validated. Updating email.")
                self.credential_manager.update_email(self.session_manager.get_user(cookie), new_email)
        # Uncomment to use per-request tokens.
        #
        #       self.token_manager.update_token(cookie)
        #        
        #return self.token_manager.get_token(cookie)

    def get_credential_info(self, cookie: str) -> str:
        return self.credential_manager.get_credential_info(self.session_manager.get_user(cookie))

    def validate_login(self, email: str, password: str) -> bool:
        print(email, password)
        return self.credential_manager.validate_user(email, password)

    def is_logged_in(self, cookie: str) -> bool:
        return self.session_manager.get_user(cookie)

