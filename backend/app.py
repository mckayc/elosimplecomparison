from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from elo import rate_1vs1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/elocompare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User, Comparison, Item

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    username = request.form['username']
    title = request.form['title']
    items = request.form['items'].splitlines()
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    comparison = Comparison(title=title, user_id=user.id, timestamp=datetime.now())
    db.session.add(comparison)
    db.session.commit()

    for item_name in items:
        item = Item(name=item_name, comparison_id=comparison.id)
        db.session.add(item)
    
    db.session.commit()

    return render_template('compare.html', comparison_id=comparison.id)

@app.route('/compare_items', methods=['POST'])
def compare_items():
    item1_id = request.form['item1_id']
    item2_id = request.form['item2_id']
    winner_id = request.form['winner_id']

    item1 = Item.query.get(item1_id)
    item2 = Item.query.get(item2_id)
    winner = Item.query.get(winner_id)

    if winner_id == item1_id:
        loser = item2
    else:
        loser = item1

    item1_score = item1.score
    item2_score = item2.score

    item1_new_score, item2_new_score = rate_1vs1(item1_score, item2_score, winner == item1)

    item1.score = item1_new_score
    item2.score = item2_new_score

    db.session.commit()

    return jsonify(success=True)

@app.route('/results/<int:comparison_id>')
def results(comparison_id):
    comparison = Comparison.query.get(comparison_id)
    items = Item.query.filter_by(comparison_id=comparison_id).order_by(Item.score.desc()).all()
    return render_template('results.html', items=items, title=comparison.title)

@app.route('/history')
def history():
    comparisons = Comparison.query.all()
    return render_template('history.html', comparisons=comparisons)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
