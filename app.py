from flask import Flask, render_template, request
from helper import is_valid_email, apology

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        # validate email server-side
        if not is_valid_email(email):
            return apology("Email is invalid")
        # get user's category preference and check if user select at least one category
        categories = request.form.getlist("categories")
        if not categories:
            return apology("Please select at least one category")
        return render_template("success.html")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
