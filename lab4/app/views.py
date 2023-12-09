from flask import request, render_template, redirect, url_for, make_response, session
from app import app
import json
from datetime import datetime
from os.path import join, dirname, abspath
import os

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Перевіряємо введені дані на автентифікацію
        for user in auth_data['users']:
            if user['username'] == username and user['password'] == password:
                # Зберігаємо інформацію про користувача в сесію
                session['username'] = username
                return redirect(url_for('info'))


    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/info')
def info():
    # Перевіряємо, чи користувач вже автентифікований
    if 'username' in session:
        username = session['username']
        os_name = os.name
        user_agent = request.user_agent.string
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render_template('info.html', os_name=os_name, user_agent=user_agent, current_time=current_time)
    else:
        # Якщо користувач не автентифікований, перенаправляємо його на сторінку входу
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



