import random
import time
from datetime import datetime
import psycopg2

# Параметры подключения к базе данных PostgreSQL
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "subscribes"
DB_USER = "postgres"
DB_PASSWORD = "5433"

# Название региона
REGION = "USA"

# Генерация рандомного числа от 0 до 50
def generate_count():
    return random.randint(0, 50)

# Отправка записи в базу данных
def send_to_db(region, count):
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()

    # Вставка новой записи в таблицу
    sql = "INSERT INTO subscribers (region, count, updatedatetime) VALUES (%s, %s, %s)"
    data = (region, count, datetime.now())
    cursor.execute(sql, data)

    conn.commit()
    cursor.close()
    conn.close()

# Главная функция приложения
def main():
    while True:
        # Генерация частоты отправки в базу данных
        frequency = random.randint(60, 300)

        # Генерация рандомного числа
        count = generate_count()

        # Отправка записи в базу данных
        send_to_db(REGION, count)

        print("Запись отправлена в базу данных:", REGION, count, datetime.now())

        # Задержка перед следующей отправкой
        time.sleep(frequency)

if __name__ == "__main__":
    main()