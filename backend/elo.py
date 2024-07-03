class EloRank:
    def __init__(self, k_factor=32):
        self.k_factor = k_factor

    def expected_result(self, rating_a, rating_b):
        expect_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        expect_b = 1 / (1 + 10 ** ((rating_a - rating_b) / 400))
        return expect_a, expect_b

    def rate_1vs1(self, rating_a, rating_b):
        expect_a, expect_b = self.expected_result(rating_a, rating_b)
        new_rating_a = rating_a + self.k_factor * (1 - expect_a)
        new_rating_b = rating_b + self.k_factor * (0 - expect_b)
        return new_rating_a, new_rating_b
