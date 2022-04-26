from session import SessionManager
from flask import Flask, render_template, request, make_response


SESSION_MANAGER = SessionManager()

app = Flask(__name__)


# @app.errorhandler(Exception)
# def bad_login(exception):
#    return "<h1>An error has occurred</h1><a href='/'>Return to home</a>"


@app.route("/")
def index():
    """Default webpage served."""
    resp = make_response(render_template("index.html"))
    resp.set_cookie("Cookie", "initialcookienonce")
    resp.set_cookie("csrf-token", "initialcsrfnonce")
    return resp


@app.route("/login", methods=["POST"])
def login():
    """Called when the user sets a cookie for the first time."""

    if not request.method == "POST":
        raise Exception("This endpoint only accepts POST requests.")

    user_email = request.form["email"]
    user_password = request.form["password"]

    cookie_key = SESSION_MANAGER.validate_login(user_email, user_password)

    if not cookie_key:
        raise Exception("Invalid credentials.")

    resp = make_response(render_template("readcookie.html"))

    new_cookie = SESSION_MANAGER.set_cookie(cookie_key)
    resp.set_cookie("Cookie", new_cookie)

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
        + "</p><p><pre>Cookie: "
        + cookie
        + "</pre></p>"
        + render_template("dashboard.html")
    )


@app.route("/update-email", methods=["POST"])
def change_email():
    
    print(request.cookies.get("Cookie"))

    cookie = request.cookies.get("Cookie")

    SESSION_MANAGER.update_email(cookie, request.form["new_email"])

    return dashboard()


if __name__ == "__main__":
    app.run()
