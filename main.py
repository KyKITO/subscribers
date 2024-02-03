import random
import psycopg2
import time
from datetime import datetime
import json

# Открываем файл с настройками подключения в формате JSON
with open('config.json') as json_file:
    config = json.load(json_file)

# Извлекаем значения из JSON файла

# Переменные для подключения к БД
db_config = config['DbConfig']
host = db_config['host']
port = db_config['port']
database = db_config['database']
user = db_config['user']
password = db_config['password']

# Переменные для кол-во подписчиков
countMin = config['BusinessConfig']['Subscribe']['min']
countMax = config['BusinessConfig']['Subscribe']['max']

# Переменная для региона
REGION = config['Region']

# Переменные для частоты
frequencyMin = config['BusinessConfig']['Frequency']['min']
frequencyMax = config['BusinessConfig']['Frequency']['max']
# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)


# Генерация рандомного числа от 0 до 50
def generate_count():
    return random.randint(int(countMin), int(countMax))

# Отправка записи в базу данных
def send_to_db(region, count):
    cursor = conn.cursor()

    # Вставка новой записи в таблицу
    sql = "INSERT INTO subscribers (region, count, updatedatetime) VALUES (%s, %s, %s)"
    data = (region, count, datetime.now())
    cursor.execute(sql, data)

    conn.commit()
    cursor.close()

# Главная функция приложен
def main():
    while True:
        # Генерация частоты отправки в базу данных
        frequency = random.randint(int(frequencyMin), int(frequencyMax))

        # Генерация рандомного числа
        count = generate_count()

        # Отправка записи в базу данных
        send_to_db(REGION, count)

        print("Запись отправлена в базу данных:", REGION, count, datetime.now())

        # Задержка перед следующей отправкой
        time.sleep(frequency)

if __name__ == "__main__":
    main()