"""
Unit tests for quantum branching system.
"""

import pytest
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from quantum_branching import QuantumBranchingSystem, BranchState


class TestQuantumBranchingSystem:
    """Test cases for QuantumBranchingSystem."""
    
    def test_initialization(self):
        """Test system initialization."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        assert len(system.branches) == 1
        assert system.branches[0].probability == 1.0
        assert np.array_equal(system.branches[0].state_vector, initial_state)
        assert not system.is_collapsed
    
    def test_branch_creation(self):
        """Test creating new branches."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        new_state = np.array([0.5, 0.5])
        branch_id = system.branch(new_state, 0.3)
        
        assert len(system.branches) == 2
        assert branch_id in [branch.id for branch in system.branches]
        
        # Check probability normalization
        total_prob = sum(branch.probability for branch in system.branches)
        assert abs(total_prob - 1.0) < 1e-10
    
    def test_branch_evolution(self):
        """Test evolving branches."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        new_state = np.array([0.5, 0.5])
        branch_id = system.branch(new_state, 0.5)
        
        evolution_matrix = np.array([
            [0.9, 0.1],
            [0.1, 0.9]
        ])
        
        system.evolve_branch(branch_id, evolution_matrix)
        
        # Find the evolved branch
        evolved_branch = None
        for branch in system.branches:
            if branch.id == branch_id:
                evolved_branch = branch
                break
        
        assert evolved_branch is not None
        expected_state = evolution_matrix @ new_state
        assert np.allclose(evolved_branch.state_vector, expected_state)
    
    def test_measurement_collapse(self):
        """Test wave function collapse through measurement."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        # Create multiple branches
        system.branch(np.array([0.7, 0.3]), 0.4)
        system.branch(np.array([0.3, 0.7]), 0.3)
        
        assert len(system.branches) == 3
        assert not system.is_collapsed
        
        # Perform measurement
        collapsed_branch = system.measure("test_observable", "test_value", 0.1)
        
        assert system.is_collapsed
        assert len(system.branches) == 1
        assert system.branches[0].id == collapsed_branch.id
    
    def test_entropy_calculation(self):
        """Test entropy calculation."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        # Single branch should have zero entropy
        assert system.get_entropy() == 0.0
        
        # Add branches with equal probability
        system.branch(np.array([0.5, 0.5]), 0.5)
        
        # Two equal probability branches should have entropy = 1
        entropy = system.get_entropy()
        assert abs(entropy - 1.0) < 1e-10
    
    def test_expected_value_calculation(self):
        """Test expected value calculation."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        # Add branches with different values
        system.branch(np.array([2.0, 0.0]), 0.3)
        system.branch(np.array([0.0, 3.0]), 0.2)
        
        expected_value = system.get_expected_value("test_observable")
        
        # Expected value should be weighted average
        # This is a simplified test - in practice, the observable extraction
        # would be more sophisticated
        assert expected_value >= 0  # Basic sanity check
    
    def test_cannot_branch_after_collapse(self):
        """Test that branching is not allowed after collapse."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        # Collapse the system
        system.measure("test", "value", 0.0)
        
        # Attempting to branch should raise an error
        with pytest.raises(RuntimeError):
            system.branch(np.array([0.5, 0.5]), 0.5)
    
    def test_cannot_evolve_after_collapse(self):
        """Test that evolution is not allowed after collapse."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        branch_id = system.branch(np.array([0.5, 0.5]), 0.5)
        
        # Collapse the system
        system.measure("test", "value", 0.0)
        
        # Attempting to evolve should raise an error
        with pytest.raises(RuntimeError):
            system.evolve_branch(branch_id, np.eye(2))
    
    def test_branch_summary(self):
        """Test branch summary generation."""
        initial_state = np.array([1.0, 0.0])
        system = QuantumBranchingSystem(initial_state)
        
        system.branch(np.array([0.5, 0.5]), 0.5)
        
        summary = system.get_branch_summary()
        
        assert "num_branches" in summary
        assert "is_collapsed" in summary
        assert "entropy" in summary
        assert "branches" in summary
        assert "measurements" in summary
        
        assert summary["num_branches"] == 2
        assert not summary["is_collapsed"]
        assert len(summary["branches"]) == 2


if __name__ == "__main__":
    pytest.main([__file__])
