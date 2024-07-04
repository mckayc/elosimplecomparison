from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@db/elocompare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your database model (e.g., Entry)
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

# Routes and other application logic
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    content = request.form['content']
    new_entry = Entry(title=title, content=content)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('submission', title=title, content=content))

@app.route('/submission')
def submission():
    title = request.args.get('title')
    content = request.args.get('content')
    return render_template('submission.html', title=title, content=content)

@app.route('/entries')
def entries():
    entries = Entry.query.all()
    return render_template('entries.html', entries=entries)

# Ensure app.run() is only executed when this script is directly run
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
