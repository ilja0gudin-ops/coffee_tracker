import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('coffee_tracker.db')
    c = conn.cursor()
    
    # Таблица сотрудников
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            department TEXT,
            email TEXT
        )
    ''')
    
    # Таблица напитков
    c.execute('''
        CREATE TABLE IF NOT EXISTS drinks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cost REAL NOT NULL,
            caffeine_mg INTEGER
        )
    ''')
    
    # Таблица потребления
    c.execute('''
        CREATE TABLE IF NOT EXISTS coffee_consumption (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            drink_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (id),
            FOREIGN KEY (drink_id) REFERENCES drinks (id)
        )
    ''')
    
    # Наполняем начальными данными
    employees = [
        ('Иван Петров', 'Разработка', 'ivan@company.com'),
        ('Мария Сидорова', 'Маркетинг', 'maria@company.com'),
        ('Алексей Козлов', 'Продажи', 'alex@company.com'),
        ('Ольга Новикова', 'HR', 'olga@company.com')
    ]
    
    drinks = [
        ('Эспрессо', 50.0, 80),
        ('Американо', 60.0, 100),
        ('Капучино', 80.0, 80),
        ('Латте', 90.0, 75),
        ('Раф', 100.0, 85)
    ]
    
    c.executemany('INSERT OR IGNORE INTO employees (name, department, email) VALUES (?, ?, ?)', employees)
    c.executemany('INSERT OR IGNORE INTO drinks (name, cost, caffeine_mg) VALUES (?, ?, ?)', drinks)
    
    conn.commit()
    conn.close()

def log_coffee_consumption(employee_id, drink_id, notes=None):
    conn = sqlite3.connect('coffee_tracker.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO coffee_consumption (employee_id, drink_id, notes)
        VALUES (?, ?, ?)
    ''', (employee_id, drink_id, notes))
    conn.commit()
    conn.close()

def get_weekly_stats():
    conn = sqlite3.connect('coffee_tracker.db')
    c = conn.cursor()
    
    # Топ потребителей за неделю
    c.execute('''
        SELECT e.name, COUNT(*) as coffee_count, SUM(d.cost) as total_cost
        FROM coffee_consumption cc
        JOIN employees e ON cc.employee_id = e.id
        JOIN drinks d ON cc.drink_id = d.id
        WHERE cc.timestamp >= datetime('now', '-7 days')
        GROUP BY e.name
        ORDER BY coffee_count DESC
        LIMIT 5
    ''')
    
    top_consumers = c.fetchall()
    
    # Статистика по напиткам
    c.execute('''
        SELECT d.name, COUNT(*) as count
        FROM coffee_consumption cc
        JOIN drinks d ON cc.drink_id = d.id
        WHERE cc.timestamp >= datetime('now', '-7 days')
        GROUP BY d.name
        ORDER BY count DESC
    ''')
    
    drink_stats = c.fetchall()
    
    # Общая статистика
    c.execute('''
        SELECT 
            COUNT(*) as total_cups,
            SUM(d.cost) as total_cost,
            SUM(d.caffeine_mg) as total_caffeine
        FROM coffee_consumption cc
        JOIN drinks d ON cc.drink_id = d.id
        WHERE cc.timestamp >= datetime('now', '-7 days')
    ''')
    
    total_stats = c.fetchone()
    
    conn.close()
    
    return {
        'top_consumers': top_consumers,
        'drink_stats': drink_stats,
        'total_stats': total_stats
    }
