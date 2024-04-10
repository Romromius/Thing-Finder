from flask import Flask, render_template, json
import os

app = Flask(__name__)


@app.route('/index')  # EDITING...
@app.route('/')
def site():
    params = {
    }
    return render_template("index_ads.html", **params)


@app.route("/form_register", methods=['GET', 'POST'])  # NEED A TEMPLATE, REALIZATION
def form_register():
    params = {
    }
    return render_template("form_register.html", **params)


@app.route("/form_ad", methods=['GET', 'POST'])  # NEED A REALIZATION
def form_ad():
    params = {
    }
    return render_template("form_ad.html", **params)


@app.route("/rating")  # NEED A TEMPLATE, REALIZATION
def rating():
    params = {
    }
    return render_template("rating.html", **params)


@app.route("/catmail")  # NEED A TEMPLATE, REALIZATION
def catmail():
    params = {
    }
    return render_template("catmail.html", **params)


@app.route("/catdocs")  # NEED A DOCS
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")  # finished
def donate():
    return render_template("donate.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='127.0.0.1')  # 0.0.0.0
