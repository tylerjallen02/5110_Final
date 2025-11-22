import pygame
import sys
from data import DataBase
from game_gui import draw_rect, get_scaled_mouse_pos, countdown
from cost import get_human_cost


def run_game():
    """
    Runs all rounds of the game
    """
    # Round durations come from the paper
    run_round(1, 40)
    run_round(2, 20)
    run_round(3, 20)
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

    n_frames = duration * 60
    database = DataBase(n_frames)
    
    FPS = 60
    countdown(canvas, clock, round_num)
    # force the correct number of collection points, even if it runs slower
    for frame in range(n_frames):
        clock.tick(FPS)

        human_cost = get_human_cost(get_scaled_mouse_pos(canvas), 0)
        # TODO dummy data, replace with real when available 
        database.append(frame, 0, 0, 0);
                
        canvas.fill(BACKGROUND_COLOR)
        draw_rect(canvas, human_cost)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    pygame.quit()
    database.write(round_num)

if __name__ == "__main__":
    run_game()
