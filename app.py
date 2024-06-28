from flask import Flask, render_template, request, redirect, url_for, jsonify
from elo import ELO
import random

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

elo_system = ELO()

@app.context_processor
def utility_processor():
    def enumerate_function(seq):
        return enumerate(seq, start=1)
    return dict(enumerate=enumerate_function)

@app.route('/')
def index():
    # Reset the ELO system
    global elo_system
    elo_system = ELO()
    return render_template('index.html')

@app.route('/add_items', methods=['POST'])
def add_items():
    items = request.form.get('items').splitlines()
    for item in items:
        elo_system.add_item(item)
    return redirect(url_for('compare'))

@app.route('/compare')
def compare():
    items = list(elo_system.items.keys())
    if len(items) < 2:
        return redirect(url_for('index'))

    # Shuffle the items to randomize the order of comparisons
    random.shuffle(items)

    # Calculate the total number of comparisons
    num_total_compares = len(items) * (len(items) - 1) // 2
    num_comparison = len(elo_system.matches)

    # Find a pair of items that haven't been compared yet
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if (items[i], items[j]) not in elo_system.matches and (items[j], items[i]) not in elo_system.matches:
                return render_template('compare.html', item1=items[i], item2=items[j], num_comparison=num_comparison, num_total_compares=num_total_compares)

    return redirect(url_for('results'))

@app.route('/submit_match', methods=['POST'])
def submit_match():
    winner = request.form['winner']
    loser = request.form['loser']
    elo_system.add_match(winner, loser)
    return jsonify(success=True)

@app.route('/results')
def results():
    elo_system.calculate_elo()
    ranking = elo_system.get_ranking()
    return render_template('results.html', ranking=ranking)

@app.route('/reset_votes')
def reset_votes():
    elo_system.matches = []
    return redirect(url_for('compare'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
