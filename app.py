from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import itertools
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLite database connection
conn = sqlite3.connect('db/elo.db', check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER DEFAULT 1000,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    items = request.form['items'].strip().split('\n')
    
    for item in items:
        c.execute("INSERT OR IGNORE INTO items (name) VALUES (?)", (item,))
    conn.commit()
    
    return redirect(url_for('next_comparison'))

@app.route('/compare/<int:item1_id>/<int:item2_id>', methods=['GET', 'POST'])
def do_comparison(item1_id, item2_id):
    if request.method == 'POST':
        winner_id = int(request.form['winner'])
        loser_id = item1_id if winner_id == item2_id else item2_id
        
        update_elo(item1_id, item2_id, winner_id)
        
        return redirect(url_for('next_comparison'))
    
    c.execute("SELECT name FROM items WHERE id=?", (item1_id,))
    item1_name = c.fetchone()[0]
    c.execute("SELECT name FROM items WHERE id=?", (item2_id,))
    item2_name = c.fetchone()[0]
    
    return render_template('compare.html', item1_id=item1_id, item2_id=item2_id,
                           item1_name=item1_name, item2_name=item2_name)

def update_elo(item1_id, item2_id, winner_id):
    c.execute("SELECT score FROM items WHERE id=?", (item1_id,))
    item1_score = c.fetchone()[0]
    c.execute("SELECT score FROM items WHERE id=?", (item2_id,))
    item2_score = c.fetchone()[0]
    
    K = 32
    
    if winner_id == item1_id:
        S1 = 1
        S2 = 0
    else:
        S1 = 0
        S2 = 1
    
    E1 = 1 / (1 + 10**((item2_score - item1_score) / 400))
    E2 = 1 / (1 + 10**((item1_score - item2_score) / 400))
    
    new_item1_score = item1_score + K * (S1 - E1)
    new_item2_score = item2_score + K * (S2 - E2)
    
    c.execute("UPDATE items SET score=?, wins=wins+?, losses=losses+? WHERE id=?",
              (new_item1_score, S1, S2, item1_id))
    c.execute("UPDATE items SET score=?, wins=wins+?, losses=losses+? WHERE id=?",
              (new_item2_score, S2, S1, item2_id))
    conn.commit()

@app.route('/next')
def next_comparison():
    c.execute("SELECT id FROM items")
    items = c.fetchall()
    
    pairs = list(itertools.combinations(items, 2))
    
    if len(pairs) > 0:
        random.shuffle(pairs)
        
        item1_id, item2_id = pairs[0][0][0], pairs[0][1][0]  # Adjust here
        
        return redirect(url_for('do_comparison', item1_id=item1_id, item2_id=item2_id))
    else:
        return redirect(url_for('results'))

@app.route('/results')
def results():
    c.execute("SELECT id, name, score, wins FROM items ORDER BY score DESC")
    ranked_items = c.fetchall()
    
    return render_template('results.html', ranked_items=ranked_items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
