from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
import os

resume = Blueprint('resume', __name__, template_folder="templates/resume", static_folder="static")

@resume.route("/")
def index():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/page1')
def page1():
    os_name = os.name
    user_agent = request.user_agent.string  # Замініть це на ваш спосіб отримання User-Agent
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page1.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/page2')
def page2():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page2.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/page3')
def page3():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('page3.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/home')
def home():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('home.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/about')
def about():
    os_name = os.name
    user_agent = request.user_agent.string
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('about.html', os_name=os_name, user_agent=user_agent, current_time=current_time)

@resume.route('/main')
def main():
    return redirect(url_for("home"))