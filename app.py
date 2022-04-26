#from session import SessionManager
#from tokens import TokenizedSessionManager
from authorization import Authorization, BasicSession, BasicCsrfTokens, NoCsrfTokens
from credentials import CredentialManagerAPI
from cli import get_args
from flask import Flask, render_template, request, make_response
from traceback import print_exc
from os import path
from shutil import rmtree


SESSION_MANAGER: Authorization


app = Flask(__name__)


# Lord forgive me for my global variables... After they are set from the CLI
# args, DO NOT change their values.
DEMO_SETTINGS: dict


# Uncomment to catch all errors (debug). You can return a generic error page.
# @app.errorhandler(Exception)
# def bad_login(exception):
#    print(print_exc(), str(exception))


@app.route("/loginerror")
def login_error(user=""):
    """Return an 'invalid login' webpage to the user (for example, bad
    username or password). If the global `unsanitized_forms` option is
    `True` (default), the returned webpage is vulnerable to XSS. Otherwise,
    it applies HTML encoding to the username, and returns a webpage that is
    safe to render on a browser."""

    # String concatenation (vulnerable to script injection).
    if DEMO_SETTINGS["unsafe_form_data"]:
        error_page = render_template("invalid-login.html").replace(
            "Dear ", "Dear " + user
        )

    # Applies encoding to all input (XSS-safe).
    else:
        error_page = render_template("invalid-login.html", username=user)

    return make_response(error_page)


@app.route("/")
def index():
    """Default webpage served."""
    resp = make_response(render_template("index.html"))
    resp.set_cookie("Cookie", "initialcookienologin")
    return resp


@app.route("/login", methods=["POST", "GET"])
def login():
    """Called when the user sets a cookie for the first time."""

    if not request.method == "POST":
        return index()

    user = request.form["email"]
    user_password = request.form["password"]

    cookie_key = SESSION_MANAGER.validate_login(user, user_password)

    if not cookie_key:
        return login_error(user)

    new_cookie, new_token = SESSION_MANAGER.create_session(cookie_key)

    resp = make_response(render_template("readcookie.html"))
    resp.set_cookie("Cookie", new_cookie)

    return resp 


@app.route("/dashboard")
def dashboard():
    """Present a mock dashboard for user actions. Current version will display
    the user's email/username and session cookie."""

    cookie = request.cookies.get("Cookie")
    csrf_token = SESSION_MANAGER.get_token(cookie)

    # If the user is not logged in, return to the login screen.
    if not SESSION_MANAGER.is_logged_in(cookie):
        return login()

    return make_response(
        render_template(
            "dashboard.html",
            username=SESSION_MANAGER.get_credential_info(cookie),
            cookie=cookie,
            csrf_token=csrf_token
        )
    )


@app.route("/update-email", methods=["POST"])
def change_email():
    """Require a token in order to change the email address."""

    cookie = request.cookies.get("Cookie")
    csrf_token = request.form.get("csrf-token")

    SESSION_MANAGER.update_email(cookie, csrf_token, request.form["new_email"])

    return dashboard()


if __name__ == "__main__":
    """TODO: Separate this logic somewhere else..."""

    delete_these = ["__pycache__"]

    for filename in delete_these:

        if path.exists(filename):
            rmtree(filename)

    # Settings are based on cli arguments.
    cli_args = get_args()

    # Set to `False` unless the flag is explicitly specified.
    DEMO_SETTINGS = {
        "unsafe_form_data": cli_args.xss,
        "disable_csrf_tokens": cli_args.csrf,
        "hardcode_admin_hash": cli_args.hardcodehash,
    }

    # TODO: In the future, see notes for composition/interfacing in tokens.py...
    SESSION_MANAGER = Authorization(
        BasicSession(),
        NoCsrfTokens() if DEMO_SETTINGS["disable_csrf_tokens"] else BasicCsrfTokens(),
        CredentialManagerAPI
    )

    app.run()
