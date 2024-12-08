from application import app
from flask import render_template, request, redirect, flash, url_for
from bson import ObjectId
from .forms import TodoForm
from application import db
from datetime import datetime


@app.route("/")
def get_todos():
    filter_option = request.args.get("filter", "all")
    todos = []

    if filter_option == "completed":
        query = {"completed": "True"}
    elif filter_option == "not_completed":
        query = {"completed": "False"}
    else:
        query = {}

    for todo in db.todos_flask.find(query).sort("date_created", -1):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
        todos.append(todo)

    return render_template("view_todos.html", todos=todos, filter_option=filter_option)


@app.route("/add_todo", methods=["POST", "GET"])
def add_todo():
    form = TodoForm(request.form)
    if request.method == "POST" and form.validate():
        todo_data = {
            "name": form.name.data,
            "description": form.description.data,
            "completed": form.completed.data,
            "due_date": form.due_date.data.strftime("%Y-%m-%d"),
            "priority": form.priority.data,
            "date_created": datetime.utcnow(),
        }
        db.todos_flask.insert_one(todo_data)
        flash("Todo successfully added", "success")
        return redirect("/")

    return render_template("add_todo.html", form=form)


@app.route("/update_todo/<id>", methods=["POST", "GET"])
def update_todo(id):
    form = TodoForm(request.form)
    if request.method == "POST" and form.validate():
        updated_data = {
            "name": form.name.data,
            "description": form.description.data,
            "completed": form.completed.data,
            "due_date": form.due_date.data.strftime("%Y-%m-%d") if form.due_date.data else None,
            "priority": form.priority.data,
        }
        db.todos_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": updated_data})
        flash("Todo successfully updated", "success")
        return redirect("/")

    todo = db.todos_flask.find_one({"_id": ObjectId(id)})
    if todo:
        form.name.data = todo.get("name")
        form.description.data = todo.get("description")
        form.completed.data = todo.get("completed")
        form.due_date.data = (
            datetime.strptime(todo.get("due_date"), "%Y-%m-%d") 
            if todo.get("due_date") else None
        )
        form.priority.data = todo.get("priority")

    return render_template("add_todo.html", form=form)


@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todos_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")
