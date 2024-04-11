from flask import Flask, render_template, json, request, url_for
import os

app = Flask(__name__)


@app.route('/index')  # EDITING...
@app.route('/')
def site():
    params = {"url": url_for('static', filename='css/style.css')}
    return render_template("index_ads.html", **params)


@app.route("/form_register", methods=['GET', 'POST'])  # NEED A REALIZATION
def form_register():
    if request.method == "GET":
        params = {}
        return render_template("form_register.html", **params)
    else:
        for i in list(request.form.keys()):
            print(i, request.form.get(i))
        request.method = "GET"
        return """<!doctype>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>site</title>
            <link rel="shortcut icon" href="static/img/icon.png">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        </head>
        <body>
            <h1>Вы успешно зарегистрировались!</h1>
        </body>
        </html>"""


@app.route("/form_ad", methods=['GET', 'POST'])  # NEED A REALIZATION
def form_ad():
    params = {
    }
    return render_template("form_ad.html", **params)


@app.route("/myads")  # NEED A REALIZATION
def myads():
    params = {
    }
    return render_template("my_ads.html", **params)


@app.route("/catdocs")  # finished
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")  # finished
def donate():
    return render_template("donate.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='127.0.0.1')  # 0.0.0.0
