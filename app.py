from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def mainpage():  # put application's code here
    if request.method == "POST":
        message = request.form.get("message")
        # TODO get solution response: 0 or 1
        response = 1
        print(message)
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
        email = {
            "subject": "Dupa",
            "from": "Baran",
            "message": "chuj ci w ogon pajacu"
        }
        # TODO fetch email dict
        # TODO get solution response: 0 or 1
        response = 1
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
