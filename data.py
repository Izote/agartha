from os.path import dirname, realpath
# from tcod.context import SDL_WINDOW_RESIZABLE


ROOT_PATH = dirname(realpath(__file__))
DATA_PATH = ROOT_PATH + "\\data\\"
TILE_SHEET = DATA_PATH + 'Dorten_SmoothWalls7.png'

WINDOW = {
    "WIDTH": 1280,
    "HEIGHT": 720,
    "FLAGS": None,  # SDL_WINDOW_RESIZABLE
}
