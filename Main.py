# -*- coding: utf-8 -*-
from HTTPServer import Server
from machine import Pin
import network

# Конфигурация
SSID = "YOUR_WIFI"  # Tumasov-MikroTik-2.4GHz
SSID_PASSWORD = "YOUR_WIFI_PASSWORD"
SERVER_PORT = 80

# Код подключения к Wi-Fi
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('Подключение к Wi-Fi сети...')
    sta_if.active(True)
    sta_if.connect(SSID, SSID_PASSWORD)
    while not sta_if.isconnected():
        pass
print('Подключено к Wi-Fi:\n', sta_if.ifconfig(), end='\n')

# Настройка пинов
relay = Pin(0, Pin.OUT)  # Присваиваем переменной led GPIO0 и назначаем его выходом
relay.value(0)  # Переводим пин в состояние 0

# Фнкции веб-сервера
def on():  # Включаем реле
    relay.value(1)
    return 'Реле включено'


def off():  # Выключаем реле
    relay.value(0)
    return 'Реле отключено'


def stop():  # Остановка сервера.
    server.stop = True
    return 'Сервер остановлен'


def free():  # Показывает в браузере состояние памяти.
    result = "Свободно ОЗУ: " + str(gc.mem_free()) + " Выделено ОЗУ: " + str(gc.mem_alloc())
    return result


def switch():  # Просто переключает состояние реле
    relay.value(not relay.value())
    return 'Новое состояние реле: ' + str(relay.value())


# Настройка веб-сервера
server = Server(SERVER_PORT)  # Создаём объект сервера
server.RouteAdd('/on', on) # http://[esp8266]/stop
server.RouteAdd('/off', off)
server.RouteAdd('/stop', stop)
server.RouteAdd('/switch', switch)
server.RouteAdd('/free', free)
server.Run()  # Запуск веб-сервера
