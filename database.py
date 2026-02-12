import sqlite3


class Database():
    """Класс для работы с базой данных SQLite."""
    def __init__(self, db_name='todo.db'):
        """При создании объекта открываем соединение с БД."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Устанавливаем соединение с БД."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        """Закрываем соединение с Бд."""
        if self.conn:
            self.conn.close()
    
    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                is_done INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def add_task(self, user_id : int, task : str):
        """Добавляет новую задачу."""
        query = """
            INSERT INTO tasks(user_id, task)
            VALUES(?,?)
        """
        self.cursor.execute(query, (user_id, task))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_tasks(self, user_id : int):
        """Возвращает список задач пользователя."""
        query = """
            SELECT  id, task, is_done
            FROM tasks
            WHERE user_id = ?
            ORDER BY is_done, created_at DESC
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def toggle_task(self, task_id : int):
        """Отмечает задачу выполненной/невыполненной."""
        query = """
        UPDATE tasks
        SET is_done = NOT is_done
        WHERE id = ?
        """
        self.cursor.execute(query, (task_id,))
        self.conn.commit()

    def delete_task(self, task_id : int):
        """Удаляет конкретную задачу."""
        query = """
        DELETE FROM tasks
        WHERE id = ?
        """
        self.cursor.execute(query, (task_id,))
        self.conn.commit()
    
    def delete_all_tasks(self, user_id : int):
        """Удаляет все задачи пользователя."""
        query = "DELETE FROM tasks WHERE user_id = ?"
        
        self.cursor.execute(query,(user_id,) )
        self.conn.commit()
    
    def __enter__(self):
        """Контекстный менеджер: автоматически открываем соединение."""
        self.connect()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()