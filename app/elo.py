# elo.py
class EloRanking:
    def __init__(self):
        self.k_factor = 32
        self.items = {}

    def add_item(self, item):
        self.items[item] = 1000  # Initial ELO score

    def get_score(self, item):
        return self.items.get(item, 1000)

    def record_result(self, winner, loser):
        expected_winner = 1 / (1 + 10 ** ((self.items[loser] - self.items[winner]) / 400))
        expected_loser = 1 - expected_winner

        self.items[winner] += self.k_factor * (1 - expected_winner)
        self.items[loser] += self.k_factor * (0 - expected_loser)
