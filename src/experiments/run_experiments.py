"""
Main experiment runner for rollback multiverse.
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from environments import OneHPDuel, GridworldChase
from predictive_agent import PredictiveAgent
from rollback_engine import RollbackReconciler
from metrics import MetricsCollector
from .exp_configs import EXPERIMENT_CONFIGS


def run_experiment(config_name, config):
    """
    Run a single experiment configuration.
    
    Args:
        config_name: Name of the configuration
        config: Configuration dictionary
        
    Returns:
        Dictionary with experiment results
    """
    print(f"Running experiment: {config_name}")
    print(f"Description: {config['description']}")
    
    # Initialize environment
    if config["environment"] == "OneHPDuel":
        env = OneHPDuel(seed=42)
    elif config["environment"] == "GridworldChase":
        env = GridworldChase(seed=42)
    else:
        raise ValueError(f"Unknown environment: {config['environment']}")
    
    # Initialize agents
    agent0 = PredictiveAgent(env.ACTIONS, seed=0)
    agent1 = PredictiveAgent(env.ACTIONS, seed=1)
    
    # Initialize rollback engine and metrics
    rollback_engine = RollbackReconciler()
    metrics = MetricsCollector()
    
    # Reset environment
    obs = env.reset()
    
    # Run simulation
    for frame in range(config["n_frames"]):
        # Get actions from agents
        a0 = agent0.policy(obs)
        a1 = agent1.policy(obs)
        
        # Simulate frame with rollback engine
        obs, r0, r1, info = rollback_engine.simulate_frame(
            env, a0, a1, 
            latency_ms=config["latency_ms"],
            jitter_ms=config["jitter_ms"]
        )
        
        # Update agents with feedback (simplified)
        if "canonical_actions" in info:
            canonical_a0, canonical_a1 = info["canonical_actions"]
            agent0.update_with_feedback(canonical_a1)
            agent1.update_with_feedback(canonical_a0)
        
        # Record metrics
        frame_data = {
            "frame": frame,
            "rollback": info.get("rollback", False),
            "entropy_agent0": agent0.brancher.entropy(),
            "entropy_agent1": agent1.brancher.entropy(),
            "latency_ms": config["latency_ms"][0],
            "reward_agent0": r0,
            "reward_agent1": r1
        }
        metrics.record_frame(frame_data)
        
        # Reset if episode done
        if obs.get("done", False):
            obs = env.reset()
    
    # Get results
    rollback_stats = rollback_engine.get_stats()
    summary_stats = metrics.get_summary_stats()
    
    results = {
        "config_name": config_name,
        "config": config,
        "rollback_stats": rollback_stats,
        "summary_stats": summary_stats,
        "entropy_evolution_agent0": metrics.get_entropy_evolution().tolist(),
        "entropy_evolution_agent1": metrics.get_entropy_evolution().tolist()
    }
    
    print(f"Completed. Rollback rate: {rollback_stats['rollback_rate']:.3f}")
    return results


def run_all_experiments():
    """Run all configured experiments."""
    results = {}
    
    for config_name, config in EXPERIMENT_CONFIGS.items():
        try:
            result = run_experiment(config_name, config)
            results[config_name] = result
        except Exception as e:
            print(f"Error in experiment {config_name}: {e}")
            results[config_name] = {"error": str(e)}
    
    return results


if __name__ == "__main__":
    print("Starting Rollback Multiverse Experiments")
    print("=" * 50)
    
    results = run_all_experiments()
    
    print("\nExperiment Summary:")
    print("=" * 50)
    for config_name, result in results.items():
        if "error" not in result:
            rollback_rate = result["rollback_stats"]["rollback_rate"]
            print(f"{config_name}: Rollback rate = {rollback_rate:.3f}")
        else:
            print(f"{config_name}: ERROR - {result['error']}")
    
    print("\nExperiments completed!")
