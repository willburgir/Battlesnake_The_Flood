
# TODO: 
# For solo games, if map is completely full of food, 
# just follow tail until about to die of hunger. 

# TODO:
# If enclosed by enemy snake, waste time with zigzags


def is_dead_end(board, board_w, board_h, x, y, depth, timer, visited: dict, food_on_path: int) -> bool:
    """
    Determines if going a certain direction (source cell) leads to a dead end
    Returns True if so, False otherwise

    initial call values:
    depth = 1
    timer = my_len
    visited = {}
    food_on_path = 0

    visited later looks like this:
    visited = {
        (1, 2): 1,
        (1, 1): 2,
        etc. where
        (x, y): longest path,
    }
    """
    
    # BASE CASES

    # Out of bounds
    if x < 0 or x >= board_w or y < 0 or y >= board_h:
        return True
    # Stationary obstacle
    elif board[x][y]["is_stationary_obstacle"]:
        return True
    # Blocked by moving obstacle AND sipc >= depth
    elif board[x][y]["is_moving_obstacle"] and board[x][y]["sipc"] + food_on_path >= depth: 
        return True
    # Not longest path
    elif (x, y) in visited and visited[(x, y)] < depth:  
        return True
    # There is enough room! (Not a dead end)
    elif depth >= timer:
        return False

    # RECURSIVE CALLS

    # food -> timer += 1
    if board[x][y]["is_food"]:
        timer += 1
        food_on_path += 1
    visited[(x,y)] = depth

    left  = is_dead_end(board, board_w, board_h, x-1, y  , depth+1, timer, visited, food_on_path)
    if not left:
        return False
    right = is_dead_end(board, board_w, board_h, x+1, y  , depth+1, timer, visited, food_on_path)
    if not right:
        return False
    down  = is_dead_end(board, board_w, board_h, x  , y-1, depth+1, timer, visited, food_on_path)
    if not down:
        return False
    up    = is_dead_end(board, board_w, board_h, x  , y+1, depth+1, timer, visited, food_on_path)
    if not up:
        return False
    # Otherwise
    return left and right and down and up
