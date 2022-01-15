from flask import Flask, render_template, request

from google.google_handler import get_emails
from models.vm import classify

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def mainpage():  # put application's code here
    if request.method == "POST":
        message = request.form.get("message")
        # TODO get solution response: 0 or 1
        response = classify(message)
        if response == 1 or response == 0:
            if response == 1:
                color = "red"
                result = ""
            elif response == 0:
                color = "green"
                result = "not "
            return render_template("result.html", msg=message, res=result, col=color)
        else:
            suggestion = "Please make sure your input is a plain text"
            return render_template("apology.html", suggestion=suggestion)
    else:
        return render_template("index.html")


@app.route('/mail', methods=["GET", "POST"])
def classfmail():
    if request.method == "POST":
        index = int(request.form.get("index"))
        try:
            email = get_emails(index)
            list = email["from"].split()
            address = list[-1]
            address = address[:4] + (len(address)-13)*"*" + address[-13:]
            list[-1] = address
            email["from"] = " ".join(list)
        except Exception as e:
            print(e)
            suggestion = "Please make sure there is enough emails"
            return render_template("apology.html", suggestion=suggestion)
        response = classify(email["message"])
        if response == 1 or response == 0:
            if response == 1:
                color = "red"
                result = ""
            elif response == 0:
                color = "green"
                result = "not "
            return render_template("mail.html", email=email, res=result, col=color, ind=index + 1)
        else:
            suggestion = "Please make sure your input is a plain text"
            return render_template("apology.html", suggestion=suggestion)


if __name__ == '__main__':
    app.run()
