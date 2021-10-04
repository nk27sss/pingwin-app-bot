import datetime
import platform
import socket
import subprocess
import time
from datetime import date, timedelta, timezone


SERVER_HOST = "localhost"  # Win10 Tslab IP
SERVER_PORT = 9090
WAITSECS = 1


def ping(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if platform.system().lower() == "windows" else True
    # Ping
    return subprocess.call(args, shell=need_sh) == 0


def insdat(d=None):
    if type(d) in [int, float]:
        d = datetime.datetime.fromtimestamp(d)
    elif type(d) == str:
        d = datetime.datetime.strptime(d)
    elif d is None:
        d = datetime.datetime.today()
    return d.strftime("%Y-%m-%d %H:%M:%S")


def send_message_bot(signal=None, dsc=""):
    if signal==1 or signal==10:
        txt = "Всё ок!"
    elif signal==0:
        txt = f"Проблема с прогой, {dsc}"
    elif signal==-3:
        txt = f"Неизвестная ошибка!, {dsc}"
    elif signal==-2:
        txt = f"Проблема с ВИНДОЙ!, {dsc}"
    elif signal==-1:
        txt = f"Проблема с коннектом, {dsc}"
    else:
        txt = f"Непонятный ответ  [{dsc}]"

    print(f"[{insdat()}]:", f"...send... [{signal}] ", txt)


def main():
    print(f"[{insdat()}]:", "START HEROKU BOT")

    signal = 0

    while True:
        try:
            sock = socket.socket()
            sock.connect((SERVER_HOST, int(SERVER_PORT)))
            runing = None
            while 1:
                # print(f"[{insdat()}]:", "ping.. ", end="")
                # Опрашиваем pinger_app
                sock.send(b'ping')
                # Получаем ответ
                resprecv = sock.recv(1024)
                try:
                    resp = int(resprecv)
                except ValueError:
                    resp = 2

                print(f"[{insdat()}]:", f": [{int(resp)}]")

                if resp == 1:
                    signal = 1
                    send_message_bot(signal)
                elif resp == 0:
                    signal = 0
                    send_message_bot(signal)
                else:
                    signal = 2
                    send_message_bot(signal,resprecv.decode('UTF-8'))

                time.sleep(WAITSECS)

            print(f"[{insdat()}]:", "Restart")

        except Exception as e:
            if type(e) in [ConnectionRefusedError, socket.gaierror, TimeoutError]:
                signal = -1
                send_message_bot(signal)
                r = ping(SERVER_HOST)
                if r:
                    # Серв отвечает
                    signal = -1
                    send_message_bot(signal, type(e).__name__)
                else:
                    # Серв НЕ отвечает
                    signal = -2
                    send_message_bot(signal, type(e).__name__)
            else:
                print(f"[{insdat()}]:", "Err:\t", e)
                signal = -3
                send_message_bot(signal, type(e).__name__)

            time.sleep(WAITSECS)


if __name__ == "__main__":
    main()

"""
    Signals
    -3      - Неизвестная ошибка!
    -2      - Проблема с ВИНДОЙ!
    -1      - Проблема с коннектом
    0       - Проблема с прогой
    1,10    - Всё ок
    2 и др  - Непонятный ответ 


"""
