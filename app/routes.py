from flask import render_template, redirect, url_for, request
from app import app, db
from app.models import Entry
from app.forms import EntryForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(title=form.title.data, content=form.content.data)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))
    return render_template('index.html', form=form)

@app.route('/entries')
def entries():
    entries = Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('entries.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    return render_template('entry.html', entry=entry)
