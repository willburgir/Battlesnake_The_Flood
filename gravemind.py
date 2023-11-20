import cherrypy

"""
I could not get this to work.
I want to create a file where I can define all board-related constants 
Then, I can simply import * into all other files without having to bother with cherrypy

HELP
"""

class BoardInfo:
    HEAD_X = None
    HEAD_Y = None
    BOARD_HEIGHT = None
    BOARD_WIDTH = None
    
    #@staticmethod
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def define_global_constants(self):
        data = cherrypy.request.json
        # My snake's head coordinates
        BoardInfo.HEAD_X = data["you"]["head"]["x"]
        BoardInfo.HEAD_Y = data["you"]["head"]["y"]
        
        # The board's border coordinates
        BoardInfo.BOARD_HEIGHT = data["board"]["height"]
        BoardInfo.BOARD_WIDTH = data["board"]["width"]

cherrypy.tree.mount(BoardInfo(), '/')