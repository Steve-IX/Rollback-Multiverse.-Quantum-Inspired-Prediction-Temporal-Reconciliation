"""
Basic quantum branching experiment.

This experiment demonstrates the fundamental quantum-inspired branching behavior,
showing how multiple futures can exist simultaneously until a measurement causes collapse.
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_branching import QuantumBranchingSystem
from visualization import MultiverseVisualizer


def run_basic_branching_experiment():
    """Run the basic quantum branching experiment."""
    print("Starting Basic Quantum Branching Experiment...")
    
    # Initialize quantum system with a simple 2D state vector
    initial_state = np.array([1.0, 0.0])  # |0⟩ state
    quantum_system = QuantumBranchingSystem(initial_state)
    
    # Create multiple branches representing different possible futures
    print("Creating quantum branches...")
    
    # Branch 1: Future where value increases
    branch1_state = np.array([0.7, 0.3])  # Superposition state
    branch1_id = quantum_system.branch(branch1_state, 0.4, {"scenario": "bull_market"})
    
    # Branch 2: Future where value decreases
    branch2_state = np.array([0.3, 0.7])  # Different superposition
    branch2_id = quantum_system.branch(branch2_state, 0.3, {"scenario": "bear_market"})
    
    # Branch 3: Future where value stays stable
    branch3_state = np.array([0.5, 0.5])  # Equal superposition
    branch3_id = quantum_system.branch(branch3_state, 0.3, {"scenario": "stable_market"})
    
    # Record initial state
    initial_summary = quantum_system.get_branch_summary()
    print(f"Initial entropy: {initial_summary['entropy']:.3f}")
    print(f"Number of branches: {initial_summary['num_branches']}")
    
    # Evolve branches over time
    print("Evolving branches...")
    
    # Evolution matrix for time evolution
    evolution_matrix = np.array([
        [0.9, 0.1],
        [0.1, 0.9]
    ])
    
    # Evolve each branch
    quantum_system.evolve_branch(branch1_id, evolution_matrix)
    quantum_system.evolve_branch(branch2_id, evolution_matrix)
    quantum_system.evolve_branch(branch3_id, evolution_matrix)
    
    # Record evolved state
    evolved_summary = quantum_system.get_branch_summary()
    print(f"Evolved entropy: {evolved_summary['entropy']:.3f}")
    
    # Perform measurement (collapse wave function)
    print("Performing measurement...")
    collapsed_branch = quantum_system.measure("market_trend", "bull_market", 0.1)
    
    # Record final state
    final_summary = quantum_system.get_branch_summary()
    print(f"Final entropy: {final_summary['entropy']:.3f}")
    print(f"Is collapsed: {final_summary['is_collapsed']}")
    print(f"Collapsed branch ID: {collapsed_branch.id[:8]}")
    
    # Collect experiment data
    experiment_data = {
        "experiment_name": "basic_branching",
        "timestamp": datetime.now().isoformat(),
        "initial_state": initial_state.tolist(),
        "initial_summary": initial_summary,
        "evolved_summary": evolved_summary,
        "final_summary": final_summary,
        "evolution_matrix": evolution_matrix.tolist(),
        "branches_created": [
            {"id": branch1_id, "scenario": "bull_market", "probability": 0.4},
            {"id": branch2_id, "scenario": "bear_market", "probability": 0.3},
            {"id": branch3_id, "scenario": "stable_market", "probability": 0.3}
        ],
        "measurement": {
            "observable": "market_trend",
            "value": "bull_market",
            "uncertainty": 0.1
        }
    }
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save experiment results
    results_file = "results/basic_branching_results.json"
    with open(results_file, 'w') as f:
        json.dump(experiment_data, f, indent=2)
    
    print(f"Experiment results saved to {results_file}")
    
    # Create CSV summary
    csv_data = []
    for branch in final_summary["branches"]:
        csv_data.append({
            "branch_id": branch["id"][:8],
            "probability": branch["probability"],
            "state_norm": branch["state_norm"],
            "timestamp": branch["timestamp"],
            "scenario": branch["metadata"].get("scenario", "unknown")
        })
    
    csv_df = pd.DataFrame(csv_data)
    csv_file = "results/basic_branching_summary.csv"
    csv_df.to_csv(csv_file, index=False)
    print(f"CSV summary saved to {csv_file}")
    
    # Create visualizations
    print("Creating visualizations...")
    visualizer = MultiverseVisualizer()
    
    # Plot branch evolution
    fig1 = visualizer.plot_quantum_branches(quantum_system, "Basic Quantum Branching Results")
    visualizer.save_plot(fig1, "results/basic_branching_plot.png")
    
    # Plot probability evolution
    fig2 = visualizer.plot_branch_probability_evolution(quantum_system, "Branch Probability Distribution")
    visualizer.save_plot(fig2, "results/branch_probabilities.png")
    
    print("Visualizations saved to results/")
    
    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)
    print(f"Initial entropy: {initial_summary['entropy']:.3f}")
    print(f"Final entropy: {final_summary['entropy']:.3f}")
    print(f"Entropy reduction: {initial_summary['entropy'] - final_summary['entropy']:.3f}")
    print(f"Branches created: {len(experiment_data['branches_created'])}")
    print(f"Measurement outcome: {experiment_data['measurement']['value']}")
    print("="*50)
    
    return experiment_data


if __name__ == "__main__":
    run_basic_branching_experiment()
