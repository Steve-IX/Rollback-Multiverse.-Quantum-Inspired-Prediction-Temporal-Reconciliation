"""
Quantum-inspired amplitude branching implementation.
"""

import numpy as np


class AmplitudeBrancher:
    """
    Quantum-inspired amplitude branching system for hypothesis management.
    """
    
    def __init__(self, n_hypotheses):
        """
        Initialize with n_hypotheses and equal amplitudes 1/sqrt(n).
        
        Args:
            n_hypotheses: Number of hypotheses to track
        """
        self.n_hypotheses = n_hypotheses
        self.amplitudes = np.ones(n_hypotheses) / np.sqrt(n_hypotheses)
    
    def renormalize(self):
        """Renormalize amplitudes to maintain unit norm."""
        norm = np.sqrt(np.sum(self.amplitudes**2))
        if norm > 0:
            self.amplitudes = self.amplitudes / norm
    
    def sample_hypothesis(self):
        """
        Sample hypothesis index and return current probability vector.
        
        Returns:
            (index, probs) where probs is amps**2 normalized
        """
        probs = self.amplitudes**2
        probs = probs / np.sum(probs)  # Ensure normalization
        
        # Sample index based on probabilities
        index = np.random.choice(self.n_hypotheses, p=probs)
        
        return index, probs
    
    def apply_unitary_like_mix(self, mix=0.1):
        """
        Diffuse amplitudes slightly toward the mean, then renormalize.
        
        Args:
            mix: Mixing parameter (0-1), higher values = more mixing
        """
        mean_amplitude = np.mean(self.amplitudes)
        
        # Mix each amplitude toward the mean
        self.amplitudes = (1 - mix) * self.amplitudes + mix * mean_amplitude
        
        # Renormalize
        self.renormalize()
    
    def collapse_with_observation(self, likelihoods):
        """
        Update amplitudes based on observation likelihoods.
        
        Args:
            likelihoods: Array of likelihood values for each hypothesis
        """
        # Update amplitudes: amps *= sqrt(likelihood)
        self.amplitudes = self.amplitudes * np.sqrt(likelihoods)
        
        # Renormalize
        self.renormalize()
    
    def entropy(self):
        """
        Return Shannon entropy of amps**2.
        
        Returns:
            Shannon entropy value
        """
        probs = self.amplitudes**2
        probs = probs / np.sum(probs)  # Ensure normalization
        
        # Calculate Shannon entropy: -sum(p * log2(p))
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
