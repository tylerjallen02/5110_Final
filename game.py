import pygame
import math

def run_game():
    """
    Starts the main game loop, game will not exit until the program finishes, the window is closed
    or 'esc' is pressed
    """
    pygame.init()
    BACKGROUND_COLOR = (200, 200, 200)
    canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Keep the Rectangle Low")
    exit = False

    while not exit:
        canvas.fill(BACKGROUND_COLOR)
        human_cost = get_human_cost(0, 0)
        draw_rect(canvas, human_cost)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit = True
        pygame.display.update()

    pygame.quit()

def get_human_cost(human_input, machine_input):
    """
    Calculates human cost from 3D quadratic equation

    Args:
        humans_input: input from the human agent in the range [-1, 1]
        machine_input: input from the machine agent in the range [-1, 1]
    Returns:
        returns the cost of the human player. Output is in the range [0, 596 / 375]
    """

    # TODO fully implement. Note that the actual values could be slightly negative. It may
    # dummy function should be replaced with actual equation

    # It may be worth adding 12/125 to the human equation. This small term will remove any potential
    # negative results from teh human equation. 
    return 1

def get_human_display_value(human_cost, screen_height):
    """
    Converts `human_cost` to appropriate display value based on the `screen height`

    Applies square root function (as suggested in the paper) to make small values more visible

    Args:
        human_cost: raw human cost from `get_human_cost()`
        screen_height: height of the screen in pixels
    Returns:
        Returns the scaled cost, meant to be used for the height of the rectangle. 
    """
    
    # These value assume adding 12/125 to the original equation documented in the paper, allowing
    # the minumum to be non-negative. 
    MAX = math.sqrt(596/ 375)
    MIN = 0

    root_cost = math.sqrt(human_cost)
    return screen_height * (root_cost - MIN) / (MAX - MIN) 

def draw_rect(canvas, human_cost):
    """
    Draws a black rectangel centered on the screen, representing the human cost

    Args:
        canvas: pygame canvas to draw the rectangle to
        human_cost: the unscaled human cost, used to caluclate the rectangle height
    """
    rect_width = canvas.get_rect().width * 0.1
    rect_height = get_human_display_value(human_cost, canvas.get_rect().height)
    rect_pos_x = (canvas.get_rect().centerx) - (rect_width / 2)
    rect_pos_y = canvas.get_rect().height - rect_height
    RECT_COLOR = (0, 0, 0)
    pygame.draw.rect(canvas,
                     RECT_COLOR,
                     (rect_pos_x, rect_pos_y, rect_width, rect_height)
                    )
