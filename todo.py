from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "harrypotter"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
	to_do = request.form["to_do"]
	return render_template("index.html", to_do=to_do)


if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")