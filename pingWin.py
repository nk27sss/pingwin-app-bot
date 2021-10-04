import datetime
import socket
import time
from datetime import date, timedelta, timezone

import psutil


NAME_EXE = "TSLab.exe"
NAME_EXE = "sublime_text.exe"

SOCKET_PORT = 9090


def processFind(name):
    find = False
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            find = p.info['name']
    return find


def insdat(d=None):
    if type(d) in [int, float]:
        d = datetime.datetime.fromtimestamp(d)
    elif type(d) == str:
        d = datetime.datetime.strptime(d)
    elif d is None:
        d = datetime.datetime.today()
    return d.strftime("%Y-%m-%d %H:%M:%S")


def main():
    print(f"[{insdat()}]:", "START PINGER-EXE SERVER")
    sock = socket.socket()
    sock.bind(('', int(SOCKET_PORT)))
    sock.listen(1)
    while True:
        try:
            # Ожидалка получения данных
            conn, addr = sock.accept()
            print(f"[{insdat()}]:", "connected:", addr)
            while True:
                # Получаем данные
                ask = conn.recv(1024)
                if ask:
                    # если есть данные то
                    print(f"[{insdat()}]:", "ask:", ask)
                    if ask == b"ping" or ask == b"1":
                        # запрос чекера к программе
                        try:
                            isrunning = processFind(NAME_EXE)
                        except Exception as e:
                            isrunning = False

                        # если работает 1 если нет 0
                        if isrunning:
                            conn.send(b"1")
                        else:
                            conn.send(b"0")

                    else:
                        print("What command 404???")
                        conn.send(b"404")
                else:
                    break
            conn.close()
        except Exception as e:
            if type(e) in [ConnectionResetError]:
                print(f"[{insdat()}]:", "connect close", addr)
            print("Err:\t", e)
            time.sleep(1)

if __name__ == "__main__":
    main()