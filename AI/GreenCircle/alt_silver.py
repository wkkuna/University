import sys
from random import choice
from itertools import combinations

card_type = {
    "training": 0,
    "coding": 1,
    "daily_routine": 2,
    "task_prioritization": 3,
    "architecture_study": 4,
    "continuous_delivery": 5,
    "code_review": 6,
    "refactoring": 7,
}
card_val_to_type = {v: k for k, v in card_type.items()}


class Player:
    def __init__(self, id: int, location: int, score: int, permanent_daily_routine_cards: int, permanent_architecture_study_cards: int) -> None:
        self.id = id
        self.location = location
        self.score = score
        self.permanent_daily_routine_cards = permanent_daily_routine_cards
        self.permanent_architecture_study_cards = permanent_architecture_study_cards


class Applications:
    def __init__(self) -> None:
        self.applications = []
        self.apps = []
        self.combs = []

    def add(self, id, training_needed, coding_needed, daily_routine_needed, task_prioritization_needed,
            architecture_study_needed, continuous_delivery_needed, code_review_needed, refactoring_needed) -> None:
        application = {
            "id": id,
            "training": training_needed,
            "coding": coding_needed,
            "daily_routine": daily_routine_needed,
            "task_prioritization": task_prioritization_needed,
            "architecture_study": architecture_study_needed,
            "continuous_delivery": continuous_delivery_needed,
            "code_review": code_review_needed,
            "refactoring": refactoring_needed,
            "cost": 0,
            "reachable": True,
            "needed_cards": set()
        }
        self.applications.append(application)
        
        app = []
        for card in card_type.keys():
            if application[card]:
                app.append((card, application[card]))

        self.apps.append(app)

    def rank_applications(self, us, cards):
        score = us.score
        hand = cards.get_hand()
        deck_status = cards.deck_status
        ranked_applications = self.applications.copy()
        multiplier = 4 if score < 4 else 2
        bonus_multiplier = 2 if score < 4 else 1

        self.permute_apps(score, cards)
        rank_apps = [c[0] for c in self.combs]
        # print(self.combs, file=sys.stderr, flush=True)
        return rank_apps

        for app in ranked_applications:
            reachable = True
            cost = 0
            for ctype in card_type.keys():
                if not app[ctype]:
                    continue

                app["needed_cards"].add(ctype)
                cost += 0 if app[ctype] < hand[ctype] * \
                    multiplier else app[ctype] - hand[ctype]*multiplier
                if cost > deck_status[ctype]*multiplier + deck_status["bonus"] * bonus_multiplier:
                    reachable = False
            app["cost"] = cost
            app["reachable"] = reachable

        ranked_applications.sort(key=lambda x: x["cost"])
        ranked_applications = [
            app for app in ranked_applications if app["reachable"]]

        return ranked_applications

    def permute_apps(self, score, cards):
        apps_left = 5 - score
        multiplier = 4 if score < 4 else 2

        def is_possible(comb):
            costs = card_type.copy()
            for c in costs:
                costs[c] = 0

            for app in comb:
                for name in card_type:
                    costs[name] += app[name]

            hand = cards.get_hand()
            deck = cards.deck_status

            missing_costs = card_type.copy()

            for name in costs:
                missing_costs[name] = costs[name] - hand[name]*multiplier
                if missing_costs[name] + deck[name] * multiplier + hand["bonus"] < 0:
                    return (False, missing_costs)
            return (True, missing_costs)

        combs = combinations(self.applications, apps_left)
        self.combs = []
        for c in combs:
            possible, missing_costs = is_possible(c)
            if possible:
                self.combs.append((c, missing_costs))

        self.combs.sort(key=lambda item: sum(item[1].values()))


