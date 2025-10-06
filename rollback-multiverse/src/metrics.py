"""
Performance and accuracy metrics for rollback multiverse experiments.
"""

import numpy as np
import pandas as pd


class MetricsCollector:
    """
    Collects and analyzes performance metrics from experiments.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.data = []
    
    def record_frame(self, frame_data):
        """
        Record data from a single frame.
        
        Args:
            frame_data: Dictionary containing frame metrics
        """
        self.data.append(frame_data)
    
    def get_rollback_rate(self):
        """Calculate rollback rate across all frames."""
        if not self.data:
            return 0.0
        
        rollback_frames = sum(1 for frame in self.data if frame.get("rollback", False))
        return rollback_frames / len(self.data)
    
    def get_prediction_accuracy(self):
        """Calculate prediction accuracy."""
        if not self.data:
            return 0.0
        
        correct_predictions = sum(1 for frame in self.data 
                                if frame.get("prediction_correct", False))
        total_predictions = sum(1 for frame in self.data 
                              if "prediction_correct" in frame)
        
        if total_predictions == 0:
            return 0.0
        
        return correct_predictions / total_predictions
    
    def get_entropy_evolution(self):
        """Get entropy evolution over time."""
        entropies = [frame.get("entropy", 0.0) for frame in self.data]
        return np.array(entropies)
    
    def get_latency_impact(self):
        """Calculate latency impact on performance."""
        if not self.data:
            return {}
        
        df = pd.DataFrame(self.data)
        
        # Group by latency and calculate average rollback rate
        if "latency_ms" in df.columns:
            latency_impact = df.groupby("latency_ms")["rollback"].mean().to_dict()
            return latency_impact
        
        return {}
    
    def get_summary_stats(self):
        """Get comprehensive summary statistics."""
        if not self.data:
            return {}
        
        df = pd.DataFrame(self.data)
        
        stats = {
            "total_frames": len(self.data),
            "rollback_rate": self.get_rollback_rate(),
            "prediction_accuracy": self.get_prediction_accuracy(),
            "avg_entropy": np.mean(self.get_entropy_evolution()),
            "entropy_std": np.std(self.get_entropy_evolution()),
            "latency_impact": self.get_latency_impact()
        }
        
        return stats
    
    def reset(self):
        """Reset all collected data."""
        self.data = []
