from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

participants = {}
current_choices = {}
trial_count = 0
last_result = "待機中"


@app.route("/", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        name = request.form["name"]
        participants[name] = True
        return redirect(url_for("participant", name=name))
    return render_template("join.html")


@app.route("/participant/<name>")
def participant(name):
    if name not in participants:
        return redirect(url_for("join"))
    return render_template(
        "participants.html",
        name=name,
        result=last_result,
        trial_count=trial_count
    )


@app.route("/choose", methods=["POST"])
def choose():
    name = request.form["name"]
    number = int(request.form["number"])
    current_choices[name] = number
    return redirect(url_for("participant", name=name))


@app.route("/admin")
def admin():
    return render_template(
        "admin.html",
        participants=participants,
        choices=current_choices,
        result=last_result,
        trial_count=trial_count,
        all_done=len(current_choices) == len(participants) and len(participants) > 0
    )


@app.route("/judge", methods=["POST"])
def judge():
    global trial_count, last_result

    trial_count += 1
    values = list(current_choices.values())

    if len(values) == len(set(values)):
        last_result = "成功"
    else:
        last_result = "失敗"

    return redirect(url_for("admin"))


@app.route("/next", methods=["POST"])
def next_trial():
    global current_choices, trial_count, last_result

    current_choices = {}
    last_result = "待機中"
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
