from flask import Flask, request, render_template, redirect, url_for
import MySQLdb

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'elocompareuser'
app.config['MYSQL_PASSWORD'] = 'elocomparepass'
app.config['MYSQL_DB'] = 'elocompare'

def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Initialize database connection
db = get_db_connection()

# Routes

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    return render_template('index.html', items=items)

@app.route('/compare')
def compare():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    return render_template('compare.html', items=items)

@app.route('/results')
def results():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM items ORDER BY id')
    items = cursor.fetchall()
    cursor.close()
    return render_template('results.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    title = request.form['title']
    item = request.form['item']
    cursor = db.cursor()
    cursor.execute('INSERT INTO items (title, name) VALUES (%s, %s)', (title, item))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
