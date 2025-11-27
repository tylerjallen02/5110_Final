import statistics

from pygame.display import set_caption
import cost

from cost import hM, mM, BM, AM, DM

# ==========================================
#               AI AGENT CLASSES
# ==========================================

class AI_Exp1:
    """
    Experiment 1: Gradient Descent in Action Space.
    Updates m continuously every frame based on gradient.
    """
    def __init__(self, alpha=0.3):
        self.m = -0.2  # Start near Nash
        self.alpha = alpha
        # DEBUG: Counter to print info every second
        self.frame_count = 0

    def get_action(self, human_h):
        # Calculate gradient d(c_M)/dm
        grad = cost.get_machine_gradient(human_h, self.m)
        
        # Update State: m = m - alpha * grad
        self.m = self.m - (self.alpha * grad)
        
        # Clamp to screen bounds [-1, 1]
        self.m = max(-1.0, min(1.0, self.m))
        
        # --- DEBUG PRINT ---
        self.frame_count += 1
        # Print every 30 frames (0.5 seconds)
        if self.frame_count % 30 == 0:
            print(f"[Exp1] Human: {human_h:.2f} | Machine Reacting: {self.m:.2f}")
            
        return self.m

    def finish_trial(self):
        pass 

class AI_Exp2:
    """
    Experiment 2: Conjectural Variation.
    """
    def __init__(self, mini_round_frames):
        # Initial Policy Slope: Nash Best Response
        self.mini_round_frames = mini_round_frames
        self.L_M = -cost.BM / cost.AM 
        self.delta = 0.05 
        self.is_perturbed = False 
        
        self.history_h = []
        self.history_m = []
        self.prev_avg_h = 0.0
        self.prev_avg_m = 0.0

    def get_action(self, human_h):
        d = self.delta if self.is_perturbed else 0.0
        return self.L_M * (human_h - cost.hM) + cost.mM + d

    def store_frame(self, h, m):
        self.history_h.append(h)
        self.history_m.append(m)
        if len(self.history_h) >= self.mini_round_frames:
            self.finish_trial()

    def finish_trial(self):
        avg_h = statistics.mean(self.history_h) if self.history_h else 0
        avg_m = statistics.mean(self.history_m) if self.history_m else 0
        self.history_h, self.history_m = [], [] 

        if not self.is_perturbed:
            self.prev_avg_h = avg_h
            self.prev_avg_m = avg_m
            self.is_perturbed = True
            print(f"  -> [Exp2] Trial A (Nominal) Done.")
        else:
            self.is_perturbed = False
            
            denom = (avg_m - self.prev_avg_m)
            if abs(denom) < 1e-9: denom = 1e-9
            L_H = (avg_h - self.prev_avg_h) / denom

            denom_pol = (cost.AM + L_H * cost.BM)
            if abs(denom_pol) < 1e-9: denom_pol = 1e-9
            self.L_M = -(cost.BM + L_H * cost.DM) / denom_pol
            
            # DEBUG PRINT
            print(f"  -> [Exp2] LEARNING: Updated Policy Slope to: {self.L_M:.3f}")

class AI_Exp3:
    """
    Experiment 3: Policy Gradient.
    """
    def __init__(self, mini_round_frames, gamma=2.0):
        self.mini_round_frames = mini_round_frames
        self.L_M = -cost.BM / cost.AM 
        self.Delta = 0.05  
        self.gamma = gamma
        self.is_perturbed = False
        
        self.history_h = []
        self.history_m = []
        self.cost_trial_1 = 0.0

    def get_action(self, human_h):
        D = self.Delta if self.is_perturbed else 0.0
        slope = self.L_M + D
        return slope * (human_h - hM) + mMhhi
    
    def store_frame(self, h, m):
        self.history_h.append(h)
        self.history_m.append(m)
        if len(self.history_h) >= self.mini_round_frames:
            self.finish_trial()
            
    def finish_trial(self):
        avg_h = statistics.mean(self.history_h) if self.history_h else 0
        avg_m = statistics.mean(self.history_m) if self.history_m else 0

        self.history_h, self.history_m = [], []

        curr_cost = cost.get_machine_cost(avg_h, avg_m)

        if not self.is_perturbed:
            self.cost_trial_1 = curr_cost
            self.is_perturbed = True
            print(f"  -> [Exp3] Trial A Cost: {curr_cost:.4f}")
        else:
            self.is_perturbed = False
            gradient = (curr_cost - self.cost_trial_1) / self.Delta
            self.L_M = self.L_M - (self.gamma * gradient)
            
            # DEBUG PRINT
            print(f"  -> [Exp3] LEARNING: Updated Policy Slope to: {self.L_M:.3f}")
