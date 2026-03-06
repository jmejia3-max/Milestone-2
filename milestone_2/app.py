from flask import Flask, render_template, request, redirect, url_for
from task_manager import TaskManager
from weather_service import get_weather

app = Flask(__name__)

task_manager = TaskManager()


@app.route("/")
def index():
    tasks = task_manager.read()
    weather = get_weather("Chicago", "US")

    return render_template(
        "index.html",
        tasks=tasks,
        weather=weather
    )


@app.route("/tasks/<int:task_id>")
def show(task_id):
    task = task_manager.read(task_id)
    return render_template("show.html", task=task)


@app.route("/tasks/new", methods=["POST"])
def create():

    task_data = {
        "title": request.form["title"],
        "description": request.form.get("description")
    }

    task_manager.create(task_data)

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/edit")
def edit(task_id):

    task = task_manager.read(task_id)

    return render_template("edit.html", task=task)


@app.route("/tasks/<int:task_id>/update", methods=["POST"])
def update(task_id):

    update_data = {
        "title": request.form["title"],
        "description": request.form.get("description"),
        "completed": True if request.form.get("completed") else False
    }

    task_manager.update(task_id, update_data)

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete")
def delete(task_id):

    task_manager.delete(task_id)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)