from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import quote  # Use quote from urllib.parse instead of url_quote

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_entry = Entry(title=title, content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('display', entry_id=new_entry.id))
    return render_template('index.html')

@app.route('/display/<int:entry_id>')
def display(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('display.html', entry=entry, entries=entries)

@app.route('/entries')
def entries():
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
