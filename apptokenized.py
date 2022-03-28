from tokens import TokenizedSessionManager
from flask import Flask, render_template, request, make_response
from traceback import print_exc


SESSION_MANAGER = TokenizedSessionManager()

app = Flask(__name__)


# Uncomment to catch all errors (debug).
# @app.errorhandler(Exception)
# def bad_login(exception):
#    print(print_exc(), str(exception))
#    return "<h1>An error has occurred</h1><a href='/'>Return to home</a>"


@app.route("/")
def index():
    """Default webpage served."""
    resp = make_response(render_template("index.html"))
    resp.set_cookie("Cookie", "initialcookienonce")
    resp.set_cookie("csrf-token", "initialcsrfnonce")
    return resp


@app.route("/login", methods=["POST", "GET"])
def login():
    """Called when the user sets a cookie for the first time."""

    if not request.method == "POST":
        raise Exception("Invalid request method.")

    user_email = request.form["email"]
    user_password = request.form["password"]

    cookie_key = SESSION_MANAGER.validate_login(user_email, user_password)

    if not cookie_key:
        raise Exception("Invalid login credentials.")

    new_cookie = SESSION_MANAGER.set_cookie(cookie_key)
    new_token = SESSION_MANAGER.update_token(new_cookie)

    resp = make_response(render_template("readcookie.html"))
    resp.set_cookie("Cookie", new_cookie)
    resp.set_cookie("csrf-token", new_token)

    return resp


@app.route("/dashboard")
def dashboard():
    """Called when a user wants to check their cookies."""

    cookie = request.cookies.get("Cookie")

    if not SESSION_MANAGER.is_logged_in(cookie):
        raise Exception("User is not logged in.")

    return make_response(
        "<h1>Welcome</h1>"
        + SESSION_MANAGER.get_credential_info(cookie)
        + "</pre></p>"
        + render_template("dashboard.html")
    )


@app.route("/update-email", methods=["POST"])
def change_email():
    """Require a token in order to change the email address."""

    cookie = request.cookies.get("Cookie")
    csrf_token = request.form["csrf-token"]

    SESSION_MANAGER.update_email(cookie, csrf_token, request.form["new_email"])

    return dashboard()


if __name__ == "__main__":
    app.run()
