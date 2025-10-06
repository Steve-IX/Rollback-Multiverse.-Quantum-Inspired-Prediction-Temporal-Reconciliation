"""
Quantum-inspired branching and collapse system.

This module implements a simulation of quantum-like branching where multiple
possible futures exist simultaneously until a measurement (observation) causes
the wave function to collapse to a single reality.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class BranchState:
    """Represents the state of a single branch in the multiverse."""
    id: str
    probability: float
    state_vector: np.ndarray
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class Measurement:
    """Represents a measurement that causes wave function collapse."""
    timestamp: datetime
    observable: str
    value: Any
    uncertainty: float


class QuantumBranchingSystem:
    """
    Quantum-inspired branching system for speculative futures.
    
    This class simulates multiple possible futures simultaneously, allowing
    for speculative execution until definitive information arrives.
    """
    
    def __init__(self, initial_state: np.ndarray, initial_probability: float = 1.0):
        """
        Initialize the quantum branching system.
        
        Args:
            initial_state: Initial state vector
            initial_probability: Initial probability (should be 1.0 for root)
        """
        self.branches: List[BranchState] = []
        self.measurements: List[Measurement] = []
        self.collapsed_branch: Optional[BranchState] = None
        self.is_collapsed = False
        
        # Create initial branch
        initial_branch = BranchState(
            id=str(uuid.uuid4()),
            probability=initial_probability,
            state_vector=initial_state.copy(),
            timestamp=datetime.now(),
            metadata={}
        )
        self.branches.append(initial_branch)
    
    def branch(self, new_state: np.ndarray, probability: float, 
               metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new branch from the current state.
        
        Args:
            new_state: State vector for the new branch
            probability: Probability of this branch (must sum to 1.0 across all branches)
            metadata: Optional metadata for this branch
            
        Returns:
            Branch ID of the newly created branch
        """
        if self.is_collapsed:
            raise RuntimeError("Cannot branch after wave function collapse")
        
        if metadata is None:
            metadata = {}
        
        # Normalize probabilities
        total_prob = sum(branch.probability for branch in self.branches)
        if total_prob + probability > 1.0:
            # Renormalize all branches
            scale_factor = (1.0 - probability) / total_prob
            for branch in self.branches:
                branch.probability *= scale_factor
        
        new_branch = BranchState(
            id=str(uuid.uuid4()),
            probability=probability,
            state_vector=new_state.copy(),
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        self.branches.append(new_branch)
        return new_branch.id
    
    def evolve_branch(self, branch_id: str, evolution_matrix: np.ndarray) -> None:
        """
        Evolve a specific branch using a linear transformation.
        
        Args:
            branch_id: ID of the branch to evolve
            evolution_matrix: Matrix representing the evolution operator
        """
        if self.is_collapsed:
            raise RuntimeError("Cannot evolve branches after wave function collapse")
        
        branch = self._find_branch(branch_id)
        if branch is None:
            raise ValueError(f"Branch {branch_id} not found")
        
        # Apply evolution: |ψ'⟩ = U|ψ⟩
        branch.state_vector = evolution_matrix @ branch.state_vector
        branch.timestamp = datetime.now()
    
    def measure(self, observable: str, value: Any, uncertainty: float = 0.0) -> BranchState:
        """
        Perform a measurement that collapses the wave function.
        
        Args:
            observable: Name of the observable being measured
            value: Measured value
            uncertainty: Measurement uncertainty
            
        Returns:
            The collapsed branch state
        """
        measurement = Measurement(
            timestamp=datetime.now(),
            observable=observable,
            value=value,
            uncertainty=uncertainty
        )
        self.measurements.append(measurement)
        
        # Find the branch that best matches the measurement
        best_branch = self._find_best_matching_branch(observable, value, uncertainty)
        
        # Collapse to this branch
        self.collapsed_branch = best_branch
        self.is_collapsed = True
        
        # Clear other branches (they no longer exist)
        self.branches = [best_branch]
        
        return best_branch
    
    def get_expected_value(self, observable: str) -> float:
        """
        Calculate the expected value of an observable across all branches.
        
        Args:
            observable: Name of the observable
            
        Returns:
            Expected value weighted by branch probabilities
        """
        if self.is_collapsed:
            if self.collapsed_branch is None:
                return 0.0
            return self._extract_observable_value(self.collapsed_branch, observable)
        
        expected_value = 0.0
        for branch in self.branches:
            value = self._extract_observable_value(branch, observable)
            expected_value += branch.probability * value
        
        return expected_value
    
    def get_entropy(self) -> float:
        """
        Calculate the von Neumann entropy of the current state.
        
        Returns:
            Entropy value (0 for collapsed state, >0 for superposition)
        """
        if self.is_collapsed or len(self.branches) <= 1:
            return 0.0
        
        entropy = 0.0
        for branch in self.branches:
            if branch.probability > 0:
                entropy -= branch.probability * np.log2(branch.probability)
        
        return entropy
    
    def _find_branch(self, branch_id: str) -> Optional[BranchState]:
        """Find a branch by its ID."""
        for branch in self.branches:
            if branch.id == branch_id:
                return branch
        return None
    
    def _find_best_matching_branch(self, observable: str, value: Any, 
                                 uncertainty: float) -> BranchState:
        """
        Find the branch that best matches the measurement.
        
        This is a simplified implementation that could be enhanced with
        more sophisticated matching algorithms.
        """
        if not self.branches:
            raise RuntimeError("No branches available for measurement")
        
        # For now, return the highest probability branch
        # In a more sophisticated implementation, this would consider
        # the actual observable values and measurement uncertainty
        return max(self.branches, key=lambda b: b.probability)
    
    def _extract_observable_value(self, branch: BranchState, observable: str) -> float:
        """
        Extract the value of an observable from a branch state.
        
        This is a simplified implementation that assumes the observable
        corresponds to a specific element of the state vector.
        """
        # For demonstration, assume observable maps to first element of state vector
        # In practice, this would be more sophisticated
        if len(branch.state_vector) > 0:
            return float(branch.state_vector[0])
        return 0.0
    
    def get_branch_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all current branches.
        
        Returns:
            Dictionary containing branch information
        """
        return {
            "num_branches": len(self.branches),
            "is_collapsed": self.is_collapsed,
            "entropy": self.get_entropy(),
            "branches": [
                {
                    "id": branch.id,
                    "probability": branch.probability,
                    "state_norm": float(np.linalg.norm(branch.state_vector)),
                    "timestamp": branch.timestamp.isoformat(),
                    "metadata": branch.metadata
                }
                for branch in self.branches
            ],
            "measurements": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "observable": m.observable,
                    "value": m.value,
                    "uncertainty": m.uncertainty
                }
                for m in self.measurements
            ]
        }
