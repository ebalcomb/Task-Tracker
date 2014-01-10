from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "harrypotter"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/create", methods=["POST"])
def create():
	to_do = request.form["to_do"]
	f = open("db.txt", 'a')
	f.write("%s\n" % to_do)
	f.close()
	f = open("db.txt")
	items = f.readlines()
	return render_template("index.html", to_do=items)


if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")