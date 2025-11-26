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
    run_round(1, 40, ai_1, "Exp1_Continuous")

    # --- Experiment 2: Conjectural Variations (Policy Space) ---
    print("Starting Experiment 2...")
    ai_2 = AI_Exp2()
    # This runs 10 PAIRS (20 trials total)
    for i in range(10): 
        # Trial 1: Nominal
        run_round(2, 20, ai_2, f"Exp2_Pair{i}_Nominal")
        ai_2.finish_trial()
        
        # Trial 2: Perturbed
        run_round(2, 20, ai_2, f"Exp2_Pair{i}_Perturbed")
        ai_2.finish_trial() # Learning happens now

    # --- Experiment 3: Policy Gradient (Policy Space) ---
    print("Starting Experiment 3...")
    ai_3 = AI_Exp3(gamma=2.0)
    # This runs 10 PAIRS (20 trials total)
    for i in range(10):
        # Trial 1: Nominal
        run_round(3, 20, ai_3, f"Exp3_Pair{i}_Nominal")
        ai_3.finish_trial()
        
        # Trial 2: Perturbed
        run_round(3, 20, ai_3, f"Exp3_Pair{i}_Perturbed")
        ai_3.finish_trial() # Learning happens now
    
def run_round(round_num, duration, ai_agent, log_label=""):
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
