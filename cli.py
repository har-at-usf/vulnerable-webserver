from argparse import ArgumentParser


def get_args():

    parser = ArgumentParser(description="Test your own web vulnerabilities.")

    parser.add_argument(
        "--xss",
        help="Use unsafe form input/output (allows XSS).",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--csrf",
        help="Do not use tokens (allows CSRF).",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--hardcodehash",
        help="Hardcode the sysadmin's password hash in the login page (cryptographic failures).",
        action="store_true",
        default=False,
    )

    return parser.parse_args()
