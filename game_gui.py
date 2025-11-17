import pygame
import math
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
    Draws a black rectangle centered on the screen, representing the human cost

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

def get_scaled_mouse_pos(canvas: pygame.Surface):
    """
    Gets mouse x position and scales it to be between -1.0 and 1.0

    Args:
      canvas: canvas the mouse is moving on
    Returns:
      returns a floating point number between [-1, 1] representing the mouse x position
        
    """
    mouse_x, _ = pygame.mouse.get_pos()
    return (mouse_x / canvas.get_rect().centerx) - 1.0
