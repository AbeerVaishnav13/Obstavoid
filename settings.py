TITLE = "Obstavoid"
WIDTH = 400
HEIGHT = 500
FPS = 60
FONT_NAME = 'comicsansms'

#Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 120, 0)
LIGHTBLUE = (0, 130, 240)
BROWN = (150, 40, 40)
GROUND_COLOR = BROWN
BGCOLOR = LIGHTBLUE

#PLAYER settings
PLAYER_ACC_X = 5
PLAYER_FRICTION = -0.00001
PLAYER_GRAVITY = -1
PLAYER_VEL_Y = -5
PLAYER_IMAGE = ""
PLAYER_SIZE = (30, 57)

#Startig obstacles
OBSTACLE_IMAGES = ["images/brick_obs.png", "images/wood_obs.png"]

CONSTANT_OBSTACLE_DISTANCE = -100

OBSTACLE_LIST = [(0, 0, WIDTH/8, 40, OBSTACLE_IMAGES[0]),
				 (WIDTH/4, 0, WIDTH/8, 40, OBSTACLE_IMAGES[0]),
				 (WIDTH/2, 0, WIDTH/8, 40, OBSTACLE_IMAGES[0]),
				 (WIDTH * 3/4, 0, WIDTH/8, 40, OBSTACLE_IMAGES[0]),
				 (WIDTH/2, -HEIGHT/6, WIDTH/10, 40, OBSTACLE_IMAGES[0]),
				 (WIDTH/4, -HEIGHT/4, WIDTH/4, 40, OBSTACLE_IMAGES[1]),
				 (WIDTH * 3/4, -HEIGHT/2, WIDTH/4, 40, OBSTACLE_IMAGES[0])]


