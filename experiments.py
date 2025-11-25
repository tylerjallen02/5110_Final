import cost

# --- Experiment 1: Gradient Descent in Action Space ---
def run_algorithm_1(steps=50, alpha=0.1, start_m=0.0):
    m = start_m
    history = []
    
    for _ in range(steps):
        # 1. FIX: Call the best response function, not the cost function
        h = cost.get_human_cost(m)
        
        # 2. Record state
        history.append((h, m))
        
        # 3. Machine updates action directly
        # Eq (3): m = m - alpha * d(c_M)/dm
        grad = cost.get_machine_cost(h, m)
        m = m - (alpha * grad)
        
    return history

# --- Experiment 2: Conjectural Variations (Policy Space) ---
def run_algorithm_2(iterations=10):
    # Start with Policy Slope
    L_M = 1.0
    [cite_start]delta = 0.05 # Perturbation size [cite: 531]
    history = []
    
    for _ in range(iterations):
        # Solve for equilibrium (h, m) given the policy constraint m = L_M * h
        
        # Trial 1: Nominal Policy
        denominator = (1 - L_M/3)
        if abs(denominator) < 1e-9: denominator = 1e-9 # Avoid div/0
        
        h1 = (-2/15) / denominator
        m1 = L_M * h1
        
        # Trial 2: Perturbed Policy (m = L_M*h + delta)
        h2 = (delta/3 - 2/15) / denominator
        m2 = L_M * h2 + delta
        
        # Algorithm Step: Estimate Human's Response Slope (L_H_tilde)
        # Eq (5)
        diff_m = m2 - m1
        if abs(diff_m) < 1e-9: diff_m = 1e-9
        L_H_tilde = (h2 - h1) / diff_m
        
        # Algorithm Step: Update Machine Policy L_M
        # Eq (6a)
        if abs(1 - L_H_tilde) > 1e-9:
            L_M = (1 - 2 * L_H_tilde) / (1 - L_H_tilde)
            
        history.append((h1, m1))
        
    return history

# --- Experiment 3: Policy Gradient (Policy Space) ---
def run_algorithm_3(iterations=10, gamma=2.0):
    # Start with Policy Slope L_M = 0
    L_M = 0.0
    [cite_start]Delta = 0.05 # Perturbation to the SLOPE [cite: 531]
    history = []
    
    for _ in range(iterations):
        # Trial 1: Nominal Policy m = L_M * h
        denom1 = (1 - L_M/3)
        if abs(denom1) < 1e-9: denom1 = 1e-9
        h1 = (-2/15) / denom1
        m1 = L_M * h1
        cost1 = cost.get_machine_cost(h1, m1)
        
        # Trial 2: Perturbed Slope m = (L_M + Delta) * h
        L_M_new = L_M + Delta
        denom2 = (1 - L_M_new/3)
        if abs(denom2) < 1e-9: denom2 = 1e-9
        h2 = (-2/15) / denom2
        m2 = L_M_new * h2
        cost2 = cost.get_machine_cost(h2, m2)
        
        # Algorithm Step: Estimate Policy Gradient
        # Eq (9)
        gradient = (cost2 - cost1) / Delta
        
        # Algorithm Step: Update Slope L_M
        # Eq (10)
        L_M = L_M - (gamma * gradient)
        
        history.append((h1, m1))
        
    return history