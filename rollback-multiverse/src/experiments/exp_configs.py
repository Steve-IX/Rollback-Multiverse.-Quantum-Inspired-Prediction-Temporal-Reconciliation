"""
Experiment configurations for rollback multiverse.
"""

# Experiment matrix configurations
EXPERIMENT_CONFIGS = {
    "onehp_baseline": {
        "environment": "OneHPDuel",
        "latency_ms": (30, 30),
        "jitter_ms": (5, 5),
        "n_frames": 1000,
        "description": "Baseline 1 HP duel with low latency"
    },
    
    "onehp_stress": {
        "environment": "OneHPDuel", 
        "latency_ms": (100, 100),
        "jitter_ms": (20, 20),
        "n_frames": 1000,
        "description": "High latency stress test"
    },
    
    "gridworld_spatial": {
        "environment": "GridworldChase",
        "latency_ms": (30, 30),
        "jitter_ms": (5, 5),
        "n_frames": 500,
        "description": "Spatial dynamics with chase"
    }
}

# Latency sweep configurations
LATENCY_SWEEP = {
    "latencies": [10, 30, 50, 100, 200],
    "jitter_ms": (5, 5),
    "n_frames": 500,
    "n_runs": 10
}

# Entropy analysis configurations  
ENTROPY_CONFIGS = {
    "n_hypotheses": [2, 4, 8, 16],
    "mixing_rates": [0.01, 0.05, 0.1, 0.2],
    "n_frames": 1000
}
