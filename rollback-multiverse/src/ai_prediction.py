"""
AI prediction and temporal reasoning module.

This module implements prediction algorithms that can forecast future states
and maintain confidence intervals, with the ability to update predictions
as new information arrives.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
from scipy import stats
from scipy.optimize import minimize


@dataclass
class Prediction:
    """Represents a single prediction with uncertainty."""
    id: str
    timestamp: datetime
    target_time: datetime
    predicted_value: float
    confidence_interval: Tuple[float, float]
    confidence_level: float
    uncertainty: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    """Represents an observed value at a specific time."""
    timestamp: datetime
    value: float
    uncertainty: float
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class TemporalReasoningEngine:
    """
    AI prediction and temporal reasoning engine.
    
    This class maintains a model of temporal relationships and can make
    predictions about future states with confidence intervals.
    """
    
    def __init__(self, prediction_horizon: timedelta = timedelta(hours=1)):
        """
        Initialize the temporal reasoning engine.
        
        Args:
            prediction_horizon: Default time horizon for predictions
        """
        self.predictions: List[Prediction] = []
        self.observations: List[Observation] = []
        self.prediction_horizon = prediction_horizon
        self.model_parameters: Dict[str, Any] = {}
        self.prediction_models: Dict[str, Callable] = {}
        
        # Initialize default models
        self._initialize_default_models()
    
    def add_observation(self, value: float, timestamp: Optional[datetime] = None,
                       uncertainty: float = 0.0, source: str = "unknown",
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a new observation to the system.
        
        Args:
            value: Observed value
            timestamp: Time of observation (defaults to now)
            uncertainty: Measurement uncertainty
            source: Source of the observation
            metadata: Additional metadata
            
        Returns:
            Observation ID
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        if metadata is None:
            metadata = {}
        
        observation = Observation(
            timestamp=timestamp,
            value=value,
            uncertainty=uncertainty,
            source=source,
            metadata=metadata
        )
        
        self.observations.append(observation)
        return str(uuid.uuid4())
    
    def make_prediction(self, target_time: datetime, 
                       model_name: str = "linear_trend",
                       confidence_level: float = 0.95) -> Prediction:
        """
        Make a prediction for a specific future time.
        
        Args:
            target_time: Time to predict for
            model_name: Name of the prediction model to use
            confidence_level: Confidence level for the prediction interval
            
        Returns:
            Prediction object with uncertainty bounds
        """
        if model_name not in self.prediction_models:
            raise ValueError(f"Unknown model: {model_name}")
        
        model_func = self.prediction_models[model_name]
        predicted_value, uncertainty = model_func(
            self.observations, target_time, self.model_parameters
        )
        
        # Calculate confidence interval
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin_of_error = z_score * uncertainty
        confidence_interval = (
            predicted_value - margin_of_error,
            predicted_value + margin_of_error
        )
        
        prediction = Prediction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            target_time=target_time,
            predicted_value=predicted_value,
            confidence_interval=confidence_interval,
            confidence_level=confidence_level,
            uncertainty=uncertainty,
            metadata={"model": model_name}
        )
        
        self.predictions.append(prediction)
        return prediction
    
    def update_prediction(self, prediction_id: str, new_observation: Observation) -> Prediction:
        """
        Update a prediction based on new observation.
        
        Args:
            prediction_id: ID of the prediction to update
            new_observation: New observation to incorporate
            
        Returns:
            Updated prediction
        """
        prediction = self._find_prediction(prediction_id)
        if prediction is None:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        # Add the new observation
        self.observations.append(new_observation)
        
        # Recalculate the prediction with updated data
        model_name = prediction.metadata.get("model", "linear_trend")
        model_func = self.prediction_models[model_name]
        
        predicted_value, uncertainty = model_func(
            self.observations, prediction.target_time, self.model_parameters
        )
        
        # Update the prediction
        z_score = stats.norm.ppf((1 + prediction.confidence_level) / 2)
        margin_of_error = z_score * uncertainty
        confidence_interval = (
            predicted_value - margin_of_error,
            predicted_value + margin_of_error
        )
        
        prediction.predicted_value = predicted_value
        prediction.uncertainty = uncertainty
        prediction.confidence_interval = confidence_interval
        prediction.timestamp = datetime.now()
        
        return prediction
    
    def get_prediction_accuracy(self, prediction_id: str, 
                              actual_value: float) -> Dict[str, float]:
        """
        Calculate accuracy metrics for a prediction.
        
        Args:
            prediction_id: ID of the prediction to evaluate
            actual_value: Actual observed value
            
        Returns:
            Dictionary with accuracy metrics
        """
        prediction = self._find_prediction(prediction_id)
        if prediction is None:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        error = abs(prediction.predicted_value - actual_value)
        relative_error = error / abs(actual_value) if actual_value != 0 else float('inf')
        
        # Check if actual value is within confidence interval
        within_interval = (
            prediction.confidence_interval[0] <= actual_value <= 
            prediction.confidence_interval[1]
        )
        
        # Calculate prediction interval coverage
        coverage = 1.0 if within_interval else 0.0
        
        return {
            "absolute_error": error,
            "relative_error": relative_error,
            "within_confidence_interval": within_interval,
            "coverage": coverage,
            "predicted_value": prediction.predicted_value,
            "actual_value": actual_value,
            "uncertainty": prediction.uncertainty
        }
    
    def register_model(self, name: str, model_func: Callable) -> None:
        """
        Register a new prediction model.
        
        Args:
            name: Name of the model
            model_func: Function that takes (observations, target_time, parameters)
                       and returns (predicted_value, uncertainty)
        """
        self.prediction_models[name] = model_func
    
    def set_model_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set parameters for prediction models.
        
        Args:
            parameters: Dictionary of model parameters
        """
        self.model_parameters.update(parameters)
    
    def _initialize_default_models(self) -> None:
        """Initialize default prediction models."""
        
        def linear_trend_model(observations: List[Observation], 
                             target_time: datetime,
                             parameters: Dict[str, Any]) -> Tuple[float, float]:
            """Linear trend model with uncertainty estimation."""
            if len(observations) < 2:
                # Not enough data for trend
                if observations:
                    return observations[-1].value, observations[-1].uncertainty
                return 0.0, 1.0
            
            # Convert to numpy arrays for easier computation
            times = np.array([(obs.timestamp - observations[0].timestamp).total_seconds() 
                            for obs in observations])
            values = np.array([obs.value for obs in observations])
            uncertainties = np.array([obs.uncertainty for obs in observations])
            
            # Weighted linear regression
            weights = 1.0 / (uncertainties ** 2 + 1e-6)  # Avoid division by zero
            
            # Calculate weighted least squares
            X = np.column_stack([np.ones(len(times)), times])
            W = np.diag(weights)
            
            try:
                beta = np.linalg.inv(X.T @ W @ X) @ X.T @ W @ values
                predicted_value = beta[0] + beta[1] * (target_time - observations[0].timestamp).total_seconds()
                
                # Estimate uncertainty based on residuals
                residuals = values - (X @ beta)
                mse = np.mean(residuals ** 2)
                uncertainty = np.sqrt(mse)
                
            except np.linalg.LinAlgError:
                # Fallback to simple average
                predicted_value = np.mean(values)
                uncertainty = np.std(values)
            
            return predicted_value, uncertainty
        
        def exponential_smoothing_model(observations: List[Observation],
                                      target_time: datetime,
                                      parameters: Dict[str, Any]) -> Tuple[float, float]:
            """Exponential smoothing model."""
            alpha = parameters.get("alpha", 0.3)
            
            if not observations:
                return 0.0, 1.0
            
            # Simple exponential smoothing
            smoothed_value = observations[0].value
            for obs in observations[1:]:
                smoothed_value = alpha * obs.value + (1 - alpha) * smoothed_value
            
            # Estimate uncertainty from recent observations
            recent_uncertainties = [obs.uncertainty for obs in observations[-5:]]
            uncertainty = np.mean(recent_uncertainties) if recent_uncertainties else 1.0
            
            return smoothed_value, uncertainty
        
        # Register default models
        self.register_model("linear_trend", linear_trend_model)
        self.register_model("exponential_smoothing", exponential_smoothing_model)
    
    def _find_prediction(self, prediction_id: str) -> Optional[Prediction]:
        """Find a prediction by its ID."""
        for prediction in self.predictions:
            if prediction.id == prediction_id:
                return prediction
        return None
    
    def get_system_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the prediction system state.
        
        Returns:
            Dictionary containing system information
        """
        return {
            "num_observations": len(self.observations),
            "num_predictions": len(self.predictions),
            "available_models": list(self.prediction_models.keys()),
            "model_parameters": self.model_parameters,
            "prediction_horizon_seconds": self.prediction_horizon.total_seconds(),
            "recent_observations": [
                {
                    "timestamp": obs.timestamp.isoformat(),
                    "value": obs.value,
                    "uncertainty": obs.uncertainty,
                    "source": obs.source
                }
                for obs in self.observations[-5:]  # Last 5 observations
            ],
            "active_predictions": [
                {
                    "id": pred.id,
                    "target_time": pred.target_time.isoformat(),
                    "predicted_value": pred.predicted_value,
                    "uncertainty": pred.uncertainty,
                    "confidence_level": pred.confidence_level
                }
                for pred in self.predictions[-10:]  # Last 10 predictions
            ]
        }
