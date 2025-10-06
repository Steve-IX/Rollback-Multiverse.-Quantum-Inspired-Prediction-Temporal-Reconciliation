"""
Rollback reconciliation engine for latency simulation.
"""

import numpy as np


class RollbackReconciler:
    """
    Rollback reconciliation system for handling network latency and rollbacks.
    """
    
    def __init__(self):
        """Initialize rollback reconciler."""
        self.total_frames = 0
        self.rollback_events = 0
        self.corrections = 0
        self.max_depth = 0
    
    def simulate_frame(self, env, a0_local, a1_local, latency_ms=(30, 30), jitter_ms=(5, 5)):
        """
        Simulate a single frame with network latency and potential rollbacks.
        
        Args:
            env: Environment instance
            a0_local, a1_local: Local actions from each player
            latency_ms: Base latency for each player (ms)
            jitter_ms: Jitter range for each player (ms)
            
        Returns:
            (obs, r0, r1, info) with "rollback": bool
        """
        self.total_frames += 1
        
        # Sample integer arrival times
        arr0 = latency_ms[0] + np.random.randint(-jitter_ms[0], jitter_ms[0] + 1)
        arr1 = latency_ms[1] + np.random.randint(-jitter_ms[1], jitter_ms[1] + 1)
        
        # Determine canonical order (smaller arrival first, tie breaks to player 0)
        canonical_first = 0 if arr0 <= arr1 else 1
        
        # Local beliefs: each device assumes it is first
        device0_belief = 0  # Device 0 assumes it's first
        device1_belief = 1  # Device 1 assumes it's first
        
        # Check for rollback conflicts
        rollback_occurred = False
        if device0_belief != canonical_first or device1_belief != canonical_first:
            rollback_occurred = True
            self.rollback_events += 1
            self.corrections += 1
            self.max_depth = max(self.max_depth, 1)
        
        # Call environment step with canonical order
        obs, r0, r1, info = env.step_resolve(a0_local, a1_local, arr0, arr1)
        
        # Add rollback information
        info["rollback"] = rollback_occurred
        info["arrival_times"] = (arr0, arr1)
        info["canonical_first"] = canonical_first
        
        return obs, r0, r1, info
    
    def get_stats(self):
        """Get current rollback statistics."""
        return {
            "total_frames": self.total_frames,
            "rollback_events": self.rollback_events,
            "corrections": self.corrections,
            "max_depth": self.max_depth,
            "rollback_rate": self.rollback_events / max(1, self.total_frames)
        }
    
    def reset_stats(self):
        """Reset all statistics."""
        self.total_frames = 0
        self.rollback_events = 0
        self.corrections = 0
        self.max_depth = 0
