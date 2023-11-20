

def can_target_snake(my_snake, enemy_snake) -> bool:
    """
    Determines if I should target a certain enemy snake 

    TODO: 
    Will this break my snake in solo games?
    """
    # I am smaller!
    if my_snake["length"] <= enemy_snake["length"]:
        return False

    # buffer = distance between our heads // 2
    #          (not taking obstacles into account)
    buffer = (abs(my_snake["head"]["x"] - enemy_snake["head"]["x"]) 
            + abs(my_snake["head"]["y"] - enemy_snake["head"]["y"]))

    buffer = buffer//2

    if my_snake["length"] > enemy_snake["length"] + buffer - 1:
        return True
    else:
        return False