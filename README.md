# Vulnerable Webserver

This is a simple Flask application that is meant for education or research purposes. The intent is to provide a developer with the means to create their own exploit, for demonstration purposes. 

The idea of a "vulnerable web application" is not new. This project differs from existing ones because you are not supposed to "find" any exploits or flaws. Instead, you are supposed to *make* them.

The flask applications are designed as a base. This should allow you to write your own exploits, to your liking, without wasting time finding them. It is less of a "pentest box" and more of an application template.

# Starting the application

Install the following applications or packages:

- `python3 >= 3.7`  
- `bcrypt`

To start the application, run the `app.py` script. Use the command-line options to specify vulnerabilities. Use `app.py -h` to list all options.

**NOTE**: You must use the same domain for all attacks. For a local session, use `127.0.0.1` or `localhost`, but *not both interchangably*. For example, the CSRF attack will fail if you use `localhost`.

# Exploits

This is an overview of the *very deliberate vulnerabilities* that currently exist. The idea is for you (the developer) to add exploits. This is meant for educational purposes, so keep them simple but meaningful.

## CSRF

By default, the application uses a basic "synchronizer" token to prevent CSRFs. You can disable these using the `--csrf` command-line option. To exploit it while using this option, do the following:

1.  Launch the Flask application.
1.  Open a web browser to `127.0.0.1:5000`
1.  Log in with the credentials `admin@mail.tld`.
1.  Navigate to the dashboard.
1.  Try to update the email address (authorized request).
1.  Open the malicious `csrf.html` page in the same browser.
1.  Check that the malicious request has changed the email address.

You can mitigate this attack by using tokens. This is what the "regular" `app.py` does by default, albeit with basic tokens. JWTs may improve the integrity of tokens even further; the user can recommend these, but the demo will not implement them, as it is outside of scope. (The point is to show what happens when you don't use *any* tokenas at all. It is a very simple point.)

## Cryptographic failures

The mitigated file (somewhat misleadingly) contains a weak, hardcoded administrator password hash. An attacker can create a rainbow table of (hashing weak-password permutations) to reveal a valid password. 

For documentation reasons, the password is `password1`. 

If you are trying this for the sake of "breaking it on your own," you could first try to leverage an application or service that generates permutations. The input for the application or service should be weak, common passwords: for example, what you might expect for routers or webserver admin panels. In addition, precomputed hash tables would also be a great demo for your audience.

Keep in mind that, even for a better password, the attacker need only find any input that generates the resultant hash. This means, they could use an input that does not actually match the user's password. By providing the administrator's hash, you are essentially facilitating a major step in such an attack.

To mitigate this, avoid hardcoded credentials or hashes. Hardcoding your passwords and hashes is tantamount to giving up your credentials. Ensure that all users (*especially* ones with higher privileges) use sufficient entropy in their passwords.

Further, ensure that the backend data store is saving salted passwords: preferably, musing a real crypto utility like `bcrypt`. This will prevent the attacker from creating a precomputed table (like a rainbow table) in a computationally feasible timeframe. Such a slowdown should give the DBA enough time to invalidate all of the compromised hashes and rebuild the database. Secure data stores are out of the scope of this project at the time of writing.

*Note about the data store: This webserver actually uses bcrypt and implements it the same way you would an actual database; the only egregious difference is that it hardcodes the credentials in the backend. SQL injection is not a current feature, as clear examples for demoing SQL injection exist all across the internet. The need to demo it here does not yet exist. If the need arises to implement that in this webserver, I will do so.*

## Injection

You can do XSS and SQL injection with then `username or email` form field.

```html
<script>alert("pwnd");</script>
```

This will raise an alert on the "login error" page. 

To mitigate script injection, you should:

- Always validate input data. For example, validating only an email pattern would prevent the script from executing.
- Always encode output based on user input. HTML encoding will convert the special characters into a corresponding safe character. For example, the brackets `<` and `>` are converted into `&lt;` and `&gt;`, respectively. This tells the browser to render those characters without treating them as actual HTML tags. They will look the same on the surface, but will have no functionality&mdash;that is the goal.

Many industry-level packages will include functionality to validate, encode, and sanitize data. Make sure that you use packages which are tested and secure. OWASP features several libraries to this end.

Incidentally, Flask includes some output encoding. The `render_template` function can accept variables and input their values, HTML-encoded, into the template webpage.

For example, the line in an HTML document named `welcome.html`:

```html 
<p>Welcome back, {{username}}!</p>
```

Can safely insert a username using a `render_template` parameter:

```python 
resp = make_response(render_template("welcome.html", username=request.form["user"]))
```

Using the malicious script above, the response will load in the user's browser. However, it will appear like this:

```html 
<p>Welcome back, &lt;script&gt;alert(0x0);&lt;/script&gt;!</p>
```

The line will render with brackets characters, but it will not raise the alert. Thus, the encoding is preventing script injection in the client's browser.

# Security considerations

The application has not been pentested. It is only mean to showcase the
basic concepts for a CSRF attack and mitigation. The application is not 
designed to face the web. Use it locally. Use it only for this exploit
demonstration.

The application catches all exceptions and redirects them to a basic
prompt. You will not receive any information (in the console) about
the reasons for an error. This is largely because a broken website can
distract the audience from the basic flow of the attack. Still, it may
be challenging to debug any unexpected issues.

# References

-   <https://flask.palletsprojects.com/en/1.1.x/quickstart/>

-   <https://portswigger.net/web-security/csrf>

-   <https://medium.com/@kaviru.mihisara/synchronizer-token-pattern-e6b23f53518e>

-   [Sanitized way to include Python variables with Flask templates (avoid XSS)](https://pythonbasics.org/flask-tutorial-templates/)
    
    
