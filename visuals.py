import cherrypy
import colored
import map_matrix as map_module
import dead_ends2


MY_SNAKE_NAME = "The Flood"
    
#########################################################################################
#                                                                                       #
#                  PRINT map_matrix IN CONSOLE TO EASILY UNDERSTAND                     #
#                                                                                       #
#########################################################################################


# To create padding
def fixed_length_matrix(text, length):
    if len(text) < length:
        text = (" " * (length - len(text)) + text)
    return text


@cherrypy.expose
@cherrypy.tools.json_in()
def print_map_matrix(map_matrix: list, see: str) -> None:
    data = cherrypy.request.json
    pad = 3 # print padding
    
    my_body = data["you"]["body"]
    my_body_list = [(pos["x"], pos["y"]) for pos in my_body]

    head_x = data["you"]["head"]["x"]
    head_y = data["you"]["head"]["y"]
    BOARD_HEIGHT = data["board"]["height"]
    BOARD_WIDTH = data["board"]["width"]

    head_left    = (head_x-1, head_y  )
    head_right   = (head_x+1, head_y  )
    head_down    = (head_x  , head_y-1)
    head_up      = (head_x  , head_y+1)
    next_to_head = [head_left, head_right, head_down, head_up]

    # TODO: use map_module.get_enemy_snakes_lists() when repared instead of duplicated code
    # populate enemy_snakes_list
    enemy_snakes_list = []
    for snake in data["board"]["snakes"]:
        if snake["name"] != MY_SNAKE_NAME: # ignore my snake
            for body_part in snake["body"]:
                is_smaller = False
                is_head = False
                if snake["length"] < data["you"]["length"]:
                    is_smaller = True
                if body_part["x"] == snake["head"]["x"] and body_part["y"] == snake["head"]["y"]:
                    is_head = True
                enemy_snakes_list.append( (body_part["x"], body_part["y"], is_smaller, is_head) )
    # populate food_list
    food_list = []
    for food in data["board"]["food"]:
        food_list.append( (food["x"], food["y"]) )

    # Console colors
    style            = colored.fg("white") # Default
    my_head          = colored.fg("green_yellow") + colored.attr("bold")
    my_body          = colored.fg("green")
    small_enemy_head = colored.fg("blue") + colored.attr("bold")
    small_enemy_body = colored.fg("light_cyan")
    big_enemy_head   = colored.fg("red") + colored.attr("bold")
    big_enemy_body   = colored.fg("red_3a")
    food             = colored.fg("dark_violet_1b")
    dead_end         = colored.fg("light_yellow")

    for x in range(len(map_matrix)):
        for y in range(len(map_matrix[0])):
            # (x, y) transposed because the matrix is transposed visually in console
            # tx and ty stand for transposed x and y
            board_width = len(map_matrix)
            tx = y            
            ty = board_width - x - 1
            my_len = data["you"]["length"]
            style            = colored.fg("white") # Reset
            

            # Print my snake in green    
            if (tx, ty) == (data["you"]["head"]["x"], data["you"]["head"]["y"]): 
                style = my_head
            elif (tx, ty) in my_body_list: 
                style = my_body
            
            # Print dead end in yellow
            elif ( (tx, ty) in next_to_head 
                and dead_ends2.is_dead_end(map_matrix, BOARD_WIDTH, BOARD_HEIGHT, tx, ty, 1, my_len, {}, 0) ):
                style = dead_end

            # print smaller snakes in blue
            elif (tx, ty, True, True) in enemy_snakes_list: 
                style = small_enemy_head
            elif (tx, ty, True, False) in enemy_snakes_list: 
                style = small_enemy_body

            # print bigger/equal snakes in yellow
            elif (tx, ty, False, True) in enemy_snakes_list: 
                style = big_enemy_head
            elif (tx, ty, False, False) in enemy_snakes_list: 
                style = big_enemy_body

            # print food in pink
            elif (tx, ty) in food_list: 
                style = food

            # Print in color
            if see == "score":
                print(colored.stylize(fixed_length_matrix(str(map_module.get_score(map_matrix, tx, ty)), pad), style), end=" ")
            else:
                print(colored.stylize(fixed_length_matrix(str(map_matrix[tx][ty][see]), pad), style), end=" ")
        print()