class Cards:
    def __init__(self) -> None:
        self.deck_status = {}
        self.cards_in_use = {}

        for ctype in card_type.keys():
            self.deck_status[ctype] = 5
            self.cards_in_use[ctype] = 0

        self.deck_status["bonus"] = 36

        self.locations = {
            "HAND": [],
            "DRAW": [],
            "DISCARD": [],
            "AUTOMATED": [],
            "OPPONENT_CARDS": [],
            "OPPONENT_AUTOMATED": []
        }

    def add_location(self, location: str, training_cards_count: int, coding_cards_count: int, daily_routine_cards_count: int, task_prioritization_cards_count: int,
                     architecture_study_cards_count: int, continuous_delivery_cards_count: int, code_review_cards_count: int, refactoring_cards_count: int,
                     bonus_cards_count: int, technical_debt_cards_count: int) -> None:
        cards = {
            "training": training_cards_count,
            "coding": coding_cards_count,
            "daily_routine": daily_routine_cards_count,
            "task_prioritization": task_prioritization_cards_count,
            "architecture_study": architecture_study_cards_count,
            "continuous_delivery": continuous_delivery_cards_count,
            "code_review": code_review_cards_count,
            "refactoring": refactoring_cards_count,
            "bonus": bonus_cards_count,
            "technical_debt": technical_debt_cards_count
        }
        self.locations[location] = cards

        for ctype in card_type.keys():
            self.cards_in_use[ctype] += cards[ctype]
            self.deck_status[ctype] -= cards[ctype]
        self.deck_status["bonus"] -= cards[ctype]

    def get_hand(self):
        return self.locations["HAND"]

    def get_riddable_card_set(self, ranked_applications, score):
        bonus_multiplier = 2 if score < 4 else 1
        apps_left = 5 - score
        hand = self.get_hand()

        costs = card_type.copy()
        for c in costs:
            costs[c] = 0

        for i in range(apps_left):
            app = ranked_applications[i]
            for card in card_type.keys():
                costs[card] += app[card]

        if hand["bonus"]:
            costs["bonus"] = hand["bonus"] * bonus_multiplier

        costs = dict(sorted(costs.items(), key=lambda item: item[1]))
        return costs

    def get_needed_card_list(self, ranked_applications, score: int):
        apps_left = 5 - score
        multiplier = 4 if score < 4 else 2
        hand = self.get_hand()
        desirable_cards = []
        # print(apps_left, len(ranked_applications), ranked_applications, file=sys.stderr, flush=True)
        for i in range(apps_left):
            app = ranked_applications[i]
            for card in card_type.keys():
                if not self.deck_status[card]:
                    continue
                id = card_type[card]
                if app[card]:
                    desirable_cards.append(id)

        return list(set(desirable_cards))


class Moves:
    play_card_moves = ["TASK_PRIORITIZATION", "CONTINUOUS_INTEGRATION", "TRAINING",
                       "ARCHITECTURE_STUDY", "CODE_REVIEW", "REFACTORING", "CODING", "DAILY_ROUTINE"]

    def __init__(self) -> None:
        self.moves = {
            "MOVE": [],
            "RELEASE": [],
            "GIVE": [],
            "THROW": [],
            "TASK_PRIORITIZATION": [],
            "CONTINUOUS_INTEGRATION": [],
            "RANDOM": None,
            "WAIT": None,
            "TRAINING": None,
            "ARCHITECTURE_STUDY": None,
            "CODE_REVIEW": None,
            "REFACTORING": None,
            "CODING": None,
            "DAILY_ROUTINE": None,
        }

    def add_possible_move(self, move_type, args) -> None:
        if move_type == "TASK_PRIORITIZATION":
            self.moves[move_type].append((args[0], args[1]))
        elif move_type == "MOVE" and len(args) == 2:
            self.moves[move_type].append((args[0], args[1]))
        elif len(args):
            self.moves[move_type].append(args[0])
        else:
            self.moves[move_type] = True

    def is_possible(self, move_type, args=None) -> bool:
        if args is None:
            return self.moves[move_type] not in [None, []]
        return args in self.moves[move_type]

    def get_any_move(self, mtype):
        if not len(self.moves[mtype]):
            return None
        return choice(self.moves[mtype])

    def get_play_card_number(self, exclude=None) -> int:
        out = 0
        for m in self.play_card_moves:
            if exclude is not None and m in exclude:
                continue
            if self.moves[m] is list:
                out += len(self.moves[m])
            elif self.moves[m] is bool:
                out += 1 if self.moves[m] else 0
        return out


