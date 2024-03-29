from flask import request, render_template, redirect, url_for, make_response, session, flash
from flask import request
from app import app, db, bcrypt
import json
from datetime import datetime
from os.path import join, dirname, abspath
import os
from app.forms import LoginForm, TaskForm
from .forms import LoginForm, RegistrationForm, LoginForm2
from .models import User, Todo


auth_data_path = join(dirname(abspath(__file__)), 'users.json')
with open(auth_data_path, 'r') as f:
    auth_data = json.load(f)

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    expiry = int(request.form.get('expiry'))

    if 'cookies' not in session:
        session['cookies'] = {}

    session['cookies'][key] = {
        'value': value,
        'expires': expiry,
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    response = make_response(redirect(url_for('info')))
    response.set_cookie(key, value, max_age=expiry)

    return response



@app.route('/remove_cookie', methods=['POST'])
def remove_cookie():
    key_to_remove = request.form.get('key_to_remove')

    if key_to_remove in request.cookies:
        response = make_response(redirect(url_for('info')))
        response.delete_cookie(key_to_remove)

        cookies = session.get('cookies', {})
        cookies.pop(key_to_remove, None)
        session['cookies'] = cookies

        return response
    else:
        return "Cookie not found", 404

@app.route('/remove_all_cookies', methods=['POST'])
def remove_all_cookies():
    response = make_response(redirect(url_for('info')))

    for key in request.cookies.keys():
        response.delete_cookie(key)

    session.pop('cookies', None)

    return response




@app.route('/')
def index():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Завантаження користувачів з файлу
        with open(auth_data_path, 'r') as f:
            users_data = json.load(f)

        # Перевірка користувача та пароля
        for user in users_data['users']:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                if form.remember.data:
                    # зберігаємо інформацію про користувача в сесію
                    session.permanent = True
                flash(f'Ви увійшли як {username}', 'success')
                return redirect(url_for('info'))

        # Якщо користувач не знайдений або пароль невірний
        flash('Невірний логін або пароль', 'danger')

    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', form=form, os_name=os_name, user_agent=user_agent, current_time=current_time)



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('login'))

@app.route('/info')
def info():
    if 'username' in session:
        username = session['username']
        os_name = os.name
        user_agent = request.user_agent.string
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render_template('info.html', os_name=os_name, user_agent=user_agent, current_time=current_time)
    else:
        flash('Будь ласка, увійдіть в систему', 'info')
        return redirect(url_for('login'))

@app.route('/delete_cookie/<key>')
def delete_cookie(key):
    response = make_response(redirect(url_for('info')))
    cookies = session.get('cookies', [])
    session['cookies'] = [cookie for cookie in cookies if cookie['key'] != key]
    response.delete_cookie(key)
    return response

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    response = make_response(redirect(url_for('info')))
    for cookie in session.get('cookies', []):
        response.delete_cookie(cookie['key'])
    session.pop('cookies', None)
    return response


@app.route('/page1')
def page1():
    os_name = os.name
    user_agent = request.user_agent.string  # Замініть це на ваш спосіб отримання User-Agent
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/page2')
def page2():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page2.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/page3')
def page3():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page3.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/home')
def home():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('home.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/about')
def about():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('about.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/main')
def main():
    return redirect(url_for("home"))



@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        username = session['username']
        new_password = request.form.get('new_password')


        with open(auth_data_path, 'r') as f:
            auth_data = json.load(f)

        for user in auth_data['users']:
            if user['username'] == username:
                user['password'] = new_password

        with open(auth_data_path, 'w') as f:
            json.dump(auth_data, f, indent=2)

        return redirect(url_for('info'))


    return redirect(url_for('login'))


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TaskForm()
    todo_list = db.session.query(Todo).all()

    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("todo"))

    return render_template('todo.html', todo_list=todo_list, form=form)
 
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))
 
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account was created for {form.username.data}!', category="success")
        return redirect(url_for("login2"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', category="danger")

    return render_template('register.html', form=form, title="Register")

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm2()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', category="success")
            session['username'] = user.username  
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful", category='warning')

    return render_template('login2.html', form=form, title="Login")

@app.route("/users", methods=['GET', 'POST'])
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users)