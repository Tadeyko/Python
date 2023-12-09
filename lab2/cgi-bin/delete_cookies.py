#!/usr/bin/env python3
import os
import http.cookies

# Створення об'єкта cookies
cookies = http.cookies.SimpleCookie()

# Виведення заголовку контенту з видаленням cookies
print("Set-Cookie: form_count=; expires=Thu, 01 Jan 1970 00:00:00 GMT")
print("Content-type: text/html\n")


print("<html>")
print("<head>")
print("<title>Видалення cookies</title>")
print("</head>")
print("<body>")
print("<h2>Cookies були успішно видалені.</h2>")
print("</body>")
print("</html>")
