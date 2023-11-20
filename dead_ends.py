import map_matrix as map_module


def is_dead_end(board, board_w, board_h, x, y, visited, depth) -> bool:
    """
    Determines if going a certain direction (source cell) leads to a dead end
    Returns True if so, False otherwise

    Important: 
    depth should start at 1 in the original call
    """
    
    # BASE CASES

    # pos is out of bounds
    if x < 0 or x >= board_w or y < 0 or y >= board_h: # Out of bounds 
        return True
    # pos is in bounds
    if (x,y) in visited:                               # Already visited
        return True
    
    pos = board[x][y]
    distance = pos["distance"]
    if depth > distance:                               # depth > distance
         return True
    
    is_stat_obst = pos["is_stationary_obstacle"]
    is_mov_obst  = pos["is_moving_obstacle"]
    if is_stat_obst:                                   # Stationary obstacle
        return True                                    
    elif is_mov_obst:                                  # Moving obstacle                        
        return pos["sipc"] >= distance
    


    # RECURSIVE CALLS
    visited.append( (x,y) )

    left  = is_dead_end(board, board_w, board_h, x-1, y  , visited, depth+1)
    if not left:
        return False
    right = is_dead_end(board, board_w, board_h, x+1, y  , visited, depth+1)
    if not right:
        return False
    down  = is_dead_end(board, board_w, board_h, x  , y-1, visited, depth+1)
    if not down:
        return False
    up    = is_dead_end(board, board_w, board_h, x  , y+1, visited, depth+1)
    if not up:
        return False
    # Otherwise
    return left and right and down and up








    
    