# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'elo.db'

# Initialize database function
def initialize_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                score INTEGER DEFAULT 1000,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY,
                item1_id INTEGER,
                item2_id INTEGER,
                winner_id INTEGER,
                timestamp TEXT,
                FOREIGN KEY (item1_id) REFERENCES items (id),
                FOREIGN KEY (item2_id) REFERENCES items (id),
                FOREIGN KEY (winner_id) REFERENCES items (id)
            )
        ''')
        conn.commit()

# Route to display index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_names = request.form.get('items', '').splitlines()
        if item_names:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                for name in item_names:
                    cursor.execute('INSERT OR IGNORE INTO items (name) VALUES (?)', (name,))
                conn.commit()
        return redirect(url_for('compare'))
    return render_template('index.html')

# Route to display compare page
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'GET':
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items ORDER BY RANDOM() LIMIT 2')
            items = cursor.fetchall()
            if len(items) == 2:
                return render_template('compare.html', item1=items[0], item2=items[1])
            else:
                return render_template('compare.html', item1=None, item2=None)

    elif request.method == 'POST':
        item1_id = request.form.get('item1_id')
        item2_id = request.form.get('item2_id')
        winner_id = request.form.get('winner_id')
        if not item1_id or not item2_id or not winner_id:
            return redirect(url_for('compare'))  # Redirect if keys are missing

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO comparisons (item1_id, item2_id, winner_id, timestamp) VALUES (?, ?, ?, ?)',
                           (item1_id, item2_id, winner_id, timestamp))
            conn.commit()

        return redirect(url_for('compare'))

# Route to display results page
@app.route('/results')
def results():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.timestamp, i1.name, i2.name
            FROM comparisons c
            INNER JOIN items i1 ON c.item1_id = i1.id
            INNER JOIN items i2 ON c.item2_id = i2.id
            ORDER BY c.timestamp DESC
            LIMIT 10
        ''')
        timestamps = cursor.fetchall()
    return render_template('results.html', timestamps=timestamps)

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0')
