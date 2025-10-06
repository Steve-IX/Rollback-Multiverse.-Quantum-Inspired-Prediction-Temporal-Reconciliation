"""
Deterministic simulation core for the rollback multiverse system.

This module provides the main simulation engine that coordinates quantum branching,
AI prediction, and rollback reconciliation in a deterministic manner.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import json

from quantum_branching import QuantumBranchingSystem, BranchState
from ai_prediction import TemporalReasoningEngine, Prediction, Observation
from rollback_reconciliation import RollbackReconciliationSystem, ActionType


@dataclass
class SimulationState:
    """Represents the complete state of a simulation."""
    timestamp: datetime
    quantum_system: QuantumBranchingSystem
    prediction_engine: TemporalReasoningEngine
    reconciliation_system: RollbackReconciliationSystem
    global_state: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class SimulationEvent:
    """Represents an event in the simulation."""
    id: str
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DeterministicSimulationCore:
    """
    Deterministic simulation core that coordinates all components.
    
    This class provides a unified interface for running simulations that combine
    quantum-inspired branching, AI prediction, and rollback reconciliation.
    """
    
    def __init__(self, initial_state: np.ndarray, 
                 prediction_horizon: timedelta = timedelta(hours=1)):
        """
        Initialize the simulation core.
        
        Args:
            initial_state: Initial state vector for the quantum system
            prediction_horizon: Default prediction horizon
        """
        self.quantum_system = QuantumBranchingSystem(initial_state)
        self.prediction_engine = TemporalReasoningEngine(prediction_horizon)
        self.reconciliation_system = RollbackReconciliationSystem()
        
        self.simulation_events: List[SimulationEvent] = []
        self.simulation_history: List[SimulationState] = []
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Initialize with initial state
        self._capture_simulation_state()
    
    def add_observation(self, value: float, timestamp: Optional[datetime] = None,
                       uncertainty: float = 0.0, source: str = "simulation",
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add an observation to the system.
        
        Args:
            value: Observed value
            timestamp: Time of observation
            uncertainty: Measurement uncertainty
            source: Source of the observation
            metadata: Additional metadata
            
        Returns:
            Event ID
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        if metadata is None:
            metadata = {}
        
        # Add to prediction engine
        obs_id = self.prediction_engine.add_observation(
            value, timestamp, uncertainty, source, metadata
        )
        
        # Create reconciliation action
        action_id = self.reconciliation_system.add_action(
            ActionType.OBSERVATION,
            {
                "value": value,
                "uncertainty": uncertainty,
                "source": source,
                "observation_id": obs_id
            },
            timestamp,
            metadata=metadata
        )
        
        # Create simulation event
        event_id = str(uuid.uuid4())
        event = SimulationEvent(
            id=event_id,
            timestamp=timestamp,
            event_type="observation",
            data={
                "value": value,
                "uncertainty": uncertainty,
                "source": source,
                "action_id": action_id,
                "observation_id": obs_id
            },
            source=source,
            metadata=metadata
        )
        
        self.simulation_events.append(event)
        self._trigger_event_handlers("observation", event)
        
        return event_id
    
    def make_prediction(self, target_time: datetime, 
                       model_name: str = "linear_trend",
                       confidence_level: float = 0.95) -> Tuple[Prediction, str]:
        """
        Make a prediction for a future time.
        
        Args:
            target_time: Time to predict for
            model_name: Name of the prediction model
            confidence_level: Confidence level
            
        Returns:
            Tuple of (prediction, event_id)
        """
        # Make prediction
        prediction = self.prediction_engine.make_prediction(
            target_time, model_name, confidence_level
        )
        
        # Create reconciliation action
        action_id = self.reconciliation_system.add_action(
            ActionType.PREDICTION,
            {
                "predicted_value": prediction.predicted_value,
                "uncertainty": prediction.uncertainty,
                "confidence_interval": prediction.confidence_interval,
                "confidence_level": prediction.confidence_level,
                "model": model_name,
                "prediction_id": prediction.id
            },
            prediction.timestamp,
            metadata={"model": model_name}
        )
        
        # Create simulation event
        event_id = str(uuid.uuid4())
        event = SimulationEvent(
            id=event_id,
            timestamp=prediction.timestamp,
            event_type="prediction",
            data={
                "prediction_id": prediction.id,
                "target_time": target_time.isoformat(),
                "predicted_value": prediction.predicted_value,
                "uncertainty": prediction.uncertainty,
                "model": model_name,
                "action_id": action_id
            },
            source="prediction_engine",
            metadata={"model": model_name}
        )
        
        self.simulation_events.append(event)
        self._trigger_event_handlers("prediction", event)
        
        return prediction, event_id
    
    def create_branch(self, new_state: np.ndarray, probability: float,
                     metadata: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
        """
        Create a new quantum branch.
        
        Args:
            new_state: State vector for the new branch
            probability: Probability of this branch
            metadata: Additional metadata
            
        Returns:
            Tuple of (branch_id, event_id)
        """
        if metadata is None:
            metadata = {}
        
        # Create branch in quantum system
        branch_id = self.quantum_system.branch(new_state, probability, metadata)
        
        # Create reconciliation action
        action_id = self.reconciliation_system.add_action(
            ActionType.BRANCH_CREATE,
            {
                "branch_id": branch_id,
                "probability": probability,
                "state_norm": float(np.linalg.norm(new_state))
            },
            datetime.now(),
            metadata=metadata
        )
        
        # Create simulation event
        event_id = str(uuid.uuid4())
        event = SimulationEvent(
            id=event_id,
            timestamp=datetime.now(),
            event_type="branch_create",
            data={
                "branch_id": branch_id,
                "probability": probability,
                "action_id": action_id
            },
            source="quantum_system",
            metadata=metadata
        )
        
        self.simulation_events.append(event)
        self._trigger_event_handlers("branch_create", event)
        
        return branch_id, event_id
    
    def collapse_branch(self, observable: str, value: Any, 
                       uncertainty: float = 0.0) -> Tuple[BranchState, str]:
        """
        Collapse the quantum system to a specific branch.
        
        Args:
            observable: Name of the observable
            value: Measured value
            uncertainty: Measurement uncertainty
            
        Returns:
            Tuple of (collapsed_branch, event_id)
        """
        # Collapse quantum system
        collapsed_branch = self.quantum_system.measure(observable, value, uncertainty)
        
        # Create reconciliation action
        action_id = self.reconciliation_system.add_action(
            ActionType.BRANCH_COLLAPSE,
            {
                "observable": observable,
                "value": value,
                "uncertainty": uncertainty,
                "collapsed_branch_id": collapsed_branch.id
            },
            datetime.now()
        )
        
        # Create simulation event
        event_id = str(uuid.uuid4())
        event = SimulationEvent(
            id=event_id,
            timestamp=datetime.now(),
            event_type="branch_collapse",
            data={
                "observable": observable,
                "value": value,
                "uncertainty": uncertainty,
                "collapsed_branch_id": collapsed_branch.id,
                "action_id": action_id
            },
            source="quantum_system",
            metadata={"observable": observable}
        )
        
        self.simulation_events.append(event)
        self._trigger_event_handlers("branch_collapse", event)
        
        return collapsed_branch, event_id
    
    def reconcile_prediction(self, prediction_id: str, actual_value: float,
                           timestamp: Optional[datetime] = None) -> str:
        """
        Reconcile a prediction with actual truth.
        
        Args:
            prediction_id: ID of the prediction to reconcile
            actual_value: Actual observed value
            timestamp: Time when truth arrived
            
        Returns:
            Event ID
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Find the prediction action
        prediction_action = None
        for action in self.reconciliation_system.actions:
            if (action.action_type == ActionType.PREDICTION and 
                action.data.get("prediction_id") == prediction_id):
                prediction_action = action
                break
        
        if prediction_action is None:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        # Reconcile with truth
        reconciliation_event = self.reconciliation_system.reconcile_with_truth(
            prediction_action.id,
            {"actual_value": actual_value},
            "truth_arrived"
        )
        
        # Update prediction engine
        observation = Observation(
            timestamp=timestamp,
            value=actual_value,
            uncertainty=0.0,  # Truth has no uncertainty
            source="truth",
            metadata={"reconciliation_id": reconciliation_event.id}
        )
        
        self.prediction_engine.update_prediction(prediction_id, observation)
        
        # Create simulation event
        event_id = str(uuid.uuid4())
        event = SimulationEvent(
            id=event_id,
            timestamp=timestamp,
            event_type="reconciliation",
            data={
                "prediction_id": prediction_id,
                "actual_value": actual_value,
                "reconciliation_id": reconciliation_event.id,
                "action_id": prediction_action.id
            },
            source="reconciliation_system",
            metadata={"reconciliation_id": reconciliation_event.id}
        )
        
        self.simulation_events.append(event)
        self._trigger_event_handlers("reconciliation", event)
        
        return event_id
    
    def rollback_to_timestamp(self, target_timestamp: datetime) -> List[str]:
        """
        Rollback the entire simulation to a specific timestamp.
        
        Args:
            target_timestamp: Timestamp to rollback to
            
        Returns:
            List of rolled back event IDs
        """
        # Rollback reconciliation system
        rolled_back_actions = self.reconciliation_system.rollback_to_timestamp(target_timestamp)
        
        # Remove events after target timestamp
        events_to_remove = [
            event for event in self.simulation_events
            if event.timestamp > target_timestamp
        ]
        
        rolled_back_event_ids = [event.id for event in events_to_remove]
        self.simulation_events = [
            event for event in self.simulation_events
            if event.timestamp <= target_timestamp
        ]
        
        # Remove simulation states after target timestamp
        self.simulation_history = [
            state for state in self.simulation_history
            if state.timestamp <= target_timestamp
        ]
        
        # Trigger rollback event handlers
        rollback_event = SimulationEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            event_type="rollback",
            data={
                "target_timestamp": target_timestamp.isoformat(),
                "rolled_back_events": rolled_back_event_ids,
                "rolled_back_actions": rolled_back_actions
            },
            source="simulation_core"
        )
        
        self._trigger_event_handlers("rollback", rollback_event)
        
        return rolled_back_event_ids
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        Register an event handler for specific event types.
        
        Args:
            event_type: Type of event to handle
            handler: Function to call when event occurs
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def get_simulation_metrics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive simulation metrics.
        
        Returns:
            Dictionary of simulation metrics
        """
        # Quantum system metrics
        quantum_metrics = {
            "entropy": self.quantum_system.get_entropy(),
            "num_branches": len(self.quantum_system.branches),
            "is_collapsed": self.quantum_system.is_collapsed
        }
        
        # Prediction engine metrics
        prediction_metrics = {
            "num_observations": len(self.prediction_engine.observations),
            "num_predictions": len(self.prediction_engine.predictions),
            "available_models": list(self.prediction_engine.prediction_models.keys())
        }
        
        # Reconciliation system metrics
        reconciliation_metrics = self.reconciliation_system.get_system_state()
        
        # Simulation metrics
        simulation_metrics = {
            "total_events": len(self.simulation_events),
            "simulation_duration": (
                self.simulation_events[-1].timestamp - self.simulation_events[0].timestamp
            ).total_seconds() if len(self.simulation_events) > 1 else 0,
            "event_types": {
                event_type: len([e for e in self.simulation_events if e.event_type == event_type])
                for event_type in set(e.event_type for e in self.simulation_events)
            }
        }
        
        return {
            "quantum_system": quantum_metrics,
            "prediction_engine": prediction_metrics,
            "reconciliation_system": reconciliation_metrics,
            "simulation": simulation_metrics,
            "timestamp": datetime.now().isoformat()
        }
    
    def export_simulation_state(self, filepath: str) -> None:
        """
        Export the complete simulation state to a JSON file.
        
        Args:
            filepath: Path to save the state file
        """
        state_data = {
            "simulation_metrics": self.get_simulation_metrics(),
            "quantum_system_summary": self.quantum_system.get_branch_summary(),
            "prediction_engine_summary": self.prediction_engine.get_system_summary(),
            "reconciliation_system_state": self.reconciliation_system.get_system_state(),
            "recent_events": [
                {
                    "id": event.id,
                    "timestamp": event.timestamp.isoformat(),
                    "type": event.event_type,
                    "source": event.source,
                    "data": event.data
                }
                for event in self.simulation_events[-20:]  # Last 20 events
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_data, f, indent=2, default=str)
    
    def _capture_simulation_state(self) -> None:
        """Capture the current simulation state."""
        state = SimulationState(
            timestamp=datetime.now(),
            quantum_system=self.quantum_system,
            prediction_engine=self.prediction_engine,
            reconciliation_system=self.reconciliation_system,
            global_state=self.get_simulation_metrics()
        )
        self.simulation_history.append(state)
    
    def _trigger_event_handlers(self, event_type: str, event: SimulationEvent) -> None:
        """Trigger all registered handlers for an event type."""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler for {event_type}: {e}")
