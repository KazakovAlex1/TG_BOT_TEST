# keep_alive.py
from flask import Flask, Response
from threading import Thread
import os
import logging

# Отключаем логи Flask, чтобы не засорять ответ
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Минимальный ответ для проверки здоровья
@app.route('/health')
def health():
    # Возвращаем просто HTTP 200 без тела ответа
    return Response(status=200)

@app.route('/')
def home():
    # Для главной страницы тоже минимальный ответ
    return Response("OK", status=200, mimetype='text/plain')

def run():
    port = int(os.environ.get('PORT', 8080))
    # Запускаем без лишних логов
    app.run(host='0.0.0.0', port=port, threaded=True)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True  # Поток завершится вместе с основным
    t.start()