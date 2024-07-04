from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Entry

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

