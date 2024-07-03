from flask import Flask, render_template, request, redirect, url_for
from elo import EloRank
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize ELO ranking system
elo = EloRank()

# SQLite database connection
conn = sqlite3.connect('backend/database.db', check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        score INTEGER DEFAULT 1000
    )
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_items', methods=['POST'])
def add_items():
    items = request.form['items'].strip().split('\n')
    
    for item in items:
        cursor.execute('INSERT INTO items (name) VALUES (?)', (item,))
        conn.commit()
    
    return redirect(url_for('compare'))

@app.route('/compare')
def compare():
    cursor.execute('SELECT * FROM items ORDER BY RANDOM() LIMIT 2')
    items = cursor.fetchall()
    return render_template('compare.html', item1=items[0], item2=items[1])

@app.route('/vote/<winner>/<loser>', methods=['POST'])
def vote(winner, loser):
    winner_id = int(winner)
    loser_id = int(loser)
    
    winner_score, loser_score = elo.rate_1vs1(1000, 1000)
    
    cursor.execute('UPDATE items SET score = ? WHERE id = ?', (winner_score, winner_id))
    cursor.execute('UPDATE items SET score = ? WHERE id = ?', (loser_score, loser_id))
    conn.commit()
    
    return redirect(url_for('compare'))

@app.route('/results')
def results():
    cursor.execute('SELECT * FROM items ORDER BY score DESC')
    items = cursor.fetchall()
    return render_template('results.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
