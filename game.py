import pygame

def run_game():
    """
    Starts the main game loop, game will not exit until, the program finishes, the window is closed
    or 'esc' is pressed
    """
    pygame.init()
    BACKGROUND_COLOR = (200, 200, 200)
    canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("rectangle game")
    exit = False

    while not exit:
        for event in pygame.event.get():
            canvas.fill(BACKGROUND_COLOR)
        
            if event.type == pygame.QUIT:
                exit = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    exit = True
                    pygame.display.update()

    pygame.quit()
