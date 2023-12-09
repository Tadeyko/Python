import socket
import time
import os
import threading

def main():
    host = 'localhost'
    port = 12345
    recv(host, port)

def handle_client(conn, addr, users):
    connection_time = time.strftime("Дата: %d/%m/%y %H:%M:%S", time.localtime())
    users.append(conn)
    print(f'Користувач {os.getlogin()} з IP: {addr} підключився до сервера в [{connection_time}]\
        \nКористувачі онлайн: {len(users)}')
    while True:
        data = conn.recv(1024)
        if not data:
            users.remove(conn)
            print(f"Користувач {os.getlogin()} з IP: {addr} відключився від сервера\
                \nКористувачі онлайн: {len(users)}")
            break
        recv_time = time.strftime("Дата: %d/%m/%y %H:%M:%S", time.localtime())
        print(f'{os.getlogin()}: {data.decode()} [{recv_time}]')
        for user in users:
            if user != conn:
                user.sendall(data)
    conn.close()

def recv(host, port):
    users = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr, users))
            t.start()

main()
