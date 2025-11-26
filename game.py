import pygame
import sys
from data import DataBase
from game_gui import draw_rect, get_scaled_mouse_pos, countdown
from cost import get_human_cost, get_machine_cost
from experiments import AI_Exp1, AI_Exp2, AI_Exp3

def run_game():
    """
    Runs all rounds of the game with the specific logic for each experiment.
    """
    # --- Experiment 1: Gradient Descent in Action Space ---
    print("Starting Experiment 1...")
    ai_1 = AI_Exp1(alpha=0.3)
    # This runs one long round (40s)
    # run_round(1, 600, ai_1, "Exp1")


    MINI_ROUND_FRAMES = 5 * 60
    MINI_ROUNDS = 10
    # --- Experiment 2: Conjectural Variations (Policy Space) ---
    print("Starting Experiment 2...")
    ai_2 = AI_Exp2(MINI_ROUND_FRAMES)
    # This runs 10 PAIRS (20 trials total)
    # run_round(2, MINI_ROUND_FRAMES * MINI_ROUNDS * 2, ai_2, "Exp2")
        
    # --- Experiment 3: Policy Gradient (Policy Space) ---
    print("Starting Experiment 3...")
    ai_3 = AI_Exp3(MINI_ROUND_FRAMES, gamma=2.0)
    run_round(3, MINI_ROUND_FRAMES * MINI_ROUNDS * 2, ai_3, "Exp3")
    
def run_round(round_num, duration, ai_agent, log_label=""):
    """
    Starts the main game loop, game will not exit until the program finishes, the window is closed
    or 'esc' is pressed

    Args:
      round_num: The round number to display between rounds
      duration: length of the round in frames (approx duration / 60 seconds)
    """
    pygame.init()
    clock = pygame.time.Clock()
    BACKGROUND_COLOR = (200, 200, 200)
    canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Keep the Rectangle Low")
    exit = False

    database = DataBase(duration)
    
    FPS = 60
    countdown(canvas, clock, round_num)
    # force the correct number of collection points, even if it runs slower
    for frame in range(duration):
        clock.tick(FPS)

        # 1. Get Human Input
        h_val = get_scaled_mouse_pos(canvas)
        
        # 2. Get Machine Action from the Agent
        m_val = ai_agent.get_action(h_val)
        
        # 3. Allow AI to store data (needed for Exp 2 & 3 learning)
        if hasattr(ai_agent, "store_frame"):
            ai_agent.store_frame(h_val, m_val)

        # 4. Calculate Costs
        c_h = get_human_cost(h_val, m_val)
        c_m = get_machine_cost(h_val, m_val)
        
        # 5. Save Real Data
        database.append(h_val, m_val, c_h, c_m)
                
        canvas.fill(BACKGROUND_COLOR)
        draw_rect(canvas, c_h)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    pygame.quit()
    database.write(f"{round_num}_{log_label}")

if __name__ == "__main__":
    run_game()
