#!/usr/bin/env python3
import cgi
import cgitb
import os
from http import cookies

# Включення виводу деталей про помилки для відладки
cgitb.enable()

# Отримання даних з форми
form = cgi.FieldStorage()

# Робота з cookies
cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
num_forms_filled = int(cookie.get("num_forms_filled", "0").value if cookie.get("num_forms_filled") else "0")

# Виведення заголовку контенту
print("Content-type: text/html\n")

print("<html>")
print("<head>")
print("<title>Результат обробки форми</title>")
print("</head>")
print("<body>")

# Обробка натискання кнопки "Видалити Cookies"
if "delete_cookies" in form:
    cookie["num_forms_filled"] = ""
    cookie["num_forms_filled"]["expires"] = 0
    print("<p>Всі cookies видалено.</p>")
else:
    # Обробка отриманих даних і виведення результатів
    if "brand" in form and "type" in form:
        brand = form["brand"].value
        car_type = form["type"].value

        print("<h2>Результат обробки форми:</h2>")
        print("<p>Ваша улюблена марка авто: {}</p>".format(brand))
        print("<p>Тип авто: {}</p>".format(car_type))

        if "favorite_model" in form:
            favorite_model = form["favorite_model"].value
            print("<p>Ваша улюблена модель: {}</p>".format(favorite_model))

        if "subscribe_news" in form:
            subscribe_news = form["subscribe_news"].value
            print("<p>Підписатися на новини: {}</p>".format("Так" if subscribe_news == "yes" else "Ні"))
        else:
            print("<p>Ви вирішили не підписуватись на новини.</p>")

        # Оновлення cookies
        num_forms_filled += 1
        cookie["num_forms_filled"] = str(num_forms_filled)
        print("<p>Ви заповнили форму {} раз(и).</p>".format(num_forms_filled))
    else:
        print("<h2>Помилка! Будь ласка, заповніть всі обов'язкові поля форми.</h2>")

print("</body>")
print("</html>")
