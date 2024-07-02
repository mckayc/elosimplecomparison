from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from elo import calculate_elo

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'elocompare'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        items = request.form['items'].splitlines()
        session['title'] = title
        session['items'] = items
        for item in items:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO items (title, name) VALUES (%s, %s)', (title, item))
            mysql.connection.commit()
        return redirect(url_for('compare'))
    return render_template('index.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        item1 = request.form['item1']
        item2 = request.form['item2']
        winner = request.form['winner']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO comparisons (title, item1, item2, winner) VALUES (%s, %s, %s, %s)',
                       (session['title'], item1, item2, winner))
        mysql.connection.commit()
        calculate_elo(item1, item2, winner, mysql)
        return redirect(url_for('compare'))
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT name FROM items WHERE title = %s', [session['title']])
        items = cursor.fetchall()
        item1, item2 = random.sample([item['name'] for item in items], 2)
        return render_template('compare.html', item1=item1, item2=item2)

@app.route('/results')
def results():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT name, elo_rating FROM items WHERE title = %s ORDER BY elo_rating DESC', [session['title']])
    items = cursor.fetchall()
    return render_template('results.html', items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
