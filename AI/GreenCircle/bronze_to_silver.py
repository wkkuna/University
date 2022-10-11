import sys

card_type = ["training", "coding", "daily_routine", "task_prioritization",
             "architecture_study", "continuous_delivery", "code_review", "refactoring"]

card_type = {
    "training": 0,
    "coding": 1,
    "daily_routine": 2,
    "task_prioritization": 3,
    "architecture_study": 4,
    "continuous_delivery": 5,
    "code_review": 6,
    "refactoring": 7
}


def get_riddable_card_list(hand, app):
    riddable_cards = []
    for ctype in card_type.keys():
        if hand[ctype] - app[ctype] > 0:
            riddable_cards.append(card_type[ctype])
            break
    return list(set(riddable_cards))


def get_card_counts(app, applications):
    card_counts = []
    for ctype in card_type.keys():
        value = [rel_app[ctype]
                 for rel_app in applications if rel_app["id"] == app["id"]][0]
        card_counts.append((ctype, value))
    card_counts.sort(key=lambda x: x[0])
    return card_counts


def get_needed_card_list(app, hand, deck_status, applications):
    card_counts = get_card_counts(app, applications)
    # print(card_counts, file=sys.stderr, flush=True)
    desirable_cards = []
    # get a list of needed cards to delay the penalty given from passing administrative desk
    for card in card_counts:
        if deck_status[card[0]] == 0 and sum(deck_status.values()) != 0:
            continue
        id = card_type[card[0]]
        if hand[ctype] - card[1] < 0:
            desirable_cards.append(id)

    desirable_cards.sort()
    return list(set(desirable_cards))

def get_any_move(mtype, possible_moves):
    if not len(possible_moves[mtype]):
        return None
    
    return possible_moves[mtype][0]

