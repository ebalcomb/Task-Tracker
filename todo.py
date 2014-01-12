from flask import Flask, render_template, request, redirect, flash
import json
from datetime import datetime


app = Flask(__name__)
app.secret_key = "harrypotter"

@app.route("/")
def index():
	items = load_items()
	return render_template("index.html", to_do=items)

@app.route("/create", methods=["GET", "POST"])
def create():
	to_do = request.form["to_do"].strip()

	if to_do:
		month = str(request.form["month"])
		day = str(request.form["day"])
		year = str(request.form["year"])
		hour = str(request.form["hour"])
		minute = str(request.form["minute"])
		ampm = str(request.form["AMPM"])

		datetime_due = make_datetime("%s/%s/%s %s:%s %s" %(month, day, year, hour, minute, ampm))

		if datetime_due:
			display_due = datetime_due.strftime('%m/%d/%Y %I:%M %p')
			datetime_created = datetime.now()
			display_created = datetime_created.strftime('%m/%d/%Y %I:%M %p')

			unique = check_unique(to_do)
			future = check_future(datetime_due, datetime_created)


			if unique:
				if future:

					items = load_items()
					items.append({"content": to_do, "status": "new", "display_created": display_created, "complete_button": "complete", "display_due": display_due, "overdue":"upcoming"})

					for item in items:
						datetime_due = make_datetime(item["display_due"])
						if datetime_due < datetime.now():
							item["overdue"] = "overdue"
						else:
							item["overdue"] = "upcoming"

					save(items)
					flash("task added!")
				else:
					flash("ERROR: item cannot be due in the past")
			else:
				flash("ERROR: task already exists")
		else:
			flash("ERROR: invalid due date")


	return redirect("/")

@app.route("/complete", methods=["POST"])
def complete():
	completed = request.form["content"]
	items = load_items()
	for item in items:
		if item["content"] == completed:
			if item["status"] == "done":
				item["status"] = "new"
				item["complete_button"] = "complete"
			elif item["status"] == "new":
				item["status"] = "done"
				item["complete_button"] = "incomplete"
		else:
			pass
	save(items)

	return redirect("/")

@app.route("/edit", methods=["POST"])
def edit():
	original = request.form["content"]
	revised = request.form["revised"]
	items = load_items()
	for item in items:
		if item["content"] == original:
			item["content"] = revised
	save(items)

	return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
	deleted = request.form["content"]
	items = load_items()
	for item in items:
		if item["content"] == deleted:
			items.remove(item)
	save(items)

	return redirect("/")

def load_items():
	f = open("db.txt")
	json_version = f.read()
	f.close()
	if json_version:
		return json.loads(json_version)
	else:
		return []

def save(items):
	json_version = json.dumps(items)
	f = open("db.txt", 'w')
	f.write(json_version)
	f.close()

def make_datetime(string):
	try:
		datetime_format = datetime.strptime(string, "%m/%d/%Y %H:%M %p")
		return datetime_format
	except ValueError:
		return False

def check_unique(content):
	items = load_items()
	for item in items:
		if item["content"] == content:
			return False
	return True

def check_future(due, created):
	if due > created:
		return True
	else: 
		return False



if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0")