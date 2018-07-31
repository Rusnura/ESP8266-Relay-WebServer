# -*- coding: utf-8 -*-
import socket


class Server:
    def send_answer(self, conn, status="200 OK", typ="text/plain; charset=utf-8", data=""):
        data = data.encode("utf-8")
        conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
        conn.send(b"Server: simplehttp\r\n")
        conn.send(b"Connection: close\r\n")
        conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
        conn.send(b"Content-Length: " + bytes(len(data)) + b"\r\n")
        conn.send(b"\r\n")  # после пустой строки в HTTP начинаются данные
        conn.send(data)

    def RouteAdd(self, path, funcname):
        if path not in self.routes:
            self.routes[path] = funcname

    def parse(self, conn, addr):  # обработка соединения в отдельной функции
        data = b""
        while not b"\r\n" in data:  # ждём первую строку
            tmp = conn.recv(1024)
            if not tmp:  # сокет закрыли, пустой объект
                break
            else:
                data += tmp

            if not data:  # данные не пришли
                return  # не обрабатываем

            udata = data.decode("utf-8")
            # берём только первую строку
            udata = udata.split("\r\n", 1)[0]
            # разбиваем по пробелам нашу строку
            method, string, protocol = udata.split(" ", 2)
            if string.find('?') != -1:
                address = string.split('?')[0]
                params = dict(b.split('=') for b in string.split('?')[1].split('&'))
            else:
                address = string
                params = {}
            if method != "GET":
                self.send_answer(conn, "404 Not Found", data="Page not found")
                return
            if address in self.routes:
                if len(params) > 0:
                    self.send_answer(conn, typ="text/html; charset=utf-8", data=self.routes[address](address, params))
                else:
                    try:
                        self.send_answer(conn, typ="text/html; charset=utf-8", data=self.routes[address]())
                    except:
                        self.send_answer(conn, typ="text/html; charset=utf-8", data=self.routes[address](address))
                return

            else:
                self.send_answer(conn, "404 Not Found", data="Page not found")
                return

    def __init__(self, port=80):
        self.routes = {}
        self.stop = False
        self.sock = socket.socket()
        self.sock.bind(("", port))
        self.sock.settimeout(2)
        self.sock.listen(5)

    def Run(self):
        try:
            while 1:  # работаем постоянно
                try:
                    if self.stop: break
                    conn, addr = self.sock.accept()
                    # print("New connection from " + addr[0])
                except:
                    continue
                try:
                    self.parse(conn, addr)
                except:
                    self.send_answer(conn, "500 Internal Server Error", data="Error")
                finally:
                    # так при любой ошибке
                    # сокет закроем корректно
                    conn.close()
        finally:
            self.sock.close()
            # так при возникновении любой ошибки сокет
            # всегда закроется корректно и будет всё хорошо
