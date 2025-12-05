import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import cost  # Imports your cost parameters for theoretical lines

# ==========================================
#        THEORETICAL REFERENCE LINES
# ==========================================
def get_reaction_curves():
    """Generates the theoretical Best Response lines for Human and Machine."""
    m_vals = np.linspace(-1, 1, 100)
    h_vals = np.linspace(-1, 1, 100)
    
    # Human Best Response: d(cH)/dh = 0
    # Formula: h = hH - (BH/AH)*(m - mH)
    h_best_response = cost.hH - (cost.BH / cost.AH) * (m_vals - cost.mH)
    
    # Machine Best Response: d(cM)/dm = 0
    # Formula: m = mM - (BM/AM)*(h - hM)
    m_best_response = cost.mM - (cost.BM / cost.AM) * (h_vals - cost.hM)
    
    return m_vals, h_best_response, h_vals, m_best_response

# ==========================================
#              PLOTTING LOGIC
# ==========================================
def plot_experiment_1():
    print("Visualizing Experiment 1 (Nash Equilibrium)...")
    files = glob.glob("data/round_1_Exp1/*.npz")
    if not files:
        print("  No data found for Round 1.")
        return

    plt.figure(figsize=(10, 8))
    
    # 1. Plot Theoretical Lines
    m_axis, h_br, h_axis, m_br = get_reaction_curves()
    plt.plot(h_br, m_axis, 'g--', label="Human Best Response", alpha=0.6)
    plt.plot(h_axis, m_br, 'r--', label="Machine Best Response", alpha=0.6)
    
    # Calculate Nash (Intersection) roughly for plotting
    # Nash is where the lines cross. 
    plt.scatter([-0.2], [-0.2], color='black', s=100, zorder=10, label="Nash Equilibrium")

    # 2. Plot Real Data Trajectories
    for i, f in enumerate(files):
        data = np.load(f)
        h = data['human_inputs']
        m = data['machine_inputs']
        # Plot trajectory with transparency to see density
        plt.plot(h, m, color='blue', alpha=0.15)
        # Plot final point of each run
        plt.scatter(h[-1], m[-1], color='blue', s=10, alpha=0.5)

    plt.title("Experiment 1: Convergence to Nash Equilibrium")
    plt.xlabel("Human Action (h)")
    plt.ylabel("Machine Action (m)")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("results_exp1.png")
    print("  -> Saved results_exp1.png")

def plot_learning_experiments(round_num, title, filename):
    print(f"Visualizing {title}...")
    # for tyler: Change path as needed (data1 to data)
    files = glob.glob(f"data1/round_{round_num}_Exp{round_num}/*.npz")
    if not files:
        print(f"  No data found for Round {round_num}.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    
    all_costs = []
    all_human_costs = []
    min_len = float('inf')

    # 1. Load all files
    for f in files:
        data = np.load(f)
        # We care about Machine Cost (optimizing its objective)
        c_m = data['machine_scores']
        c_h = data['human_scores']
        all_costs.append(c_m)
        all_human_costs.append(c_h)
        if len(c_m) < min_len:
            min_len = len(c_m)
        if len(c_h) < min_len:
            min_len = len(c_h)

    # 2. Trim to shortest length to average them
    trimmed_costs = [c[:min_len] for c in all_costs]
    trimmed_human = [c[:min_len] for c in all_human_costs]
    avg_cost = np.median(trimmed_costs, axis=0)
    avg_human = np.median(trimmed_human, axis=0)
    
    # 3. Apply Moving Average to smooth the noise
    window = 100
    if min_len > window:
        smooth_avg = np.convolve(avg_cost, np.ones(window)/window, mode='valid')
        smooth_human = np.convolve(avg_human, np.ones(window)/window, mode='valid')
        time_axis = np.arange(len(smooth_avg))
    else:
        smooth_avg = avg_cost
        smooth_human = avg_human
        time_axis = np.arange(len(smooth_avg))

    # 4. Plot individual runs (lightly) and average (bold)
    # for c in trimmed_costs:
    #     # Plot a subset of raw data or just the background noise
    #     ax.plot(c, color='gray', alpha=0.05)

    # Machine cost on primary y-axis
    ax.plot(time_axis, smooth_avg, color='red', linewidth=2, label="Average Machine Cost")
    ax.set_title(f"{title}: Cost Reduction Over Time")
    ax.set_xlabel("Time (Frames)")
    ax.set_ylabel("Machine Cost ($c_M$)", color='red')
    ax.tick_params(axis='y', colors='red')

    # Human cost on secondary y-axis
    ax2 = ax.twinx()
    ax2.plot(time_axis, smooth_human, color='blue', linewidth=2, label="Average Human Cost")
    ax2.set_ylabel("Human Cost ($c_H$)", color='blue')
    ax2.tick_params(axis='y', colors='blue')

    # Combine legends from both axes
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='best')

    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename)
    print(f"  -> Saved {filename}")

if __name__ == "__main__":
    plot_experiment_1()
    plot_learning_experiments(1, "Experiment 1 (Nash Equilibrium)", "results_exp1_learning.png")   
    plot_learning_experiments(2, "Experiment 2 (Conjectural Variations)", "results_exp2.png")
    plot_learning_experiments(3, "Experiment 3 (Policy Gradient)", "results_exp3.png")
    print("Done!")