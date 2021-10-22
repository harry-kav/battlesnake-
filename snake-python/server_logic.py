import random
import math
from typing import List, Dict
"""
This file can be a nice home for your move logic, and to write helper functions.
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict],
                  possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[
        1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

#find the bounds of the arena
def get_walls(board_height, board_width):
    walls = []

    y = -1
    while y <= board_height:
        walls.append({'x': -1, 'y': y})
        walls.append({'x': board_width, 'y': y})
        y += 1
    x = -1
    while x <= board_width:
        walls.append({'x': x, 'y': -1})
        walls.append({'x': x, 'y': board_height})
        x += 1
    return walls


#avoid impact with certain co-ordinates
def avoid_impact(my_head, positions, possible_moves):

    for pos in positions:
        for move in possible_moves:
            if move == 'up':
                if my_head['x'] == pos['x'] and my_head['y'] + 1 == pos['y']:
                    possible_moves.remove('up')
            elif move == 'down':
                if my_head['x'] == pos['x'] and my_head['y'] - 1 == pos['y']:
                    possible_moves.remove('down')
            elif move == 'right':
                if my_head['x'] + 1 == pos['x'] and my_head['y'] == pos['y']:
                    possible_moves.remove('right')
            else:
                if my_head['x'] - 1 == pos['x'] and my_head['y'] == pos['y']:
                    possible_moves.remove('left')

    return possible_moves

#get all the moves that a snake's head can move to
def get_head_moves(head):
    moves = []
    #right
    moves.append({'x': head['x'] + 1, 'y': head['y']})
    #left
    moves.append({'x': head['x'] - 1, 'y': head['y']})
    #up
    moves.append({'x': head['x'], 'y': head['y'] + 1})
    #down
    moves.append({'x': head['x'], 'y': head['y'] - 1})

    return moves

#get all the moves a snake's tail can make
def get_tail_moves(tail):
    moves = []
    #right
    moves.append({'x': tail['x'] + 1, 'y': tail['y']})
    #left
    moves.append({'x': tail['x'] - 1, 'y': tail['y']})
    #up
    moves.append({'x': tail['x'], 'y': tail['y'] + 1})
    #down
    moves.append({'x': tail['x'], 'y': tail['y'] - 1})

    return moves

#get the distance between two points
def get_distance(point1, point2):
    distance = math.sqrt((point1['x'] - point2['x'])**2 +
                         (point1['y'] - point2['y'])**2)

    return distance

#locate the closest food- can also be used to find the closest snake head
def get_closest_food(head, foods, hazards):
    closest = {}
    closest_distance = 99999
    for food in foods:
      if food != head:
        distance = get_distance(head, food)
        #add to distance if food in hazard
        if food in hazards:
            if distance > 2:
                distance += 10
        if distance < closest_distance:
            closest_distance = distance
            closest = {'x': food['x'], 'y': food['y']}

    return closest

#find the optimal move towards food, or sometimes another snake's head
def move_to_food(head, food, possible_moves):
    best_dist = 9999
    best_move = 'none'
    for move in possible_moves:
        if move == 'up':
            distance = get_distance({'x': head['x'], 'y': head['y'] + 1}, food)
            if distance < best_dist:
                best_dist = distance
                best_move = 'up'

        elif move == 'down':
            distance = get_distance({'x': head['x'], 'y': head['y'] - 1}, food)
            if distance < best_dist:
                best_dist = distance
                best_move = 'down'

        elif move == 'right':
            distance = get_distance({'x': head['x'] + 1, 'y': head['y']}, food)
            if distance < best_dist:
                best_dist = distance
                best_move = 'right'

        elif move == 'left':
            distance = get_distance({'x': head['x'] - 1, 'y': head['y']}, food)
            if distance < best_dist:
                best_dist = distance
                best_move = 'left'

    return best_move

#a recursive floodfill algorithm
#used to find how many free spaces there are if a snake makes a given move, and can be applied at various search depths
def flood_recursive(start_pos, obstacles, width, height, depth, hazards):
    free_spaces = 0
    checked = []
    start_depth = depth

    def fill(pos, obstacles, depth, hazards, start_depth):
        nonlocal free_spaces
        nonlocal checked
        print(pos)
        #stop searching if there are over 70 free spaces as this is clearly enough
        if free_spaces > 70:
            return
        #if at max search depth then stop
        if depth == 0:
            #last_move = []
            print("max depth reached")
            return
        #if the square is occupied or has been checked, return
        if pos in obstacles:
            #print("obstacle hit")
            return
        elif pos in checked:
            #print("already checked")
            return
        else:
            checked.append(pos)

            #try to avoid hazards that are not instant killers by awarding less than 1 free space to these locations
            if pos in hazards:
                if depth == start_depth:
                    free_spaces = free_spaces -0.5
                elif depth == start_depth - 1:
                    free_spaces = free_spaces +0.2
                else:
                    free_spaces = free_spaces + 0.25
            elif pos['x'] == 0 or pos['x'] == 10 or pos['y'] == 0 or pos[
                    'y'] == 10:
                if depth == start_depth:
                    free_spaces = free_spaces + 0.5
                else:
                    free_spaces = free_spaces + 0.75
            elif pos['x'] >= 4 and pos ['x'] <= 6 and pos['y'] >= 4 and pos['y'] <=6 and depth == start_depth or depth == start_depth - 1:
              free_spaces = free_spaces +1.8
            elif depth== start_depth and pos['x'] == 0 or pos['x'] == 10 or pos['y'] == 0 or pos['y'] == 10:
              free_spaces = free_spaces - 0.5
            else:
                free_spaces = free_spaces + 1
            #print(free_spaces)

            #all next possible moves
            neighbours = [{
                'x': pos['x'] + 1,
                'y': pos['y']
            }, {
                'x': pos['x'] - 1,
                'y': pos['y']
            }, {
                'x': pos['x'],
                'y': pos['y'] + 1
            }, {
                'x': pos['x'],
                'y': pos['y'] - 1
            }]

            #floodfill each neighbour
            for n in neighbours:
                #if neighbour is not out of bounds
                if 0 <= n['x'] < width and 0 <= n[
                        'y'] < height and n not in checked:
                    fill(n, obstacles, depth - 1, hazards, start_depth)

    fill(start_pos, obstacles, depth, hazards, start_depth)
    #print(free_spaces)
    return free_spaces

#choose which move to make
def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"][
        "head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"][
        "body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    print(
        f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~"
    )
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    #the move options
    original_moves = ["up", "down", "left", "right"]
    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    print('After neck check: ' + str(possible_moves))

    #edges of board
    board_height = data['board']['height']
    board_width = data['board']['width']

    walls = get_walls(board_height, board_width)

    #avoid walls
    possible_moves = avoid_impact(my_head, walls, possible_moves)

    print('After wall check' + str(possible_moves))

    #if only one move avoids a wall then play it
    if len(possible_moves) == 1:
        return possible_moves[0]

    #avoid own head
    new_possible_moves = avoid_impact(my_head, my_body[:-1], possible_moves)

    if new_possible_moves != []:
        possible_moves = new_possible_moves

    print("After own body check: " + str(possible_moves))

    #if there is only one possible move just play it
    if len(possible_moves) == 1:
        return possible_moves[0]

    print(possible_moves)
    old_possible_moves = []
    for direction in possible_moves:
        old_possible_moves.append(direction)

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake
    snakes = data['board']['snakes']
    snakes_locations = []
    enemy_pos_heads = []
    enemy_pos_tails = []
    for snake in snakes:
        if snake['head'] != my_head:

            head_moves = get_head_moves(snake['head'])

            for food in data['board']['food']:
                food_found = False
                if food in head_moves:
                    food_found = True
                if food_found != True:
                    #non-food tails will not be obstacles
                    enemy_pos_tails.append(snake['body'][-1])

            if food_found == True:
                new_possible_moves = avoid_impact(my_head, snake["body"],
                                                  possible_moves)
            else:
                new_possible_moves = avoid_impact(my_head, snake["body"][:-1],
                                                  possible_moves)

            if len(new_possible_moves) != 0:
                possible_moves = new_possible_moves
            else:
                return random.choice(old_possible_moves)

            print("After enemy snake:" + str(possible_moves))

            old_possible_moves = []
            for direction in possible_moves:
                old_possible_moves.append(direction)

            snakes_locations.extend(snake['body'])

            #remove head moves if small
            if data['you']['length'] <= snake['length'] + 1:

                #print("head moves: "+ str(head_moves))
                new_possible_moves = avoid_impact(my_head, head_moves,
                                                  possible_moves)

                snakes_locations.extend(head_moves)
                enemy_pos_heads.extend(head_moves)

                print(len(new_possible_moves))
                if len(new_possible_moves) != 0:
                    possible_moves = new_possible_moves
                else:
                    return random.choice(old_possible_moves)

            #tail_moves = get_tail_moves(snake['body'][-1])
            #new_possible_moves = avoid_impact(my_head,tail_moves, possible_moves)

            #if new_possible_moves != []:
            #  possible_moves = new_possible_moves

    print(possible_moves)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board

    #go for food at the start of the game and when low on health
    hazards = data['board']['hazards']
    food_move = 'none'
    if data['turn'] <= 20 or data['you']['health'] < 60 or data['you'][
            'length'] < 9:
        closest_food = get_closest_food(my_head, data['board']['food'],
                                        hazards)

        food_move = move_to_food(my_head, closest_food, possible_moves)
    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    print(possible_moves)

    #desperation food move
    if food_move != 'none' and data['you']['health'] < 20:
        move = food_move
    else:
        #perform a dfs floodfill in each possible direction to find which move gets the most free space/if the food is safe to get
        obstacles = []
        is_biggest = False
        for enemy in snakes:
          if enemy['head']!= my_head:
            #attack other snakes if bigger by at least 2
            if enemy['length'] < data['you']['length'] + 1:
              is_biggest = True
            else:
              is_biggest = False
            
        if enemy_pos_heads != [] and is_biggest != True:

            for pos in enemy_pos_heads:
                neighbours = [{
                    'x': pos['x'] + 1,
                    'y': pos['y']
                }, {
                    'x': pos['x'] - 1,
                    'y': pos['y']
                }, {
                    'x': pos['x'],
                    'y': pos['y'] + 1
                }, {
                    'x': pos['x'],
                    'y': pos['y'] - 1
                }]

                obstacles.extend(neighbours)


        if data['turn'] < 20 or data['you']['length'] < 9:
            depth = 9
            food_space_val = data['you']['length'] + 5
            attack_space_val = 100
        else:
            depth = 13
            if data['you']['length'] < 15:
                food_space_val = 15
                attack_space_val = 10
            else:
                food_space_val = data['you']['length'] + 2
                attack_space_val = food_space_val -7
        obstacles.extend(walls)
        obstacles.extend(my_body)
        obstacles.extend(snakes_locations)

        #if there is no food near the head then the tail is not an obstacle
        my_head_moves = get_head_moves(my_head)
        food_found = False
        for food in data['board']['food']:
            if food in my_head_moves:
                food_found = True
        if food_found == False:
            obstacles.remove(my_body[-1])

        #remove tails that will not be there in  the future
        for tail in enemy_pos_tails:
            if tail in obstacles:
                obstacles.remove(tail)

        move = my_head
        right_spaces = -100
        left_spaces = -100
        up_spaces = -100
        down_spaces = -100
        for direction in possible_moves:
            if direction == "right":
                try_move = {'x': my_head['x'] + 1, 'y': my_head['y']}
                print("checking right")
                right_spaces = flood_recursive(try_move, obstacles,
                                               board_width, board_height,
                                               depth, hazards)
            elif direction == "left":
                try_move = {'x': my_head['x'] - 1, 'y': my_head['y']}
                print("checking left")
                left_spaces = flood_recursive(try_move, obstacles, board_width,
                                              board_height, depth, hazards)
            elif direction == "up":
                print("checking up")
                try_move = {'x': my_head['x'], 'y': my_head['y'] + 1}
                up_spaces = flood_recursive(try_move, obstacles, board_width,
                                            board_height, depth, hazards)
            elif direction == "down":
                print("checking down")
                try_move = {'x': my_head['x'], 'y': my_head['y'] - 1}
                down_spaces = flood_recursive(try_move, obstacles, board_width,
                                              board_height, depth, hazards)

        print("Right spaces: " + str(right_spaces))
        print("Left spaces: " + str(left_spaces))
        print("Up spaces: " + str(up_spaces))
        print("Down spaces: " + str(down_spaces))

        #try and attack if health is greater than 40 and you are the biggest snake
        if is_biggest == True and data['you']['health'] > 40:
          bravery = 2
          dist_for_interest = 8
          closest_prey = get_closest_food(my_head, snakes_locations, hazards)
          attack_move = move_to_food(my_head, closest_prey, possible_moves)
          if attack_move == 'right':
            attack_dir = {'x': my_head['x']+1, 'y': my_head['y']}
          elif attack_move == 'left':
            attack_dir = {'x': my_head['x']-1, 'y': my_head['y']}
          elif attack_move == 'up':
            attack_dir = {'x': my_head['x'], 'y': my_head['y']+1}
          else:
            attack_dir = {'x': my_head['x'], 'y': my_head['y']-1}

          if my_head['x'] == 0 or my_head['x'] == board_width - 1 or my_head['y'] == 0 or my_head['y'] == board_height - 1 or attack_dir['x'] == 0 or attack_dir['x'] == board_width -1 or attack_dir['y'] == 0 or attack_dir['y'] == board_height -1:

            if get_distance(my_head, closest_prey) < bravery:
              food_space_val = attack_space_val +8
              food_move = attack_move
          else:
            if get_distance(my_head, closest_prey) < dist_for_interest:
              food_space_val = attack_space_val +8
              food_move = attack_move

        #if there is space surrounding food then go for it

        if right_spaces >= food_space_val and food_move == 'right' and {'x': my_head['x']+ 1, 'y': my_head['y']} not in hazards:
            move = 'right'
            print('floodfill right food priority')
            return move
        elif left_spaces >= food_space_val and food_move == 'left' and {'x': my_head['x']- 1, 'y': my_head['y']} not in hazards:
            move = 'left'
            print('floodfill left food priority')
            return move
        elif up_spaces >= food_space_val and food_move == 'up' and {'x': my_head['x'], 'y': my_head['y']+1} not in hazards:
            move = 'up'
            print('floodfill up food priority')
            return move
        if down_spaces >= food_space_val and food_move == 'down' and {'x': my_head['x'], 'y': my_head['y']-1} not in hazards:
            move = 'down'
            print('floodfill down food priority')
            return move

        best_move = max(right_spaces, left_spaces, up_spaces, down_spaces)
        if best_move == right_spaces and 'right' in possible_moves:
            move = 'right'
            print("floodfilled right")
        elif best_move == left_spaces and 'left' in possible_moves:
            move = 'left'
            print("floodfilled left")
        elif best_move == up_spaces and 'up' in possible_moves:
            move = 'up'
            print("floodfilled up")
        elif best_move == down_spaces and 'down' in possible_moves:
            move = 'down'
            print("floodfilled down")
        else:
            if len(possible_moves) > 0:
                move = random.choice(possible_moves)
                print("random possible")
            else:
                move = random.choice(original_moves)
                print("random desperation")
    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}"
    )

    return move
