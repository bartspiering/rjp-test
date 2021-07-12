import re


def strong_password(value):
    if not re.match(
        "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})", value
    ):
        raise ValueError(
            (
                "Password not strong enough, the requirements are: "
                "The password is at least 8 characters long. "
                "The password has at least one uppercase letter. "
                "The password has at least one lowercase letter. "
                "The password has at least one digit. "
                "The password has at least one special character."
            )
        )

    return value
