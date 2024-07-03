# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import sqlite3

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
        item1_id = request.form['item1_id']
        item2_id = request.form['item2_id']
        winner_id = request.form['winner_id']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO comparisons (item1_id, item2_id, winner_id, timestamp) VALUES (?, ?, ?, ?)',
                           (item1_id, item2_id, winner_id, timestamp))
            conn.commit()

        return redirect(url_for('compare'))

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0')
