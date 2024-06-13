# We draw hands randomly for each player
# s times and count the probability by
# wins / no of games.

# The best deck (experimentally):
# Blotkarz deck range(8, 11) and colors range(0, 4)
# Possibility of Blotkarz's win 53.84%

# We don't have to compare all poker rankings
# since some of them are not even possible
# (like royal flush)

from random import sample


class PokerTable:
    hand_rankings = {
        'Straight flush': 8,
        'Four of a kind': 7,
        'Full house': 6,
        'Flush': 5,
        'Straight': 4,
        'Three of a kind': 3,
        'Two pair': 2,
        'One pair': 1,
        'High card': 0
    }

    def __init__(self, ranks0=range(2, 11), ranks1=range(11, 15), colors0=range(0, 4), colors1=range(0, 4)):
        self.deck0 = [[r, c] for r in ranks0 for c in colors0]
        self.deck1 = [[r, c] for r in ranks1 for c in colors1]

    def draw_hand(self, deck="blotkarz"):
        return sample(self.deck1, 5) if deck == "figurant" else sample(self.deck0, 5)

    def get_hand_ranking(self, hand):
        hand = sorted(hand, key=lambda x: x[0], reverse=True)
        color = [1]*5
        ascending = [1]*5
        one_rank = [1]*5

        prev_card = hand[0]
        for i, card in enumerate(hand[1:], 1):
            # Number of cards of each color
            if prev_card[1] == card[1]:
                color[i] = color[i-1] + 1

            # How many cards of the same rank
            if prev_card[0] == card[0]:
                one_rank[i] = one_rank[i-1] + 1

            # How many ascending cards
            if prev_card[0] - 1 == card[0]:
                ascending[i] = ascending[i-1] + 1

            prev_card = card

        max_color = max(color)
        max_ascending = max(ascending)
        max_one_rank = max(one_rank)

        if max_ascending == 5 and max_color == 5:
            return self.hand_rankings['Straight flush']

        if max_one_rank == 4:
            return self.hand_rankings['Four of a kind']

        if max_one_rank == 3 and 2 in one_rank:
            return self.hand_rankings['Full house']

        if max_color == 5:
            return self.hand_rankings['Flush']

        if max_ascending == 5:
            return self.hand_rankings['Straight']

        if max_one_rank == 3:
            return self.hand_rankings['Three of a kind']

        if max_one_rank == 2 and one_rank.count(2) == 2:
            return self.hand_rankings['Two pair']

        if max_one_rank == 2:
            return self.hand_rankings['One pair']

        return self.hand_rankings['High card']

    # Returns the hand number of a winner
    def determine_winner(self, hand0, hand1):
        ranking0 = self.get_hand_ranking(hand0)
        ranking1 = self.get_hand_ranking(hand1)

        # If the ranking is the same, the highest card wins
        if ranking0 == ranking1:
            for r in range(5):
                if hand1[0][r] != hand0[0][r]:
                    return int(hand1[0][0] > hand0[0][0])
            return 0

        return int(ranking1 > ranking0)


def win_probability(sample, blotkarz_deck=range(2, 11), blotkarz_colors=range(0, 4)):
    print(f"Blotkarz deck {blotkarz_deck} and colors {blotkarz_colors}")
    pt = PokerTable(ranks0=blotkarz_deck, colors0=blotkarz_colors)
    wins = 0

    for _ in range(sample):
        blotkarz_hand = pt.draw_hand()
        figurant_hand = pt.draw_hand("figurant")

        wins += pt.determine_winner(figurant_hand, blotkarz_hand)

    print(f"Possibility of Blotkarz's win {wins / sample * 100}%")


if __name__ == "__main__":
    s = 10000
    win_probability(s, range(2, 11))
    win_probability(s, range(3, 11))
    win_probability(s, range(4, 11))
    win_probability(s, range(5, 11))
    win_probability(s, range(6, 11))
    win_probability(s, range(7, 11))
    win_probability(s, range(8, 11))
    win_probability(s, range(2, 11), range(0, 3))
    win_probability(s, range(2, 11), range(0, 2))
    win_probability(s, range(3, 11), range(0, 3))
    win_probability(s, range(3, 11), range(0, 2))
    win_probability(s, range(6, 11), range(0, 2))
