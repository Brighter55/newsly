import re
from flask import render_template

def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(regex, email):
        return True
    else:
        return False

def apology(text):
    return render_template("apology.html", text=text)
