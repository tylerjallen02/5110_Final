import pygame
from game_gui import draw_rect, get_scaled_mouse_pos, countdown
from cost import get_human_cost

def run_round(round_num, duration):
    """
    Starts the main game loop, game will not exit until the program finishes, the window is closed
    or 'esc' is pressed

    Args:
      round_num: The round number to display between rounds
      duration: length of the round in seconds
    """
    pygame.init()
    clock = pygame.time.Clock()
    BACKGROUND_COLOR = (200, 200, 200)
    canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Keep the Rectangle Low")
    exit = False

    FPS = 60
    countdown(canvas, clock, round_num)
    # force the correct number of collection points, even if it runs slower
    for frame in range(duration * 60):
        clock.tick(FPS)
        
        canvas.fill(BACKGROUND_COLOR)
        human_cost = get_human_cost(get_scaled_mouse_pos(canvas), 0)
        draw_rect(canvas, human_cost)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
        pygame.display.update()

    pygame.quit()
