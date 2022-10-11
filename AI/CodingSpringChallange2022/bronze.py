import sys
import math
from tkinter import E

from numpy import mat, randint

monster_type = 0
ally_hero_type = 1
enemy_hero_type = 2

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# base_x: The corner of the map representing your base
base_x, base_y = [int(i) for i in input().split()]
base_is_topleft = (base_x, base_y) == (0, 0)
enemy_base_x = 17630 - base_x
enemy_base_y = 9000 - base_y

heroes_per_player = int(input())  # Always 3
default_positions = [(12843, 6062), (4706, 2033), (2033, 4706)] if base_is_topleft else [
    (4787, 6967), (12924, 2033), (15597, 4706)]

# game loop
while True:
    base_health, base_mana = [int(i) for i in input().split()]
    enemy_health, enemy_mana = [int(i) for i in input().split()]
    entity_count = int(input())  # Amount of heros and monsters you can see

    spiders = []
    enemy_heroes = []
    my_heroes = []

    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [
            int(j) for j in input().split()]

        entity = {
            'id': _id,
            'type': _type,
            'x': x,
            'y': y,
            'shield_life': shield_life,
            'is_controlled': is_controlled,
            'health': health,
            'vx': vx,
            'vy': vy,
            'near_base': near_base,
            'threat_for': threat_for
        }
        if _type == monster_type:
            spiders.append(entity)
        elif _type == ally_hero_type:
            my_heroes.append(entity)
        elif _type == enemy_hero_type:
            enemy_heroes.append(entity)
    
    # Attack
    spider_near_enemy = False
    for spider in spiders:
        if spider['shield_life'] > 0:
            continue
        distance = math.hypot(spider['x'] - my_heroes[0]['x'], spider['y'] - my_heroes[0]['y'])
        if distance <= 1280:
            spider_near_enemy = True

    if base_mana >= 10 and spider_near_enemy:
        print("SPELL WIND", enemy_base_x, enemy_base_y)
    else:
        target_move_x = default_positions[0][0]
        target_move_y = default_positions[0][1]
        for spider in spiders:
            spider_x = spider['x']
            spider_y = spider['y']
            distance = math.hypot(spider_x - enemy_base_x,
                                  spider_y - enemy_base_y)
            if distance <= 6000:
                target_move_x = spider_x
                target_move_y = spider_y
        print("MOVE", target_move_x, target_move_y)

    # Defence
    if spiders:
        spiders_ranked = []
        for spider in spiders:
            threat_level = 0
            if spider['near_base'] and spider['threat_for']:
                threat_level = 1000
            elif spider['threat_for']:
                threat_level = 500

            distance = math.hypot(base_x - spider['x'], base_y - spider['y'])
            threat_level += 500 * (1 / (distance + 1))

            if distance <= 6500:
                spiders_ranked.append((threat_level, spider))
        spiders_ranked.sort(reverse=True)

        targets = [None, None]
        if spiders_ranked:
            threat_x = spiders_ranked[0][1]['x']
            threat_y = spiders_ranked[0][1]['y']
            distance_1 = math.hypot(
                my_heroes[1]['x'] - threat_x, my_heroes[1]['y'] - threat_y)
            distance_2 = math.hypot(
                my_heroes[2]['x'] - threat_x, my_heroes[2]['y'] - threat_y)

            if distance_1 < distance_2:
                targets[0] = (threat_x, threat_y)
            else:
                targets[1] = (threat_x, threat_y)

        if len(spiders_ranked) > 1:
            threat_x = spiders_ranked[1][1]['x']
            threat_y = spiders_ranked[1][1]['y']
            targets[targets.index(None)] = (threat_x, threat_y)

        for i in range(2):
            if targets[i] is not None:
                print("MOVE", targets[i][0], targets[i][1])
            else:
                print("MOVE", default_positions[i+1]
                      [0], default_positions[i+1][1])
    else:
        for x, y in default_positions[1:]:
            print("MOVE", x, y)
