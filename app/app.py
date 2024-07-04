from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# SQLite Database Setup
def create_db():
    conn = sqlite3.connect('app/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 content TEXT NOT NULL,
                 timestamp TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_db()

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('app/database.db')
        c = conn.cursor()
        c.execute('INSERT INTO entries (title, content, timestamp) VALUES (?, ?, ?)',
                  (title, content, timestamp))
        conn.commit()
        conn.close()

        return redirect(url_for('submission'))

    return render_template('index.html')

@app.route('/submission')
def submission():
    conn = sqlite3.connect('app/database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM entries ORDER BY timestamp DESC')
    entries = c.fetchall()
    conn.close()

    return render_template('submission.html', entries=entries)

@app.route('/entries/<title>')
def show_entries(title):
    conn = sqlite3.connect('app/database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM entries WHERE title=? ORDER BY timestamp DESC', (title,))
    entries = c.fetchall()
    conn.close()

    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
