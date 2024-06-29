import pickle

class ELO:
    def __init__(self, k=32):
        self.k = k
        self.items = {}
        self.matches = []

    def add_item(self, item):
        if item not in self.items:
            self.items[item] = 1000

    def add_match(self, winner, loser):
        self.matches.append((winner, loser))

    def calculate_elo(self):
        for winner, loser in self.matches:
            winner_rating = self.items[winner]
            loser_rating = self.items[loser]

            expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
            expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))

            self.items[winner] += self.k * (1 - expected_winner)
            self.items[loser] += self.k * (0 - expected_loser)

    def get_ranking(self):
        return sorted(self.items.items(), key=lambda item: item[1], reverse=True)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
