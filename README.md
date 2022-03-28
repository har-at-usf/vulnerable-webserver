# CSRF Demo

# Purpose 

This project allows you to demonstrate a CSRF exploit. There are
two components:

-   Vulnerable web application. The default initializes a poorly
    implemented session manager, one that does not use CSRF 
    tokens. The `session` module also includes a better version,
    which does use tokens to authorize requests. 

-   CSRF webpage. This will immediately launch the exploit and
    redirect to the webpage. 

# Exploit workflow

## CSRF

1.  Launch the Flask application.
1.  Open a web browser to `localhost:5000`
1.  Log in with the credentials `admin@mail.tld`.
1.  Navigate to the dashboard.
1.  Try to update the email address (authorized request).
1.  Open the malicious `csrf.html` page in the browser.
1.  Check that the malicious request has changed the email address.

## Cryptographic failures

The mitigated file (somewhat misleadingly) contains a weak, hardcoded administrator password hash. An attacker can create a rainbow table of (hashing weak-password permutations) to reveal a valid password. 

For documentation reasons, the password is `password1`. If you are trying this yourself, you should try to leverage an application or service that generates permutations. The input for the application or service should be weak, common passwords: for example, what you might expect for routers or webserver admin panels.

# Mitigation 

Try the exploit but use token-based session manager in the Flask 
application.

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
    
    
