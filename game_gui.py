import sys
import pygame
import math
def draw_rect(canvas, human_cost):
    """
    Draws a black rectangle centered on the screen, representing the human cost

    Args:
      canvas: pygame canvas to draw the rectangle to
      human_cost: the unscaled human cost, used to caluclate the rectangle height
    """
    rect_width = canvas.get_rect().width * 0.1
    rect_height = _get_human_display_value(human_cost, canvas.get_rect().height)
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

def countdown(screen, clock, round_num, duration=3):
    """
    Displays a `duration` second countdown on the screen. Also displays round number.

    Args:
      screen: game canvas
      clock: clock used by main game
      round_num: the round number to be displayed
      duration: how many seconds the countdown should be
    """
    font = pygame.font.Font(None, 100)
    for tick in range(duration, 0, -1):
        
        screen.fill((0, 0, 0)) 
        
        count_text = font.render(str(tick), True, (255, 255, 255))
        text_rect = count_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(count_text, text_rect)

        round_text = font.render(f"Round {round_num}", True, (255, 255, 255))
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        
        round_text_rect = round_text.get_rect(center=(center_x, center_y - 100))
        screen.blit(round_text, round_text_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        # update once per second
        clock.tick(1)
        
def _get_human_display_value(human_cost, screen_height):
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