def chose_play_card(moves, ncards, rcards, deck_status, opponent, us, cards):
    # list of tuples; possible plays & their weight
    plays = []
    default_value = 50

    if moves.is_possible("ARCHITECTURE_STUDY"):
        val = default_value
        if us.score == 4:
            val += 5

        # if card_type["architecture_study"] in ncards:
        #     val -= 10
        # if not deck_status["architecture_study"]:
        #     val -= 5

        if val > 0:
            plays.append(("ARCHITECTURE_STUDY", val))

    if moves.is_possible("DAILY_ROUTINE"):
        val = default_value

        if us.score == 4:
            val += 5

        # if card_type["daily_routine"] in ncards:
        #     val -= 10
        # if not cards.deck_status["daily_routine"]:
        #     val -= 5

        if not sum(deck_status.values()):
            val -= 15

        if val > 0:
            plays.append(("DAILY_ROUTINE", val))

    if moves.is_possible("TRAINING"):
        val = default_value
        # if card_type["training"] in ncards:
        #     val = 0
        # if not cards.deck_status["training"]:
        #     val -= 5

        if moves.get_play_card_number(exclude=["TRAINING"]) < 1:
            val -= 20

        if moves.get_play_card_number(exclude=["TRAINING", "CODING"]) > 1:
            val += 10

        if val > 0:
            plays.append(("TRAINING", val))

    if moves.is_possible("TASK_PRIORITIZATION"):
        val = default_value
        cmd = "TASK_PRIORITIZATION"
        fst = None

        # if card_type["task_prioritization"] in ncards:
        #     val = 0
        # if not cards.deck_status["task_prioritization"]:
        #     val -= 5

        for ncard in ncards:
            for rcard in rcards.values():
                if moves.is_possible("TASK_PRIORITIZATION", (ncard, rcard)):
                    if not fst:
                        fst = f"TASK_PRIORITIZATION {ncard} {rcard}"
                    if rcard not in ncards:
                        cmd = f"TASK_PRIORITIZATION {ncard} {rcard}"
                        val += 10
                        break

            if cmd != "TASK_PRIORITIZATION":
                break

        if cmd == "TASK_PRIORITIZATION":
            cmd = fst

        if cmd is not None and val > 0:
            plays.append((cmd, val))

    if moves.is_possible("CONTINUOUS_INTEGRATION"):
        val = default_value
        cmd = None

        # if card_type["continuous_delivery"] in ncards:
        #     val = 0
        # if not cards.deck_status["continuous_delivery"]:
        #     val -= 5

        for ncard in ncards:
            if moves.is_possible("CONTINUOUS_INTEGRATION", ncard):
                val += 10
                cmd = f"CONTINUOUS_INTEGRATION {ncard}"
                break

        if cmd and val > 0:
            plays.append((cmd, val))

    if moves.is_possible("CODE_REVIEW"):
        val = default_value

        # if card_type["code_review"] in ncards and not cards.deck_status["code_review"]:
        #     val -= 5

        if cards.deck_status["bonus"] < 2:
            val = 0

        if val > 0:
            plays.append(("CODE_REVIEW", val))

    if moves.is_possible("CODING"):
        val = default_value

        # if card_type["coding"] in ncards:
        #     val = 0

        # if not cards.deck_status["coding"]:
        #     val -= 5

        if moves.get_play_card_number(exclude=["CODING", "TRAINING"]) < 2:
            val = 0

        if moves.get_play_card_number(exclude=["CODING", "TRAINING"]) > 1:
            val += 15

        if val > 0:
            plays.append(("CODING", val))

    if moves.is_possible("REFACTORING"):
        val = default_value
        hand = cards.get_hand()

        # if card_type["refactoring"] in ncards:
        #     val = 0

        # if not cards.deck_status["refactoring"]:
        #     val -= 5

        if opponent.score > 3 and us.score > 3:
            val += 5

        if not hand["technical_debt"]:
            val = 0

        if val > 0:
            plays.append(("REFACTORING", val))

    plays.sort(key=lambda x: x[1], reverse=True)
    return plays


