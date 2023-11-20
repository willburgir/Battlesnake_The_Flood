import cherrypy
import dead_ends2

MY_SNAKE_NAME = "The Flood"


#########################################################################################
#                                                                                       #
#                         GETTING VARIOUS INFO FROM DATA["BOARD"]                       #
#                                                                                       #
#########################################################################################
@cherrypy.expose
@cherrypy.tools.json_in()
# TODO: fix this error -> discord post
def get_enemy_snakes_lists():
    """
    Creates and returns two lists: 
    1. enemy_snakes_list          -> all enemy snakes' body parts
       [(x, y, is_smaller, is_head)]
    2. enemy_snakes_heads_list    -> all enemy snakes' heads
       [(x, y, is_smaller)]

       ERROR: Won't let me use this function in other modules for some reason. I will copy-paste it for now... Strange error: 

       Traceback (most recent call last):
       File "server.py", line 7, in <module>
       import visuals
       File "/home/runner/The-Flood/visuals.py", line 7, in <module>
       enemy_snakes_list, ignore = map_module.get_enemy_snakes_lists()
       File "/home/runner/The-Flood/map_matrix.py", line 24, in get_enemy_snakes_lists
       data = cherrypy.request.json
       File "/opt/virtualenvs/python3/lib/python3.8/site-packages/cherrypy/__init__.py", line 224, in __getattr__
       return getattr(child, name)
       AttributeError: 'Request' object has no attribute 'json'
    """
    data = cherrypy.request.json
    enemy_snakes_list = []
    enemy_snakes_heads_list = []
    for snake in data["board"]["snakes"]:
        if snake["name"] != MY_SNAKE_NAME:  # ignore my snake
            for body_part in snake["body"]:
                is_smaller = False
                is_head = False
                # is_smaller
                if snake["length"] < data["you"]["length"]:
                    is_smaller = True
                # is_head
                if body_part["x"] == snake["head"]["x"] and body_part[
                        "y"] == snake["head"]["y"]:
                    is_head = True
                    enemy_snakes_heads_list.append(
                        (body_part["x"], body_part["y"], is_smaller))
                enemy_snakes_list.append(
                    (body_part["x"], body_part["y"], is_smaller, is_head))
    return enemy_snakes_list, enemy_snakes_heads_list


#########################################################################################
#                                                                                       #
#                                  SETTERS AND GETTERS                                  #
#                                                                                       #
#########################################################################################
"""
This Section is also responsible for:
    Out of bounds = -99
    Big snakes possible next move = -98
"""
MIN_VAL = -99
QUASI_MIN_VAL = -98


@cherrypy.expose
@cherrypy.tools.json_in()
def get_score(board, x, y):
    data = cherrypy.request.json
    BOARD_HEIGHT = data["board"]["height"]
    BOARD_WIDTH  = data["board"]["width"]
    my_len = data["you"]["length"]

      
    # TODO: use get_enemy_snakes_lists() when repared instead of duplicated code
    enemy_snakes_list = []
    enemy_snakes_heads_list = []
    for snake in data["board"]["snakes"]:
        if snake["name"] != MY_SNAKE_NAME:  # ignore my snake
            for body_part in snake["body"]:
                is_smaller = False
                is_head = False
                # is_smaller
                if snake["length"] < data["you"]["length"]:
                    is_smaller = True
                # is_head
                if body_part["x"] == snake["head"]["x"] and body_part[
                        "y"] == snake["head"]["y"]:
                    is_head = True
                    enemy_snakes_heads_list.append(
                        (body_part["x"], body_part["y"], is_smaller))
                enemy_snakes_list.append(
                    (body_part["x"], body_part["y"], is_smaller, is_head))

    # Out of bounds
    if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
        return MIN_VAL
        
    head_x  = data["you"]["head"]["x"]
    head_y  = data["you"]["head"]["y"]
    my_neck = (data["you"]["body"][1]["x"], data["you"]["body"][1]["y"])
    head_left    = (head_x-1, head_y  )
    head_right   = (head_x+1, head_y  )
    head_down    = (head_x  , head_y-1)
    head_up      = (head_x  , head_y+1)
    next_to_head = [head_left, head_right, head_down, head_up]
    # Dead ends
    if (board[x][y]["score"] > -99                                                  # not MIN_VAL
        and (x,y) in next_to_head                                                   # pos is next to head
        and (x,y) != my_neck                                                        # pos is not my neck
        and dead_ends2.is_dead_end(board, BOARD_WIDTH, BOARD_HEIGHT, x, y, 1, my_len, {}, 0) ): # is dead end
        return QUASI_MIN_VAL

    # Bigger or equal snake possible next move AND food = -99
    # because we assume they are going to eat the food
    elif(((x + 1, y, False) in enemy_snakes_heads_list or
          (x - 1, y, False) in enemy_snakes_heads_list or
          (x, y + 1, False) in enemy_snakes_heads_list or 
          (x, y - 1, False) in enemy_snakes_heads_list) 
        and board[x][y]["score"] >= MIN_VAL
        and board[x][y]["is_food"]):
        return MIN_VAL
    
    # Bigger or equal snake possible next move = -97
    elif ((x + 1, y, False) in enemy_snakes_heads_list or
        (x - 1, y, False) in enemy_snakes_heads_list or
        (x, y + 1, False) in enemy_snakes_heads_list or (x, y - 1, False)
            in enemy_snakes_heads_list) and board[x][y]["score"] >= QUASI_MIN_VAL:
        return QUASI_MIN_VAL + 1 #(Not as bad as dead end)


    # Otherwise, normal score
    return board[x][y]["score"]


