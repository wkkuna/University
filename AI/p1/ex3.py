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

    def __init__(self, ranks0=range(2, 11), ranks1=range(11, 15), colours0=range(0, 4), colours1=range(0, 4)):
        self.deck0 = [[r, c] for r in ranks0 for c in colours0]
        self.deck1 = [[r, c] for r in ranks1 for c in colours1]

    def draw_hand(self, deck=0):
        return sample(self.deck1, 5) if deck == 1 else sample(self.deck0, 5)

    def get_hand_ranking(self, hand):
        hand = sorted(hand, key=lambda x: x[0], reverse=True)
        colour = [1]*5
        ascending = [1]*5
        one_rank = [1]*5

        prev_card = hand[0]
        for i, card in enumerate(hand[1:], 1):
            if prev_card[1] == card[1]:
                colour[i] = colour[i-1] + 1

            if prev_card[0] == card[0]:
                one_rank[i] = one_rank[i-1] + 1

            if prev_card[0] - 1 == card[0]:
                ascending[i] = ascending[i-1] + 1

            prev_card = card

        max_colour = max(colour)
        max_ascending = max(ascending)
        max_one_rank = max(one_rank)

        if max_ascending == 5 and max_colour == 5:
            return self.hand_rankings['Straight flush']

        if max_one_rank == 4:
            return self.hand_rankings['Four of a kind']

        if max_one_rank == 3 and 2 in one_rank:
            return self.hand_rankings['Full house']

        if max_colour == 5:
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

    # returns the hand number of a winner
    def determine_winner(self, hand0, hand1):
        ranking0 = self.get_hand_ranking(hand0)
        ranking1 = self.get_hand_ranking(hand1)

        if ranking0 == ranking1:
            return int(hand1[0][0] > hand0[0][0])

        return int(ranking1 > ranking0)


def estimate_winning_probability(sample, blotkarz_deck=range(2, 11), blotkarz_colours=range(0, 4)):
    print("Running tests with blotkarz deck {} and blotkarz colours {}".format(
        blotkarz_deck, blotkarz_colours))
    pt = PokerTable(ranks0=blotkarz_deck, colours0=blotkarz_colours)
    win_count = 0

    for _ in range(sample):
        blotkarz_hand = pt.draw_hand()
        figurant_hand = pt.draw_hand(1)

        win_count += pt.determine_winner(figurant_hand, blotkarz_hand)

    print("The tests estimate the possibility of Blotkarz's win at {}%".format(
        (win_count/sample)*100))


if __name__ == "__main__":
    estimate_winning_probability(10000, blotkarz_deck=range(2, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(3, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(4, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(5, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(6, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(7, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(8, 11))
    estimate_winning_probability(10000, blotkarz_deck=range(
        2, 11), blotkarz_colours=range(0, 3))
    estimate_winning_probability(10000, blotkarz_deck=range(
        2, 11), blotkarz_colours=range(0, 2))
    estimate_winning_probability(10000, blotkarz_deck=range(
        3, 11), blotkarz_colours=range(0, 3))
    estimate_winning_probability(10000, blotkarz_deck=range(
        3, 11), blotkarz_colours=range(0, 2))
    estimate_winning_probability(10000, blotkarz_deck=range(
        6, 11), blotkarz_colours=range(0, 2))
    pass
