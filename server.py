import os
import random
import cherrypy

import map_matrix as map_module
from floodfill import floodfill_positive
import visuals
import aggressive

MY_NAME = "The Flood"



"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⡿⢿⠿⠿⠿⠿⠿⠿⠿⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀
⢲⣶⣶⣶⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀
⠀⢻⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣤
⠀⠀⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣶⣦⣤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

"""


"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "william_c-137_dev",  # TODO: Your Battlesnake Username
            "color": "#6ea11d",  # TODO: Personalize
            "head": "lantern-fish",  # TODO: Personalize
            "tail": "cosmic-horror",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        
        #########################################################################################
        #                                                                                       #
        #                                 DEFINING CONSTANTS                                    #
        #                                                                                       #
        #########################################################################################
        data = cherrypy.request.json
        # My snake's head coordinates
        HEAD_X = data["you"]["head"]["x"]
        HEAD_Y = data["you"]["head"]["y"]

        # The board's border coordinates
        BOARD_HEIGHT = data["board"]["height"]
        BOARD_WIDTH = data["board"]["width"]

        # Getting the map_matrix
        map_matrix = map_module.get_map_matrix()

        # Get my snake
        my_snake = data["you"]

        # Getting enemy snakes list 
        enemy_snakes_list = [s for s in data["board"]["snakes"] if s["name"] != MY_NAME]

        #########################################################################################
        #                                                                                       #
        #                             AM I AGGRESSIVE OR HUNGRY ?                               #
        #                                                                                       #
        #########################################################################################
        
        AGGRESSIVE_LOVE = 35
        FOOD_LOVE = 35
        BECOME_HUNGRY = 25

        aggressive_mode = False
        
        for enemy in enemy_snakes_list:
            if aggressive.can_target_snake(my_snake, enemy) and data["you"]["health"] > BECOME_HUNGRY:
                aggressive_mode = True
                # call flood fill around enemy's head
                floodfill_positive(map_matrix, enemy["head"]["x"]-1, enemy["head"]["y"]  , AGGRESSIVE_LOVE, enemy["head"]["x"]-1, enemy["head"]["y"]  , 0, []) # left
                floodfill_positive(map_matrix, enemy["head"]["x"]+1, enemy["head"]["y"]  , AGGRESSIVE_LOVE, enemy["head"]["x"]+1, enemy["head"]["y"]  , 0, []) # right
                floodfill_positive(map_matrix, enemy["head"]["x"]  , enemy["head"]["y"]-1, AGGRESSIVE_LOVE, enemy["head"]["x"]  , enemy["head"]["y"]-1, 0, []) # down
                floodfill_positive(map_matrix, enemy["head"]["x"]  , enemy["head"]["y"]+1, AGGRESSIVE_LOVE, enemy["head"]["x"]  , enemy["head"]["y"]+1, 0, []) # up
        

        #########################################################################################
        #                                                                                       #
        #                             POSITIVE FLOODFILL: FOOD                                  #
        #                            (if not in aggressive mode)                                #
        #########################################################################################
        if not aggressive_mode:
            for food in data["board"]["food"]:
                # ignore DANGEROUS start center food 
                if not ( data["turn"] <= 10 and (food["x"], food["y"]) == (BOARD_WIDTH//2, BOARD_HEIGHT//2) ):
                    floodfill_positive(map_matrix, food["x"], food["y"], FOOD_LOVE, food["x"], food["y"], 0, [])

        
        left  = map_module.get_score(map_matrix, HEAD_X - 1, HEAD_Y)
        right = map_module.get_score(map_matrix, HEAD_X + 1, HEAD_Y)
        down  = map_module.get_score(map_matrix, HEAD_X, HEAD_Y - 1)
        up    = map_module.get_score(map_matrix, HEAD_X, HEAD_Y + 1)

        # TODO: if 2 positions have same highest score, target the one with most room
        


        #########################################################################################
        #                                                                                       #
        #               DECISION MAKING BASED ON SCORE OF NEIGHBOR POSITIONS                    #
        #                                                                                       #
        #########################################################################################

        moving_list = []

        # If score is highest in the LEFT position
        if left >= right and left >= down and left >= up:
            moving_list.append("left")

        # If score is highest in the UP position
        if up >= right and up >= down and up >= left:
            moving_list.append("up")

        # If score is highest in the DOWN position
        if down >= right and down >= left and down >= up:
            moving_list.append("down")

        # If score is highest in the RIGHT position
        if right >= left and right >= down and right >= up:
            moving_list.append("right")

        move = random.choice(moving_list)
        #print("moving_list:", moving_list, "\nleft", left, "\nright", right, "\ndown", down, "\nup", up)
        print()
        print(f'TURN: {data["turn"]}')
        print(f"MOVE: {move}")
        print(f"AGGRESSIVE MODE: {aggressive_mode}")
        
        visuals.print_map_matrix(map_matrix, "score")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