def get_is_stationary_obstacle(board, x, y):
    if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
        return True
    return board[x][y]["is_stationary_obstacle"]


#########################################################################################
#                                                                                       #
#                               Creating the map_matrix                                 #
#                                                                                       #
#########################################################################################
@cherrypy.expose
@cherrypy.tools.json_in()
def get_map_matrix():
    data = cherrypy.request.json
    # My snake's head coordinates
    HEAD_X = data["you"]["head"]["x"]
    HEAD_Y = data["you"]["head"]["y"]

    # The board's border coordinates
    BOARD_HEIGHT = data["board"]["height"]
    BOARD_WIDTH = data["board"]["width"]

    # Define map_matrix
    # TODO: add prtinting color into this info
    map_matrix = [[{
        "score": 0,
        "food_score": 0,
        "distance": None,
        "longest_path": 0,
        "sipc": 0,
        "is_food": False,
        "is_moving_obstacle": False,
        "is_stationary_obstacle": False
    } for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]

    #########################################################################################
    #                                                                                       #
    #                          Set is_food attribute where needed                           #
    #                                                                                       #
    #########################################################################################

    for f in data["board"]["food"]:
        map_matrix[f["x"]][f["y"]]["is_food"] = True
        
    #########################################################################################
    #                                                                                       #
    #                      BODY PARTS STAY IN PLACE COUNTDOWN (SIPC)                        #
    #                                                                                       #
    #########################################################################################

    # sipc only gets the +1 is the body list of that snake has an overlapping tail

    for snake in data["board"]["snakes"]:
        # needs +1 ?
        # just_ate = 0
        # if len(snake["body"]) > 1 and snake["body"][-1] == snake["body"][-2]:
        #     just_ate = 1
        for body_part in snake["body"]:
            sipc = snake["length"] - snake["body"].index(body_part) - 1
            map_matrix[body_part["x"]][body_part["y"]]["is_moving_obstacle"] = True
            map_matrix[body_part["x"]][body_part["y"]]["sipc"] = sipc #+ just_ate

    #########################################################################################
    #                                                                                       #
    #                   CALCULATING THE DISTANCE IN NUMBER OF TURNS                         #
    #                     (and identifying stationary obstacles)                            #
    #########################################################################################
    hazards_list = [(h["x"], h["y"]) for h in data["board"]["hazards"]]

    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            # write distance
            map_matrix[x][y]["distance"] = abs(x - HEAD_X) + abs(y - HEAD_Y)
            # write is_stationary_obstacle
            if (x, y) in hazards_list:
                map_matrix["x"]["y"]["is_stationary_obstacle"] = True

    #########################################################################################
    #                                                                                       #
    #                            Deadly potions get a -99 score                             #
    #                                                                                       #
    #########################################################################################

    ##### Mark bodies as -99 ##### NEW VERSION CONSIDERS DISTANCE AND SIPC
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            # Moving obstacles with (distance <= SIPC)
            if map_matrix[x][y]["is_moving_obstacle"] and (
                    map_matrix[x][y]["distance"] <= map_matrix[x][y]["sipc"]):
                map_matrix[x][y]["score"] = -99
            # Stationary obstacles
            elif map_matrix[x][y]["is_stationary_obstacle"]:
                map_matrix[x][y]["score"] = -99
    return map_matrix


if __name__ == "__main__":
    cherrypy.quickstart(get_enemy_snakes_lists)
