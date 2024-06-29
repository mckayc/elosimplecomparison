from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from elo import ELO
import random

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

VERSION = "0.1.2b"  # Define the version here

elo_system = ELO()

@app.context_processor
def utility_processor():
    def enumerate_function(seq):
        return enumerate(seq, start=1)
    return dict(enumerate=enumerate_function, version=VERSION)

@app.route('/')
def index():
    global elo_system
    elo_system = ELO()
    session.clear()  # Clear the session when starting over
    print("Session cleared")
    return render_template('index.html')

@app.route('/add_items', methods=['POST'])
def add_items():
    items = request.form.get('items').splitlines()
    for item in items:
        elo_system.add_item(item)
    session['items'] = items  # Store items in session
    session['matches'] = []  # Initialize matches in session
    print("Items added:", items)
    return redirect(url_for('compare'))

@app.route('/compare')
def compare():
    items = session.get('items', [])
    if len(items) < 2:
        return redirect(url_for('index'))

    # Shuffle the items to randomize the order of comparisons
    random.shuffle(items)

    # Find a pair of items that haven't been compared yet
    matches = session.get('matches', [])
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if (items[i], items[j]) not in matches and (items[j], items[i]) not in matches:
                return render_template('compare.html', item1=items[i], item2=items[j], num_comparison=len(matches) + 1, num_total_compares=(len(items) * (len(items) - 1)) // 2)

    return redirect(url_for('results'))

@app.route('/submit_match', methods=['POST'])
def submit_match():
    winner = request.form['winner']
    loser = request.form['loser']
    elo_system.add_match(winner, loser)

    matches = session.get('matches', [])
    matches.append((winner, loser))
    session['matches'] = matches  # Update matches in session
    print("Match submitted:", winner, "vs", loser)

    return jsonify(success=True)

@app.route('/results')
def results():
    elo_system.calculate_elo()
    ranking = elo_system.get_ranking()
    print("ELO rankings:", ranking)
    return render_template('results.html', ranking=ranking)

@app.route('/reset_votes')
def reset_votes():
    global elo_system
    elo_system = ELO()  # Reset the ELO system
    session['matches'] = []  # Clear matches in session
    print("Votes reset")
    return redirect(url_for('compare'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
