"""
Unit tests for AI prediction system.
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_prediction import TemporalReasoningEngine, Prediction, Observation


class TestTemporalReasoningEngine:
    """Test cases for TemporalReasoningEngine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = TemporalReasoningEngine()
        
        assert len(engine.observations) == 0
        assert len(engine.predictions) == 0
        assert len(engine.prediction_models) > 0  # Should have default models
        assert "linear_trend" in engine.prediction_models
    
    def test_add_observation(self):
        """Test adding observations."""
        engine = TemporalReasoningEngine()
        
        obs_id = engine.add_observation(
            value=10.0,
            timestamp=datetime.now(),
            uncertainty=0.1,
            source="test"
        )
        
        assert len(engine.observations) == 1
        assert engine.observations[0].value == 10.0
        assert engine.observations[0].uncertainty == 0.1
        assert engine.observations[0].source == "test"
    
    def test_make_prediction(self):
        """Test making predictions."""
        engine = TemporalReasoningEngine()
        
        # Add some observations first
        base_time = datetime.now()
        for i in range(5):
            engine.add_observation(
                value=10.0 + i * 0.5,
                timestamp=base_time + timedelta(minutes=i*10),
                uncertainty=0.1,
                source="test"
            )
        
        # Make a prediction
        target_time = base_time + timedelta(hours=1)
        prediction = engine.make_prediction(
            target_time=target_time,
            model_name="linear_trend",
            confidence_level=0.95
        )
        
        assert isinstance(prediction, Prediction)
        assert prediction.target_time == target_time
        assert prediction.confidence_level == 0.95
        assert len(prediction.confidence_interval) == 2
        assert prediction.confidence_interval[0] < prediction.confidence_interval[1]
        assert len(engine.predictions) == 1
    
    def test_prediction_with_insufficient_data(self):
        """Test prediction with insufficient data."""
        engine = TemporalReasoningEngine()
        
        # Make prediction with no observations
        target_time = datetime.now() + timedelta(hours=1)
        prediction = engine.make_prediction(target_time=target_time)
        
        assert isinstance(prediction, Prediction)
        assert prediction.predicted_value is not None
        assert prediction.uncertainty > 0
    
    def test_update_prediction(self):
        """Test updating predictions with new observations."""
        engine = TemporalReasoningEngine()
        
        # Add initial observations
        base_time = datetime.now()
        for i in range(3):
            engine.add_observation(
                value=10.0 + i * 0.5,
                timestamp=base_time + timedelta(minutes=i*10),
                uncertainty=0.1,
                source="test"
            )
        
        # Make prediction
        target_time = base_time + timedelta(hours=1)
        prediction = engine.make_prediction(target_time=target_time)
        
        # Add new observation
        new_observation = Observation(
            timestamp=base_time + timedelta(minutes=30),
            value=12.0,
            uncertainty=0.1,
            source="truth"
        )
        
        # Update prediction
        updated_prediction = engine.update_prediction(prediction.id, new_observation)
        
        assert updated_prediction.id == prediction.id
        assert len(engine.observations) == 4  # Should have added the new observation
    
    def test_prediction_accuracy_calculation(self):
        """Test prediction accuracy calculation."""
        engine = TemporalReasoningEngine()
        
        # Add observations and make prediction
        base_time = datetime.now()
        engine.add_observation(value=10.0, timestamp=base_time, uncertainty=0.1, source="test")
        engine.add_observation(value=11.0, timestamp=base_time + timedelta(minutes=10), uncertainty=0.1, source="test")
        
        target_time = base_time + timedelta(hours=1)
        prediction = engine.make_prediction(target_time=target_time)
        
        # Calculate accuracy
        actual_value = 12.0
        accuracy = engine.get_prediction_accuracy(prediction.id, actual_value)
        
        assert "absolute_error" in accuracy
        assert "relative_error" in accuracy
        assert "within_confidence_interval" in accuracy
        assert "coverage" in accuracy
        assert accuracy["actual_value"] == actual_value
        assert accuracy["predicted_value"] == prediction.predicted_value
    
    def test_register_custom_model(self):
        """Test registering custom prediction models."""
        engine = TemporalReasoningEngine()
        
        def custom_model(observations, target_time, parameters):
            return 42.0, 1.0  # Always predict 42 with uncertainty 1.0
        
        engine.register_model("custom", custom_model)
        
        assert "custom" in engine.prediction_models
        
        # Test using custom model
        target_time = datetime.now() + timedelta(hours=1)
        prediction = engine.make_prediction(target_time=target_time, model_name="custom")
        
        assert prediction.predicted_value == 42.0
        assert prediction.uncertainty == 1.0
    
    def test_set_model_parameters(self):
        """Test setting model parameters."""
        engine = TemporalReasoningEngine()
        
        parameters = {"alpha": 0.5, "beta": 0.3}
        engine.set_model_parameters(parameters)
        
        assert engine.model_parameters["alpha"] == 0.5
        assert engine.model_parameters["beta"] == 0.3
    
    def test_system_summary(self):
        """Test system summary generation."""
        engine = TemporalReasoningEngine()
        
        # Add some data
        engine.add_observation(value=10.0, timestamp=datetime.now(), uncertainty=0.1, source="test")
        engine.make_prediction(datetime.now() + timedelta(hours=1))
        
        summary = engine.get_system_summary()
        
        assert "num_observations" in summary
        assert "num_predictions" in summary
        assert "available_models" in summary
        assert "model_parameters" in summary
        assert "recent_observations" in summary
        assert "active_predictions" in summary
        
        assert summary["num_observations"] == 1
        assert summary["num_predictions"] == 1
        assert "linear_trend" in summary["available_models"]


class TestObservation:
    """Test cases for Observation dataclass."""
    
    def test_observation_creation(self):
        """Test creating observations."""
        timestamp = datetime.now()
        observation = Observation(
            timestamp=timestamp,
            value=10.0,
            uncertainty=0.1,
            source="test"
        )
        
        assert observation.timestamp == timestamp
        assert observation.value == 10.0
        assert observation.uncertainty == 0.1
        assert observation.source == "test"
        assert observation.metadata == {}


class TestPrediction:
    """Test cases for Prediction dataclass."""
    
    def test_prediction_creation(self):
        """Test creating predictions."""
        timestamp = datetime.now()
        target_time = timestamp + timedelta(hours=1)
        
        prediction = Prediction(
            id="test_id",
            timestamp=timestamp,
            target_time=target_time,
            predicted_value=10.0,
            confidence_interval=(9.0, 11.0),
            confidence_level=0.95,
            uncertainty=0.5
        )
        
        assert prediction.id == "test_id"
        assert prediction.timestamp == timestamp
        assert prediction.target_time == target_time
        assert prediction.predicted_value == 10.0
        assert prediction.confidence_interval == (9.0, 11.0)
        assert prediction.confidence_level == 0.95
        assert prediction.uncertainty == 0.5


if __name__ == "__main__":
    pytest.main([__file__])
