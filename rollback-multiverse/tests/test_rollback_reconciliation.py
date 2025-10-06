"""
Unit tests for rollback reconciliation system.
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rollback_reconciliation import (
    RollbackReconciliationSystem, 
    ActionType, 
    Action, 
    ReconciliationEvent
)


class TestRollbackReconciliationSystem:
    """Test cases for RollbackReconciliationSystem."""
    
    def test_initialization(self):
        """Test system initialization."""
        system = RollbackReconciliationSystem()
        
        assert len(system.actions) == 0
        assert len(system.reconciliation_events) == 0
        assert len(system.action_dependencies) == 0
        assert len(system.corrected_actions) == 0
        assert len(system.rollback_stack) == 0
    
    def test_add_action(self):
        """Test adding actions."""
        system = RollbackReconciliationSystem()
        
        action_id = system.add_action(
            action_type=ActionType.PREDICTION,
            data={"predicted_value": 10.0},
            timestamp=datetime.now(),
            metadata={"model": "linear_trend"}
        )
        
        assert len(system.actions) == 1
        assert action_id in [action.id for action in system.actions]
        
        action = system.actions[0]
        assert action.action_type == ActionType.PREDICTION
        assert action.data["predicted_value"] == 10.0
        assert action.metadata["model"] == "linear_trend"
    
    def test_add_action_with_dependencies(self):
        """Test adding actions with dependencies."""
        system = RollbackReconciliationSystem()
        
        # Add first action
        action1_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            datetime.now()
        )
        
        # Add second action that depends on first
        action2_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 12.0},
            datetime.now(),
            dependencies={action1_id}
        )
        
        assert len(system.actions) == 2
        assert action1_id in system.action_dependencies[action2_id]
    
    def test_reconcile_with_truth(self):
        """Test reconciling predictions with truth."""
        system = RollbackReconciliationSystem()
        
        # Add a prediction action
        action_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 10.0, "uncertainty": 0.5},
            datetime.now()
        )
        
        # Reconcile with truth
        truth_data = {"actual_value": 12.0}
        reconciliation_event = system.reconcile_with_truth(
            action_id, truth_data, "truth_arrived"
        )
        
        assert len(system.reconciliation_events) == 1
        assert reconciliation_event.original_action_id == action_id
        assert reconciliation_event.corrected_data == truth_data
        assert reconciliation_event.correction_reason == "truth_arrived"
        assert action_id in system.corrected_actions
        
        # Check that action data was updated
        action = system.actions[0]
        assert action.data["actual_value"] == 12.0
        assert action.metadata["corrected"] == True
    
    def test_rollback_to_timestamp(self):
        """Test rolling back to a specific timestamp."""
        system = RollbackReconciliationSystem()
        
        base_time = datetime.now()
        
        # Add actions at different times
        action1_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            base_time
        )
        
        action2_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 12.0},
            base_time + timedelta(minutes=10)
        )
        
        action3_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 15.0},
            base_time + timedelta(minutes=20)
        )
        
        # Rollback to before the last action
        rollback_time = base_time + timedelta(minutes=15)
        rolled_back = system.rollback_to_timestamp(rollback_time)
        
        assert len(rolled_back) == 1  # Only action3 should be rolled back
        assert action3_id in rolled_back
        assert len(system.actions) == 2  # action1 and action2 should remain
        assert action1_id in [action.id for action in system.actions]
        assert action2_id in [action.id for action in system.actions]
        assert action3_id not in [action.id for action in system.actions]
    
    def test_restore_rollback(self):
        """Test restoring rolled back actions."""
        system = RollbackReconciliationSystem()
        
        # Add and rollback an action
        action_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            datetime.now()
        )
        
        rollback_time = datetime.now() - timedelta(minutes=1)
        system.rollback_to_timestamp(rollback_time)
        
        # Restore the action
        success = system.restore_rollback(action_id)
        
        assert success == True
        assert len(system.actions) == 1
        assert system.actions[0].id == action_id
    
    def test_get_causal_chain(self):
        """Test getting causal chain of actions."""
        system = RollbackReconciliationSystem()
        
        # Create a chain of dependencies
        action1_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            datetime.now()
        )
        
        action2_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 12.0},
            datetime.now() + timedelta(minutes=1),
            dependencies={action1_id}
        )
        
        action3_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 14.0},
            datetime.now() + timedelta(minutes=2),
            dependencies={action2_id}
        )
        
        # Get causal chain for action3
        causal_chain = system.get_causal_chain(action3_id)
        
        assert len(causal_chain) == 3
        assert causal_chain[0].id == action1_id  # Should come first
        assert causal_chain[1].id == action2_id  # Then second
        assert causal_chain[2].id == action3_id  # Finally third
    
    def test_get_impacted_actions(self):
        """Test getting actions that depend on a specific action."""
        system = RollbackReconciliationSystem()
        
        # Create actions with dependencies
        action1_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            datetime.now()
        )
        
        action2_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 12.0},
            datetime.now() + timedelta(minutes=1),
            dependencies={action1_id}
        )
        
        action3_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 14.0},
            datetime.now() + timedelta(minutes=2),
            dependencies={action1_id}
        )
        
        # Get actions impacted by action1
        impacted = system.get_impacted_actions(action1_id)
        
        assert len(impacted) == 2
        assert action2_id in [action.id for action in impacted]
        assert action3_id in [action.id for action in impacted]
    
    def test_validate_temporal_consistency(self):
        """Test temporal consistency validation."""
        system = RollbackReconciliationSystem()
        
        base_time = datetime.now()
        
        # Add actions in correct temporal order
        action1_id = system.add_action(
            ActionType.OBSERVATION,
            {"value": 10.0},
            base_time
        )
        
        action2_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 12.0},
            base_time + timedelta(minutes=1),
            dependencies={action1_id}
        )
        
        # Should have no warnings
        warnings = system.validate_temporal_consistency()
        assert len(warnings) == 0
        
        # Add action with incorrect temporal order
        action3_id = system.add_action(
            ActionType.PREDICTION,
            {"predicted_value": 14.0},
            base_time - timedelta(minutes=1),  # Earlier than dependency
            dependencies={action1_id}
        )
        
        # Should have warnings
        warnings = system.validate_temporal_consistency()
        assert len(warnings) > 0
        assert any("earlier timestamp" in warning for warning in warnings)
    
    def test_get_system_state(self):
        """Test getting system state summary."""
        system = RollbackReconciliationSystem()
        
        # Add some actions
        system.add_action(ActionType.OBSERVATION, {"value": 10.0}, datetime.now())
        system.add_action(ActionType.PREDICTION, {"predicted_value": 12.0}, datetime.now())
        
        # Reconcile one action
        action_id = system.actions[0].id
        system.reconcile_with_truth(action_id, {"actual_value": 11.0})
        
        state = system.get_system_state()
        
        assert "total_actions" in state
        assert "corrected_actions" in state
        assert "reconciliation_events" in state
        assert "rollback_stack_size" in state
        assert "temporal_consistency_warnings" in state
        assert "action_types" in state
        assert "recent_actions" in state
        assert "recent_reconciliations" in state
        
        assert state["total_actions"] == 2
        assert state["corrected_actions"] == 1
        assert state["reconciliation_events"] == 1


class TestActionType:
    """Test cases for ActionType enum."""
    
    def test_action_type_values(self):
        """Test ActionType enum values."""
        assert ActionType.PREDICTION.value == "prediction"
        assert ActionType.OBSERVATION.value == "observation"
        assert ActionType.CORRECTION.value == "correction"
        assert ActionType.BRANCH_CREATE.value == "branch_create"
        assert ActionType.BRANCH_COLLAPSE.value == "branch_collapse"


if __name__ == "__main__":
    pytest.main([__file__])
