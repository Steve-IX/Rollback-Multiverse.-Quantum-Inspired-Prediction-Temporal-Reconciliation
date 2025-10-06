"""
Predictive agent with quantum-inspired hypothesis management.
"""

import numpy as np
from quantum_branching import AmplitudeBrancher


class PredictiveAgent:
    """
    Predictive agent that uses quantum-inspired branching for opponent modeling.
    """
    
    def __init__(self, actions, seed=0, n_hypotheses=4):
        """
        Initialize predictive agent.
        
        Args:
            actions: List of possible actions
            seed: Random seed for reproducibility
            n_hypotheses: Number of hypotheses to track
        """
        self.actions = actions
        self.rng = np.random.RandomState(seed)
        self.brancher = AmplitudeBrancher(n_hypotheses)
        self.n_hypotheses = n_hypotheses
    
    def predict_opponent(self):
        """
        Sample hypothesis and map to opponent action.
        
        Returns:
            (action, probs) where action is predicted opponent action and probs is probability distribution
        """
        # Sample hypothesis
        hypothesis_idx, probs = self.brancher.sample_hypothesis()
        
        # Map hypothesis index to action by index mod len(actions)
        action_idx = hypothesis_idx % len(self.actions)
        predicted_action = self.actions[action_idx]
        
        return predicted_action, probs
    
    def update_with_feedback(self, observed_action, noise=0.05):
        """
        Update beliefs based on observed opponent action.
        
        Args:
            observed_action: The action the opponent actually took
            noise: Noise level for non-matching hypotheses
        """
        # Construct likelihoods
        likelihoods = np.full(self.n_hypotheses, noise / (len(self.actions) - 1))
        
        # Find hypotheses that predict the observed action
        for i in range(self.n_hypotheses):
            action_idx = i % len(self.actions)
            predicted_action = self.actions[action_idx]
            
            if predicted_action == observed_action:
                likelihoods[i] = 1.0 - noise
        
        # Update amplitudes with observation
        self.brancher.collapse_with_observation(likelihoods)
        
        # Apply slight mixing to prevent overconfidence
        self.brancher.apply_unitary_like_mix(mix=0.05)
    
    def policy(self, obs):
        """
        Simple policy for action selection.
        
        Args:
            obs: Current observation
            
        Returns:
            Selected action
        """
        # TODO: Implement policy improvement
        # For now, return a simple policy
        if "hp" in obs and obs["hp"] > 0:
            return "attack"  # Simple aggressive policy for OneHPDuel
        else:
            return "idle"
