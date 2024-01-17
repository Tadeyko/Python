from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from .models import Todo
from .forms import TaskForm

tasks = Blueprint('tasks', __name__, template_folder="templates/tasks")

@tasks.route('/', methods=['GET', 'POST'])
def todo():
    form = TaskForm()
    todo_list = db.session.query(Todo).all()

    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("tasks.todo"))

    return render_template('tasks.html', todo_list=todo_list, form=form)
 
@tasks.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("tasks.todo"))
 
@tasks.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("tasks.todo"))