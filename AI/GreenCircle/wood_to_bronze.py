import sys
import math

# Complete the hackathon before your opponent by following the principles of Green IT

# game loop
while True:
    card_type = ["training", "coding", "daily_routine", "task_prioritization",
                 "architecture_study", "continuous_delivery", "code_review", "refactoring"]
    type_to_id = {
        "training": 0,
        "coding": 1,
        "daily_routine": 2,
        "task_prioritization": 3,
        "architecture_study": 4,
        "continuous_delivery": 5,
        "code_review": 6,
        "refactoring": 7
    }

    deck_status = {}
    for type in card_type:
        deck_status[type] = 0

    game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    applications_count = int(input())

    applications = []
    players = []
    card_locations = {
        "HAND": [],
        "DRAW": [],
        "DISCARD": [],
        "OPPONENT_CARDS": []
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
        # the location of the card list. It can be HAND, DRAW, DISCARD or OPPONENT_CARDS (AUTOMATED and OPPONENT_AUTOMATED will appear in later leagues)
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

        for ctype in card_type:
            deck_status[ctype] += cards[ctype]

        card_locations[cards_location] = cards

    # rank releases & update card needed as relative to hand
    hand = card_locations["HAND"]
    ranked_applications = applications.copy()
    for app in ranked_applications:
        cost = 0
        for ctype in card_type:
            app[ctype] = 0 if app[ctype] < hand[ctype] else app[ctype] - hand[ctype]
            cost += app[ctype]
        app["cost"] = cost

    ranked_applications.sort(key=lambda x: x["cost"])

    possible_moves_count = int(input())
    non_argument_moves = ["RANDOM", "WAIT", "TRAINING",
                          "ARCHITECTURE_STUDY", "CODE_REVIEW", "REFACTORING", "CODING",
                          "DAILY_ROUTINE"]
    moves = {
        "MOVE": [],
        "RELEASE": [],
        "GIVE": [],
        "THROW": [],
        "TASK_PRIORITIZATION": [],
        "CONTINUOUS_INTEGRATION": [],
    }

    for i in range(possible_moves_count):
        possible_move = input()

        if possible_move in non_argument_moves:
            continue

        move, id = possible_move.split()
        moves[move].append(int(id))
    

    for ctype in card_type:
        deck_status[ctype] = 5 - deck_status[ctype]


    output = False
    if game_phase == "RELEASE" and len(moves["RELEASE"]):
        print("RELEASE", ranked_applications[0]["id"])
        output = True
    
    elif game_phase == "MOVE" and len(moves["MOVE"]):
        for app in ranked_applications:
            card_counts = []
            for ctype in card_type:
                value = [rel_app[ctype] for rel_app in applications if rel_app["id"] == app["id"]][0]
                card_counts.append((ctype, value))
            card_counts.sort(key=lambda x: x[0])

            for card in card_counts:
                if deck_status[card[0]] == 0 and sum(deck_status.values()) != 0:
                    continue
                id = type_to_id[card[0]]
                if (players[1]["location"] != id or (hand[ctype] - card[1] > 0)) and id in moves["MOVE"]:
                    print("MOVE", id)
                    output = True
                    break
            if output:
                break
    
    elif game_phase == "GIVE_CARD" and len(moves["GIVE"]):
        for ids in range(len(ranked_applications)):
            app_id = ranked_applications[ids]["id"]
            app = [a for a in applications if a["id"] == app_id][0]
            for ctype in card_type:
                if hand[ctype] - app[ctype] > 0:
                    print("GIVE", type_to_id[ctype])
                    output = True
                    break
                
            if output:
                break
        if not output:
            print("GIVE", moves["GIVE"][0])
    
    # elif game_phase == "PLAY_CARD" and "REFACTORING" in moves:
    #     # if hand["technical_debt"] > 5:
    #     print("REFACTORING")

    else:
        print("RANDOM")

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT; In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING;
    # print("RANDOM")
