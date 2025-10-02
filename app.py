from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Инициализация базы данных при старте
@app.before_first_request
def initialize():
    db.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stats = db.get_weekly_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/add-coffee', methods=['GET', 'POST'])
def add_coffee():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        drink_id = request.form.get('drink_id')
        notes = request.form.get('notes', '')
        
        if employee_id and drink_id:
            db.log_coffee_consumption(int(employee_id), int(drink_id), notes)
            flash('Кофе успешно добавлен! ☕', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Пожалуйста, выберите сотрудника и напиток', 'error')
    
    # Получаем списки сотрудников и напитков для формы
    conn = db.sqlite3.connect('coffee_tracker.db')
    c = conn.cursor()
    
    c.execute('SELECT id, name FROM employees ORDER BY name')
    employees = c.fetchall()
    
    c.execute('SELECT id, name, cost FROM drinks ORDER BY name')
    drinks = c.fetchall()
    
    conn.close()
    
    return render_template('add_coffee.html', employees=employees, drinks=drinks)

if __name__ == '__main__':
    app.run(debug=True)
