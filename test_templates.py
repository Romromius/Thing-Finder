from flask import Flask, render_template, json
import os

app = Flask(__name__)


@app.route('/index')
@app.route('/')
def site():
    params = {
    }
    return render_template("index_ads.html", **params)


@app.route("/form_register", methods=['GET', 'POST'])
def form_register():
    params = {
    }
    return render_template("form_register.html", **params)


@app.route("/form_ad", methods=['GET', 'POST'])
def form_ad():
    params = {
    }
    return render_template("form_ad.html", **params)


@app.route("/catmail")
def catmail():
    params = {
    }
    return render_template("catmail.html", **params)


@app.route("/catdocs")
def catdocs():
    return render_template("catdocs.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='127.0.0.1')  # 0.0.0.0