# game loop
while True:
    applications = Applications()
    cards = Cards()
    moves = Moves()
    game_phase = input()
    applications_count = int(input())

    # Get applications info
    for i in range(applications_count):
        inputs = input().split()
        args = [int(inputs[i]) for i in range(1, 10)]
        applications.add(args[0], args[1], args[2], args[3],
                         args[4], args[5], args[6], args[7], args[8])

    # Get players info
    plocation, pscore, ppermanent_daily_routine_cards, ppermanent_architecture_study_cards = [
        int(j) for j in input().split()]
    us = Player(0, plocation, pscore, ppermanent_daily_routine_cards,
                ppermanent_architecture_study_cards)

    plocation, pscore, ppermanent_daily_routine_cards, ppermanent_architecture_study_cards = [
        int(j) for j in input().split()]
    opponent = Player(1, plocation, pscore, ppermanent_daily_routine_cards,
                      ppermanent_architecture_study_cards)

    # Get cards locations
    card_locations_count = int(input())
    for i in range(card_locations_count):
        inputs = input().split()
        args = [int(inputs[i]) for i in range(1, 11)]
        cards.add_location(inputs[0], args[0], args[1], args[2], args[3],
                           args[4], args[5], args[6], args[7], args[8], args[9])

    # Get possible moves
    possible_moves_count = int(input())
    for i in range(possible_moves_count):
        move = input().split()
        moves.add_possible_move(move[0], [int(mv) for mv in move[1:]])

    # rank applications
    hand = cards.get_hand()
    ranked_applications = applications.rank_applications(us, cards)
    ncards = cards.get_needed_card_list(ranked_applications, us.score)
    rcards = cards.get_riddable_card_set(ranked_applications, us.score)

    output = False

    if game_phase == "RELEASE":
        for aid in range(len(ranked_applications)):
            if moves.is_possible("RELEASE", ranked_applications[aid]["id"]):
                print("RELEASE", ranked_applications[aid]["id"])
                output = True
                break
        if not output:
            print("WAIT")

    elif game_phase == "MOVE" and moves.is_possible("MOVE"):
        missing_releases = 5 - us.score
        loc = us.location

        # use daily routine perks
        if us.permanent_daily_routine_cards:
            for id in range(8):
                move_to = (loc + id) % 7
                for card in ncards:
                    if opponent.location == move_to:
                        continue
                    if moves.is_possible("MOVE", (move_to, card)) and cards.deck_status[card_val_to_type[card]]:
                        print("MOVE", move_to, card)
                        output = True
                        break
                if output:
                    break
        if output:
            continue

        # for id in ncards:
        for id in range(8):
            move_to = (loc + id) % 7
            if opponent.location == move_to:
                continue
            if moves.is_possible("MOVE", move_to):
                print("MOVE", move_to)
                output = True
                break

        # get random
        if not output:
            mv = moves.get_any_move("MOVE")
            if type(mv) == tuple:
                print("MOVE", mv[0], mv[1])
            else:
                print("MOVE", mv)

    elif game_phase == "GIVE_CARD" and moves.is_possible("GIVE"):
        for rcard in rcards.keys():
            if hand[rcard]:
                if rcard == "bonus" and opponent.score == 4:
                    continue
                if rcard == "bonus" and opponent.score < 4:
                    print("GIVE 8")
                else:
                    print("GIVE", card_type[rcard])
                output = True
                break

        if not output:
            print("GIVE", moves.get_any_move("GIVE"))

    elif game_phase == "PLAY_CARD":
        plays = chose_play_card(moves, ncards, rcards,
                                cards.deck_status, opponent, us, cards)
        # print(plays, file=sys.stderr, flush=True)
        # print(moves.moves, file=sys.stderr, flush=True)
        if not len(plays):
            # print(moves.moves, file=sys.stderr, flush=True)
            print("WAIT")
        else:
            print(plays[0][0])

    elif game_phase == "THROW_CARD" and moves.is_possible("THROW"):
        for card in rcards.values():
            if moves.is_possible("THROW", card):
                print("THROW", card)
                output = True
                break
        
        if not output:
            print("THROW", moves.get_any_move("THROW"))

    else:
        print("WAIT")

# print(moves["TASK_PRIORITIZATION"], file=sys.stderr, flush=True)
