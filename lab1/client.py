import socket
import time

def send():
    host="localhost"
    port=12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        start_time = time.strftime("%H:%M:%S", time.localtime())
        s.sendall(start_time.encode())
        while True:
            now = time.strftime("Дата: %d/%m/%y %H:%M:%S", time.localtime())
            message = input(f"[{now}] > ")
            s.sendall(message.encode())


send()