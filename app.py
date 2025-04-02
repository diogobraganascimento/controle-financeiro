from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/credito")
def credito():
    return render_template("credito.html")


@app.route("/debito")
def debito():
    return render_template("debito.html")


if __name__ == "__main__":
    app.run(debug=True)

