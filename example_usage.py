"""
Example usage of the rollback multiverse system.

This script demonstrates how to use all components together to create
a complete quantum-inspired branching and prediction system.
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from simulation_core import DeterministicSimulationCore
from visualization import MultiverseVisualizer


def run_comprehensive_example():
    """Run a comprehensive example demonstrating all system capabilities."""
    print("="*60)
    print("ROLLBACK MULTIVERSE - COMPREHENSIVE EXAMPLE")
    print("="*60)
    
    # Initialize the simulation core
    print("\n1. Initializing simulation core...")
    initial_state = np.array([1.0, 0.0])  # Start in |0⟩ state
    simulation = DeterministicSimulationCore(initial_state)
    
    # Add some initial observations
    print("\n2. Adding initial observations...")
    base_time = datetime.now()
    
    for i in range(5):
        value = 10.0 + i * 0.5 + np.random.normal(0, 0.1)
        simulation.add_observation(
            value=value,
            timestamp=base_time + timedelta(minutes=i*10),
            uncertainty=0.1,
            source="sensor_1",
            metadata={"location": "building_a"}
        )
        print(f"   Added observation {i+1}: {value:.2f}")
    
    # Create quantum branches for different scenarios
    print("\n3. Creating quantum branches for different scenarios...")
    
    # Bull market scenario
    bull_state = np.array([0.8, 0.2])
    bull_branch_id, bull_event_id = simulation.create_branch(
        new_state=bull_state,
        probability=0.4,
        metadata={"scenario": "bull_market", "confidence": 0.8}
    )
    print(f"   Created bull market branch: {bull_branch_id[:8]}")
    
    # Bear market scenario
    bear_state = np.array([0.2, 0.8])
    bear_branch_id, bear_event_id = simulation.create_branch(
        new_state=bear_state,
        probability=0.3,
        metadata={"scenario": "bear_market", "confidence": 0.7}
    )
    print(f"   Created bear market branch: {bear_branch_id[:8]}")
    
    # Stable market scenario
    stable_state = np.array([0.5, 0.5])
    stable_branch_id, stable_event_id = simulation.create_branch(
        new_state=stable_state,
        probability=0.3,
        metadata={"scenario": "stable_market", "confidence": 0.6}
    )
    print(f"   Created stable market branch: {stable_branch_id[:8]}")
    
    # Make predictions for different time horizons
    print("\n4. Making predictions for different time horizons...")
    predictions = []
    
    for i in range(3):
        target_time = base_time + timedelta(hours=1 + i*0.5)
        prediction, event_id = simulation.make_prediction(
            target_time=target_time,
            model_name="linear_trend",
            confidence_level=0.95
        )
        predictions.append(prediction)
        print(f"   Prediction {i+1}: {prediction.predicted_value:.2f} ± {prediction.uncertainty:.2f}")
    
    # Simulate truth arriving and reconcile predictions
    print("\n5. Simulating truth arrival and reconciling predictions...")
    
    for i, prediction in enumerate(predictions):
        # Simulate actual value (with some deviation from prediction)
        actual_value = prediction.predicted_value + np.random.normal(0, 0.5)
        
        reconciliation_event_id = simulation.reconcile_prediction(
            prediction_id=prediction.id,
            actual_value=actual_value,
            timestamp=base_time + timedelta(hours=1.2 + i*0.5)
        )
        
        print(f"   Reconciled prediction {i+1}: Actual={actual_value:.2f}, "
              f"Error={abs(prediction.predicted_value - actual_value):.2f}")
    
    # Perform a measurement to collapse the quantum system
    print("\n6. Performing measurement to collapse quantum system...")
    
    # Simulate market data arriving
    market_trend = "bull_market"  # Truth arrives
    market_confidence = 0.9
    
    collapsed_branch, collapse_event_id = simulation.collapse_branch(
        observable="market_trend",
        value=market_trend,
        uncertainty=1.0 - market_confidence
    )
    
    print(f"   Market trend measured: {market_trend}")
    print(f"   Collapsed to branch: {collapsed_branch.id[:8]}")
    print(f"   Branch scenario: {collapsed_branch.metadata.get('scenario', 'unknown')}")
    
    # Demonstrate rollback functionality
    print("\n7. Demonstrating rollback functionality...")
    
    # Add some actions after the collapse
    for i in range(3):
        simulation.add_observation(
            value=15.0 + i * 0.2,
            timestamp=base_time + timedelta(hours=2 + i*0.1),
            uncertainty=0.05,
            source="post_collapse_sensor"
        )
    
    # Rollback to before the post-collapse observations
    rollback_time = base_time + timedelta(hours=1.8)
    rolled_back_events = simulation.rollback_to_timestamp(rollback_time)
    
    print(f"   Rolled back to {rollback_time.strftime('%H:%M:%S')}")
    print(f"   Rolled back {len(rolled_back_events)} events")
    
    # Get comprehensive system metrics
    print("\n8. System metrics and analysis...")
    metrics = simulation.get_simulation_metrics()
    
    print(f"   Total events: {metrics['simulation']['total_events']}")
    print(f"   Quantum entropy: {metrics['quantum_system']['entropy']:.3f}")
    print(f"   Number of observations: {metrics['prediction_engine']['num_observations']}")
    print(f"   Number of predictions: {metrics['prediction_engine']['num_predictions']}")
    print(f"   Reconciliation events: {metrics['reconciliation_system']['reconciliation_events']}")
    
    # Create visualizations
    print("\n9. Creating visualizations...")
    visualizer = MultiverseVisualizer()
    
    # Create results directory
    os.makedirs("results", exist_ok=True)
    
    # Generate all visualizations
    figures = visualizer.create_dashboard(simulation, "results")
    print(f"   Created {len(figures)} visualization plots")
    
    # Export simulation state
    print("\n10. Exporting simulation state...")
    simulation.export_simulation_state("results/comprehensive_example_state.json")
    print("   Simulation state exported to results/comprehensive_example_state.json")
    
    # Create summary report
    print("\n11. Creating summary report...")
    
    summary_report = {
        "experiment_name": "comprehensive_example",
        "timestamp": datetime.now().isoformat(),
        "system_metrics": metrics,
        "branches_created": [
            {"id": bull_branch_id[:8], "scenario": "bull_market", "probability": 0.4},
            {"id": bear_branch_id[:8], "scenario": "bear_market", "probability": 0.3},
            {"id": stable_branch_id[:8], "scenario": "stable_market", "probability": 0.3}
        ],
        "predictions_made": len(predictions),
        "reconciliations_performed": len(predictions),
        "measurement_outcome": market_trend,
        "rollback_operations": 1,
        "collapsed_branch": {
            "id": collapsed_branch.id[:8],
            "scenario": collapsed_branch.metadata.get("scenario", "unknown"),
            "probability": collapsed_branch.probability
        }
    }
    
    with open("results/comprehensive_example_summary.json", 'w') as f:
        json.dump(summary_report, f, indent=2)
    
    print("   Summary report saved to results/comprehensive_example_summary.json")
    
    # Print final summary
    print("\n" + "="*60)
    print("EXPERIMENT COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"Quantum branches created: {len(summary_report['branches_created'])}")
    print(f"Predictions made: {summary_report['predictions_made']}")
    print(f"Reconciliations performed: {summary_report['reconciliations_performed']}")
    print(f"Measurement outcome: {summary_report['measurement_outcome']}")
    print(f"Final quantum entropy: {metrics['quantum_system']['entropy']:.3f}")
    print(f"Total system events: {metrics['simulation']['total_events']}")
    print("\nAll results saved to the 'results/' directory")
    print("="*60)
    
    return summary_report


if __name__ == "__main__":
    run_comprehensive_example()
