from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from elo import ELO
import random
from datetime import datetime

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elo_comparisons.db'
db = SQLAlchemy(app)

elo_system = ELO()
version = "0.1.1.dev"

class Comparison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    comparison_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.Column(db.Text, nullable=False)
    matches = db.Column(db.Text, nullable=True)
    results = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

@app.context_processor
def utility_processor():
    def enumerate_function(seq):
        return enumerate(seq, start=1)
    return dict(enumerate=enumerate_function, version=version)

@app.route('/')
def index():
    return render_template('index.html', version=version)

@app.route('/add_items', methods=['POST'])
def add_items():
    global elo_system
    elo_system = ELO()
    username = request.form.get('username')
    comparison_name = request.form.get('comparison_name')
    items = request.form.get('items').splitlines()

    for item in items:
        elo_system.add_item(item)

    comparison = Comparison(username=username, comparison_name=comparison_name, items='\n'.join(items))
    db.session.add(comparison)
    db.session.commit()

    return redirect(url_for('compare', comparison_id=comparison.id, version=version))

@app.route('/compare/<int:comparison_id>')
def compare(comparison_id):
    comparison = Comparison.query.get_or_404(comparison_id)
    items = list(elo_system.items.keys())

    if len(items) < 2:
        return redirect(url_for('index', version=version))

    random.shuffle(items)

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if (items[i], items[j]) not in elo_system.matches and (items[j], items[i]) not in elo_system.matches:
                return render_template('compare.html', item1=items[i], item2=items[j], comparison_id=comparison_id, version=version)

    return redirect(url_for('results', comparison_id=comparison_id, version=version))

@app.route('/submit_match', methods=['POST'])
def submit_match():
    global elo_system
    winner = request.form['winner']
    loser = request.form['loser']
    comparison_id = request.form['comparison_id']
    comparison = Comparison.query.get_or_404(comparison_id)

    elo_system.add_match(winner, loser)
    comparison.matches = str(elo_system.matches)
    db.session.commit()

    return jsonify(success=True)

@app.route('/results/<int:comparison_id>')
def results(comparison_id):
    global elo_system
    comparison = Comparison.query.get_or_404(comparison_id)
    elo_system.calculate_elo()
    ranking = elo_system.get_ranking()

    comparison.results = str(ranking)
    db.session.commit()

    return render_template('results.html', ranking=ranking, comparison_id=comparison_id, version=version)

@app.route('/previous_comparisons')
def previous_comparisons():
    comparisons = Comparison.query.order_by(Comparison.timestamp.desc()).all()
    return render_template('previous_comparisons.html', comparisons=comparisons, version=version)

@app.route('/reset_votes/<int:comparison_id>')
def reset_votes(comparison_id):
    global elo_system
    elo_system.matches = []
    comparison = Comparison.query.get_or_404(comparison_id)
    comparison.matches = ''
    db.session.commit()

    return redirect(url_for('compare', comparison_id=comparison_id, version=version))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
