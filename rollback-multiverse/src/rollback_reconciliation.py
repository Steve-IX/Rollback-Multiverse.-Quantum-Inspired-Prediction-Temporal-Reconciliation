"""
Rollback reconciliation system with timestamp-based correction.

This module implements a system for correcting predictions when truth arrives,
maintaining deterministic ordering based on action arrival timestamps.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from enum import Enum


class ActionType(Enum):
    """Types of actions in the system."""
    PREDICTION = "prediction"
    OBSERVATION = "observation"
    CORRECTION = "correction"
    BRANCH_CREATE = "branch_create"
    BRANCH_COLLAPSE = "branch_collapse"


@dataclass
class Action:
    """Represents an action with timestamp ordering."""
    id: str
    timestamp: datetime
    action_type: ActionType
    data: Dict[str, Any]
    dependencies: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReconciliationEvent:
    """Represents a reconciliation event when truth arrives."""
    id: str
    timestamp: datetime
    original_action_id: str
    corrected_data: Dict[str, Any]
    correction_reason: str
    impact_analysis: Dict[str, Any] = field(default_factory=dict)


class RollbackReconciliationSystem:
    """
    Rollback reconciliation system for correcting predictions when truth arrives.
    
    This system maintains deterministic ordering based on action arrival timestamps
    and provides mechanisms for rolling back and correcting speculative execution.
    """
    
    def __init__(self):
        """Initialize the rollback reconciliation system."""
        self.actions: List[Action] = []
        self.reconciliation_events: List[ReconciliationEvent] = []
        self.action_dependencies: Dict[str, Set[str]] = {}
        self.corrected_actions: Set[str] = set()
        self.rollback_stack: List[Tuple[str, Action]] = []  # (action_id, original_action)
    
    def add_action(self, action_type: ActionType, data: Dict[str, Any],
                   timestamp: Optional[datetime] = None,
                   dependencies: Optional[Set[str]] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a new action to the system.
        
        Args:
            action_type: Type of action
            data: Action data
            timestamp: Action timestamp (defaults to now)
            dependencies: Set of action IDs this action depends on
            metadata: Additional metadata
            
        Returns:
            Action ID
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        if dependencies is None:
            dependencies = set()
        
        if metadata is None:
            metadata = {}
        
        action_id = str(uuid.uuid4())
        action = Action(
            id=action_id,
            timestamp=timestamp,
            action_type=action_type,
            data=data,
            dependencies=dependencies,
            metadata=metadata
        )
        
        self.actions.append(action)
        self.action_dependencies[action_id] = dependencies.copy()
        
        return action_id
    
    def reconcile_with_truth(self, action_id: str, truth_data: Dict[str, Any],
                           correction_reason: str = "truth_arrived") -> ReconciliationEvent:
        """
        Reconcile a prediction with the actual truth.
        
        Args:
            action_id: ID of the action to reconcile
            truth_data: Actual truth data
            correction_reason: Reason for the correction
            
        Returns:
            Reconciliation event
        """
        action = self._find_action(action_id)
        if action is None:
            raise ValueError(f"Action {action_id} not found")
        
        # Create reconciliation event
        reconciliation_id = str(uuid.uuid4())
        reconciliation_event = ReconciliationEvent(
            id=reconciliation_id,
            timestamp=datetime.now(),
            original_action_id=action_id,
            corrected_data=truth_data,
            correction_reason=correction_reason
        )
        
        # Analyze impact of the correction
        impact_analysis = self._analyze_correction_impact(action, truth_data)
        reconciliation_event.impact_analysis = impact_analysis
        
        # Store the reconciliation event
        self.reconciliation_events.append(reconciliation_event)
        
        # Mark the action as corrected
        self.corrected_actions.add(action_id)
        
        # Update the action data with truth
        action.data.update(truth_data)
        action.metadata["corrected"] = True
        action.metadata["correction_timestamp"] = reconciliation_event.timestamp
        action.metadata["correction_reason"] = correction_reason
        
        return reconciliation_event
    
    def rollback_to_timestamp(self, target_timestamp: datetime) -> List[str]:
        """
        Rollback all actions to a specific timestamp.
        
        Args:
            target_timestamp: Timestamp to rollback to
            
        Returns:
            List of action IDs that were rolled back
        """
        rolled_back_actions = []
        
        # Find actions to rollback (those after the target timestamp)
        actions_to_rollback = [
            action for action in self.actions
            if action.timestamp > target_timestamp
        ]
        
        # Store original actions for potential restoration
        for action in actions_to_rollback:
            self.rollback_stack.append((action.id, action))
            rolled_back_actions.append(action.id)
        
        # Remove actions from the main list
        self.actions = [
            action for action in self.actions
            if action.timestamp <= target_timestamp
        ]
        
        # Update corrected actions set
        self.corrected_actions = {
            action_id for action_id in self.corrected_actions
            if action_id in [action.id for action in self.actions]
        }
        
        return rolled_back_actions
    
    def restore_rollback(self, action_id: str) -> bool:
        """
        Restore a previously rolled back action.
        
        Args:
            action_id: ID of the action to restore
            
        Returns:
            True if restoration was successful
        """
        # Find the action in the rollback stack
        for i, (stored_id, original_action) in enumerate(self.rollback_stack):
            if stored_id == action_id:
                # Restore the action
                self.actions.append(original_action)
                self.rollback_stack.pop(i)
                return True
        
        return False
    
    def get_causal_chain(self, action_id: str) -> List[Action]:
        """
        Get the causal chain of actions leading to a specific action.
        
        Args:
            action_id: ID of the action to trace
            
        Returns:
            List of actions in causal order
        """
        action = self._find_action(action_id)
        if action is None:
            return []
        
        causal_chain = []
        visited = set()
        
        def trace_dependencies(current_action: Action):
            if current_action.id in visited:
                return
            
            visited.add(current_action.id)
            
            # Add dependencies first
            for dep_id in current_action.dependencies:
                dep_action = self._find_action(dep_id)
                if dep_action is not None:
                    trace_dependencies(dep_action)
            
            # Add current action
            causal_chain.append(current_action)
        
        trace_dependencies(action)
        return causal_chain
    
    def get_impacted_actions(self, action_id: str) -> List[Action]:
        """
        Get all actions that depend on a specific action.
        
        Args:
            action_id: ID of the action to check
            
        Returns:
            List of actions that depend on the given action
        """
        impacted_actions = []
        
        for action in self.actions:
            if action_id in action.dependencies:
                impacted_actions.append(action)
        
        return impacted_actions
    
    def validate_temporal_consistency(self) -> List[str]:
        """
        Validate that all actions maintain temporal consistency.
        
        Returns:
            List of inconsistency warnings
        """
        warnings = []
        
        # Check that dependencies come before dependent actions
        for action in self.actions:
            for dep_id in action.dependencies:
                dep_action = self._find_action(dep_id)
                if dep_action is None:
                    warnings.append(f"Action {action.id} depends on non-existent action {dep_id}")
                elif dep_action.timestamp > action.timestamp:
                    warnings.append(
                        f"Action {action.id} depends on {dep_id} but has earlier timestamp"
                    )
        
        # Check for circular dependencies
        for action in self.actions:
            if self._has_circular_dependency(action.id, set()):
                warnings.append(f"Circular dependency detected involving action {action.id}")
        
        return warnings
    
    def get_system_state(self) -> Dict[str, Any]:
        """
        Get the current state of the reconciliation system.
        
        Returns:
            Dictionary containing system state information
        """
        return {
            "total_actions": len(self.actions),
            "corrected_actions": len(self.corrected_actions),
            "reconciliation_events": len(self.reconciliation_events),
            "rollback_stack_size": len(self.rollback_stack),
            "temporal_consistency_warnings": self.validate_temporal_consistency(),
            "action_types": {
                action_type.value: len([a for a in self.actions if a.action_type == action_type])
                for action_type in ActionType
            },
            "recent_actions": [
                {
                    "id": action.id,
                    "timestamp": action.timestamp.isoformat(),
                    "type": action.action_type.value,
                    "corrected": action.metadata.get("corrected", False)
                }
                for action in sorted(self.actions, key=lambda x: x.timestamp, reverse=True)[:10]
            ],
            "recent_reconciliations": [
                {
                    "id": event.id,
                    "timestamp": event.timestamp.isoformat(),
                    "original_action_id": event.original_action_id,
                    "reason": event.correction_reason
                }
                for event in sorted(self.reconciliation_events, key=lambda x: x.timestamp, reverse=True)[:5]
            ]
        }
    
    def _find_action(self, action_id: str) -> Optional[Action]:
        """Find an action by its ID."""
        for action in self.actions:
            if action.id == action_id:
                return action
        return None
    
    def _analyze_correction_impact(self, action: Action, truth_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the impact of correcting an action.
        
        Args:
            action: The action being corrected
            truth_data: The truth data
            
        Returns:
            Impact analysis dictionary
        """
        # Find all actions that depend on this one
        impacted_actions = self.get_impacted_actions(action.id)
        
        # Calculate prediction accuracy if this was a prediction
        accuracy_metrics = {}
        if action.action_type == ActionType.PREDICTION:
            predicted_value = action.data.get("predicted_value")
            actual_value = truth_data.get("actual_value")
            
            if predicted_value is not None and actual_value is not None:
                error = abs(predicted_value - actual_value)
                relative_error = error / abs(actual_value) if actual_value != 0 else float('inf')
                
                accuracy_metrics = {
                    "absolute_error": error,
                    "relative_error": relative_error,
                    "predicted_value": predicted_value,
                    "actual_value": actual_value
                }
        
        return {
            "impacted_actions_count": len(impacted_actions),
            "impacted_action_ids": [a.id for a in impacted_actions],
            "accuracy_metrics": accuracy_metrics,
            "correction_magnitude": self._calculate_correction_magnitude(action.data, truth_data)
        }
    
    def _calculate_correction_magnitude(self, original_data: Dict[str, Any], 
                                      truth_data: Dict[str, Any]) -> float:
        """
        Calculate the magnitude of the correction.
        
        Args:
            original_data: Original action data
            truth_data: Truth data
            
        Returns:
            Correction magnitude (0.0 to 1.0)
        """
        # Simple implementation - could be more sophisticated
        if "predicted_value" in original_data and "actual_value" in truth_data:
            pred_val = original_data["predicted_value"]
            actual_val = truth_data["actual_value"]
            
            if pred_val != 0:
                return abs(pred_val - actual_val) / abs(pred_val)
            else:
                return abs(actual_val) if actual_val != 0 else 0.0
        
        return 0.0
    
    def _has_circular_dependency(self, action_id: str, visited: Set[str]) -> bool:
        """
        Check if there's a circular dependency involving the given action.
        
        Args:
            action_id: ID of the action to check
            visited: Set of already visited actions (for cycle detection)
            
        Returns:
            True if circular dependency exists
        """
        if action_id in visited:
            return True
        
        visited.add(action_id)
        action = self._find_action(action_id)
        
        if action is None:
            return False
        
        for dep_id in action.dependencies:
            if self._has_circular_dependency(dep_id, visited.copy()):
                return True
        
        return False
