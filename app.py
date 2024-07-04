from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS user_input (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL
)''')
conn.commit()

@app.route('/')
def index():
    # Get all saved data
    c.execute('SELECT * FROM user_input')
    data = c.fetchall()
    return render_template('index.html', data=data)

@app.route('/save', methods=['POST'])
def save():
    # Get user input from form
    user_data = request.form['user_input']
    
    # Save data to database
    c.execute('INSERT INTO user_input (data) VALUES (?)', (user_data,))
    conn.commit()
    
    # Show success message
    return f"Data saved successfully! <a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)
