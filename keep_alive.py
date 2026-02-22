# keep_alive.py
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!", 200

@app.route('/health')
def health():
    return "OK", 200

def run():
    # Render сам задает порт через переменную окружения PORT
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    # Запускаем Flask в отдельном потоке, чтобы не мешать основному боту
    t = Thread(target=run)
    t.start()