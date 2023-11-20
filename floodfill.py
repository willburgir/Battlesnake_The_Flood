import cherrypy
import map_matrix as map_module


@cherrypy.expose
@cherrypy.tools.json_in()
def floodfill_positive(board: list, x: int, y: int, signal: int, source_x: int, source_y: int, 
                       depth: int, visited: list) -> None:
    """Recursively sends positive signal to attract the snake"""
    data = cherrypy.request.json
    # The board's border coordinates
    BOARD_HEIGHT = data["board"]["height"]
    BOARD_WIDTH = data["board"]["width"]
    
    # Base cases
    distance = abs(x - source_x) + abs(y - source_y)
    if (   x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT     # out of bounds
        or board[x][y]["score"] >= signal                                # stronger signal from other source
        or distance < depth                                            # signal sent closer to source
        or signal <= 0                                                 # no more signal
        or map_module.get_score(board, x, y) <= -99                    # obstacle
        or (x,y) in visited):                                          # already visited):                                               
            return

    board[x][y]["score"] = signal
    visited.append( (x,y) )

    
    # Recursive calls
    floodfill_positive(board, x - 1, y, signal-1, source_x, source_y, depth+1, visited)  # left
    floodfill_positive(board, x + 1, y, signal-1, source_x, source_y, depth+1, visited)  # right
    floodfill_positive(board, x, y - 1, signal-1, source_x, source_y, depth+1, visited)  # down
    floodfill_positive(board, x, y + 1, signal-1, source_x, source_y, depth+1, visited)  # up
    










if __name__ == "__main__":
    cherrypy.quickstart(floodfill_positive)