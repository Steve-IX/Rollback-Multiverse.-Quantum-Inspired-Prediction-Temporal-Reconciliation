"""
AI prediction accuracy experiment.

This experiment tests the accuracy of AI predictions and demonstrates
how the system corrects predictions when truth arrives.
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_prediction import TemporalReasoningEngine, Observation
from visualization import MultiverseVisualizer


def generate_synthetic_data(n_points: int = 50, noise_level: float = 0.1) -> list:
    """
    Generate synthetic time series data with trend and noise.
    
    Args:
        n_points: Number of data points to generate
        noise_level: Level of noise to add
        
    Returns:
        List of (timestamp, value) tuples
    """
    base_time = datetime.now() - timedelta(hours=n_points)
    data = []
    
    for i in range(n_points):
        timestamp = base_time + timedelta(minutes=i*10)
        # Generate trend with some noise
        trend = 0.1 * i  # Linear trend
        noise = np.random.normal(0, noise_level)
        value = 10.0 + trend + noise
        
        data.append((timestamp, value))
    
    return data


def run_prediction_accuracy_experiment():
    """Run the AI prediction accuracy experiment."""
    print("Starting AI Prediction Accuracy Experiment...")
    
    # Initialize prediction engine
    prediction_engine = TemporalReasoningEngine(prediction_horizon=timedelta(hours=2))
    
    # Generate synthetic data
    print("Generating synthetic time series data...")
    synthetic_data = generate_synthetic_data(n_points=30, noise_level=0.2)
    
    # Add observations to the system
    print("Adding observations to prediction engine...")
    for timestamp, value in synthetic_data[:20]:  # Use first 20 points for training
        prediction_engine.add_observation(
            value=value,
            timestamp=timestamp,
            uncertainty=0.1,
            source="synthetic_data"
        )
    
    # Make predictions for future points
    print("Making predictions...")
    predictions = []
    actual_values = []
    
    for i in range(20, 30):  # Predict last 10 points
        timestamp, actual_value = synthetic_data[i]
        target_time = timestamp
        
        # Make prediction
        prediction = prediction_engine.make_prediction(
            target_time=target_time,
            model_name="linear_trend",
            confidence_level=0.95
        )
        
        predictions.append(prediction)
        actual_values.append(actual_value)
        
        # Add the actual observation after prediction
        observation = Observation(
            timestamp=timestamp,
            value=actual_value,
            uncertainty=0.1,
            source="truth"
        )
        
        # Update prediction with actual value
        updated_prediction = prediction_engine.update_prediction(
            prediction.id, observation
        )
        
        print(f"Prediction {i-19}: Predicted={prediction.predicted_value:.2f}, "
              f"Actual={actual_value:.2f}, Error={abs(prediction.predicted_value - actual_value):.2f}")
    
    # Calculate accuracy metrics
    print("Calculating accuracy metrics...")
    accuracy_metrics = []
    
    for prediction, actual_value in zip(predictions, actual_values):
        metrics = prediction_engine.get_prediction_accuracy(prediction.id, actual_value)
        accuracy_metrics.append(metrics)
    
    # Aggregate metrics
    absolute_errors = [m["absolute_error"] for m in accuracy_metrics]
    relative_errors = [m["relative_error"] for m in accuracy_metrics if m["relative_error"] != float('inf')]
    coverage_rate = np.mean([m["coverage"] for m in accuracy_metrics])
    
    summary_metrics = {
        "mean_absolute_error": np.mean(absolute_errors),
        "std_absolute_error": np.std(absolute_errors),
        "mean_relative_error": np.mean(relative_errors) if relative_errors else 0,
        "std_relative_error": np.std(relative_errors) if relative_errors else 0,
        "coverage_rate": coverage_rate,
        "num_predictions": len(predictions)
    }
    
    print(f"Mean Absolute Error: {summary_metrics['mean_absolute_error']:.3f}")
    print(f"Coverage Rate: {summary_metrics['coverage_rate']:.3f}")
    
    # Collect experiment data
    experiment_data = {
        "experiment_name": "prediction_accuracy",
        "timestamp": datetime.now().isoformat(),
        "summary_metrics": summary_metrics,
        "individual_metrics": accuracy_metrics,
        "predictions": [
            {
                "id": pred.id,
                "target_time": pred.target_time.isoformat(),
                "predicted_value": pred.predicted_value,
                "uncertainty": pred.uncertainty,
                "confidence_interval": pred.confidence_interval
            }
            for pred in predictions
        ],
        "actual_values": actual_values,
        "synthetic_data": [
            {"timestamp": ts.isoformat(), "value": val}
            for ts, val in synthetic_data
        ]
    }
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save experiment results
    results_file = "results/prediction_accuracy_results.json"
    with open(results_file, 'w') as f:
        json.dump(experiment_data, f, indent=2)
    
    print(f"Experiment results saved to {results_file}")
    
    # Create CSV summary
    csv_data = []
    for i, (pred, actual, metrics) in enumerate(zip(predictions, actual_values, accuracy_metrics)):
        csv_data.append({
            "prediction_id": i+1,
            "target_time": pred.target_time.isoformat(),
            "predicted_value": pred.predicted_value,
            "actual_value": actual,
            "absolute_error": metrics["absolute_error"],
            "relative_error": metrics["relative_error"],
            "within_confidence_interval": metrics["within_confidence_interval"],
            "uncertainty": pred.uncertainty
        })
    
    csv_df = pd.DataFrame(csv_data)
    csv_file = "results/prediction_accuracy_summary.csv"
    csv_df.to_csv(csv_file, index=False)
    print(f"CSV summary saved to {csv_file}")
    
    # Create visualizations
    print("Creating visualizations...")
    visualizer = MultiverseVisualizer()
    
    # Plot prediction accuracy
    fig1 = visualizer.plot_prediction_accuracy(prediction_engine, "AI Prediction Accuracy Results")
    visualizer.save_plot(fig1, "results/prediction_accuracy_plot.png")
    
    # Plot confidence intervals
    fig2 = visualizer.plot_prediction_confidence_intervals(prediction_engine, "Prediction Confidence Intervals")
    visualizer.save_plot(fig2, "results/prediction_confidence_intervals.png")
    
    print("Visualizations saved to results/")
    
    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)
    print(f"Number of predictions: {summary_metrics['num_predictions']}")
    print(f"Mean Absolute Error: {summary_metrics['mean_absolute_error']:.3f}")
    print(f"Mean Relative Error: {summary_metrics['mean_relative_error']:.3f}")
    print(f"Coverage Rate: {summary_metrics['coverage_rate']:.3f}")
    print(f"Standard Deviation (MAE): {summary_metrics['std_absolute_error']:.3f}")
    print("="*50)
    
    return experiment_data


if __name__ == "__main__":
    run_prediction_accuracy_experiment()