# game loop
while True:

    deck_status = {}
    for type in card_type.keys():
        deck_status[type] = 0

    game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    applications_count = int(input())

    applications = []
    players = []
    card_locations = {
        "HAND": [],
        "DRAW": [],
        "DISCARD": [],
        "AUTOMATED": [],
        "OPPONENT_CARDS": [],
        "OPPONENT_AUTOMATED": []
    }

    for i in range(applications_count):
        inputs = input().split()
        object_type = inputs[0]
        _id = int(inputs[1])
        # number of TRAINING skills needed to release this application
        training_needed = int(inputs[2])
        # number of CODING skills needed to release this application
        coding_needed = int(inputs[3])
        # number of DAILY_ROUTINE skills needed to release this application
        daily_routine_needed = int(inputs[4])
        # number of TASK_PRIORITIZATION skills needed to release this application
        task_prioritization_needed = int(inputs[5])
        # number of ARCHITECTURE_STUDY skills needed to release this application
        architecture_study_needed = int(inputs[6])
        # number of CONTINUOUS_DELIVERY skills needed to release this application
        continuous_delivery_needed = int(inputs[7])
        # number of CODE_REVIEW skills needed to release this application
        code_review_needed = int(inputs[8])
        # number of REFACTORING skills needed to release this application
        refactoring_needed = int(inputs[9])

        application = {
            "id": _id,
            "training": training_needed,
            "coding": coding_needed,
            "daily_routine": daily_routine_needed,
            "task_prioritization": task_prioritization_needed,
            "architecture_study": architecture_study_needed,
            "continuous_delivery": continuous_delivery_needed,
            "code_review": code_review_needed,
            "refactoring": refactoring_needed,
            "cost": 0
        }

        applications.append(application)

    for i in range(2):
        # player_location: id of the zone in which the player is located
        # player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
        # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
        player_location, player_score, player_permanent_daily_routine_cards, player_permanent_architecture_study_cards = [
            int(j) for j in input().split()]

        player = {
            "id": i,
            "location": player_location,
            "score": player_score,
            "permament_daily_routine_cards": player_permanent_daily_routine_cards,
            "permament_architecture_study_cards": player_permanent_architecture_study_cards
        }

        players.append(player)

    card_locations_count = int(input())

    for i in range(card_locations_count):
        inputs = input().split()
        # the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS, AUTOMATED and OPPONENT_AUTOMATED
        cards_location = inputs[0]
        training_cards_count = int(inputs[1])
        coding_cards_count = int(inputs[2])
        daily_routine_cards_count = int(inputs[3])
        task_prioritization_cards_count = int(inputs[4])
        architecture_study_cards_count = int(inputs[5])
        continuous_delivery_cards_count = int(inputs[6])
        code_review_cards_count = int(inputs[7])
        refactoring_cards_count = int(inputs[8])
        bonus_cards_count = int(inputs[9])
        technical_debt_cards_count = int(inputs[10])

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

        for ctype in card_type.keys():
            deck_status[ctype] += cards[ctype]

        card_locations[cards_location] = cards

    # rank releases & update card needed as relative to hand
    hand = card_locations["HAND"]
    ranked_applications = applications.copy()
    for app in ranked_applications:
        cost = 0
        for ctype in card_type.keys():
            app[ctype] = 0 if app[ctype] < hand[ctype] else app[ctype] - hand[ctype]
            cost += app[ctype]
        app["cost"] = cost

    ranked_applications.sort(key=lambda x: x["cost"])

    possible_moves_count = int(input())
    non_argument_moves = []
    moves = {
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

    for i in range(possible_moves_count):
        possible_move = input()

        move = possible_move.split()
        mtype = move[0]
        args = move[1:]

        if mtype == "TASK_PRIORITIZATION":
            moves[mtype].append((int(args[0]), int(args[1])))
        elif len(args):
            moves[mtype].append(int(args[0]))
        else:
            moves[mtype] = True

    for ctype in card_type.keys():
        deck_status[ctype] = 5 - deck_status[ctype]

    output = False

    if game_phase == "RELEASE" and len(moves["RELEASE"]):
        for aid in range(len(ranked_applications)):
            if ranked_applications[0]["id"] in moves["RELEASE"]:
                print("RELEASE", ranked_applications[0]["id"])
                output = True
                break
        if not output:
            print("RELEASE", get_any_move("RELEASE", moves))

    elif game_phase == "MOVE" and len(moves["MOVE"]):
        for app in ranked_applications:
            ncards = get_needed_card_list(app, hand, deck_status, applications)

            for id in ncards:
                if id > players[0]["location"] and id in moves["MOVE"]:
                    print("MOVE", id)
                    output = True
                    break
            if output:
                break

        if not output:
            for id in moves["MOVE"]:
                if players[1]["location"] == id:
                    continue

                if id > players[0]["location"]:
                    print("MOVE", id)
                    output = True
                    break
        if not output:
            print("MOVE", get_any_move("MOVE", moves))

    elif game_phase == "GIVE_CARD" and len(moves["GIVE"]):
        for ids in range(len(ranked_applications)):
            app_id = ranked_applications[ids]["id"]
            app = [a for a in applications if a["id"] == app_id][0]
            cards_list = get_riddable_card_list(hand, app)

            if len(cards_list):
                print("GIVE", cards_list[0])
                output = True
                break

        if not output:
            print("GIVE", get_any_move("GIVE", moves))

    elif game_phase == "PLAY_CARD":
        if moves["TASK_PRIORITIZATION"]:
            ncards = []
            rcards = []
            for app in ranked_applications:
                ncards.append(get_needed_card_list(
                    app, hand, deck_status, applications))
                rcards.append(get_riddable_card_list(hand, app))

            possible_give = [mv[0] for mv in moves["TASK_PRIORITIZATION"]]
            possible_throw = [mv[1] for mv in moves["TASK_PRIORITIZATION"]]
            for ncard in ncards:
                for rcard in rcards:
                    if ncard in possible_give and rcard in possible_throw:
                        print("TASK_PRIORITIZATION", ncard, rcard)
                        output = True
                        break
                if output:
                    break
        if not output and moves["CONTINUOUS_INTEGRATION"]:
            print("CONTINUOUS_INTEGRATION", get_any_move("CONTINUOUS_INTEGRATION", moves))
        if not output and moves["CODE_REVIEW"]:
            print("CODE_REVIEW")
            output = True
        if not output and moves["ARCHITECTURE_STUDY"]:
            print("ARCHITECTURE_STUDY")
            output = True
        if not output and moves["CODING"]:
            print("CODING")
            output = True
        if not output and moves["TRAINING"]:
            print("TRAINING")
            output = True
        if not output and moves["DAILY_ROUTINE"]:
            print("DAILY_ROUTINE")
            output = True
        if not output and moves["REFACTORING"]:
            print("REFACTORING")
            output = True
        if not output:
            print("RANDOM")

    elif game_phase == "THROW_CARD" and len(moves["THROW"]):
        for app in ranked_applications:
            rcards = get_riddable_card_list(hand, app)
            for card in rcards:
                if card in moves["THROW"]:
                    print("THROW", card)
                    output = True
                    break
            if output:
                break
        if not output:
            print("THROW", get_any_move("THROW", moves))
    else:
        print("RANDOM")

# print(moves["TASK_PRIORITIZATION"], file=sys.stderr, flush=True)
