"""
Rollback reconciliation performance experiment.

This experiment tests the performance and correctness of the rollback
reconciliation system under various scenarios.
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys
import time

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation_core import DeterministicSimulationCore
from rollback_reconciliation import ActionType
from visualization import MultiverseVisualizer


def run_rollback_performance_experiment():
    """Run the rollback reconciliation performance experiment."""
    print("Starting Rollback Reconciliation Performance Experiment...")
    
    # Initialize simulation core
    initial_state = np.array([1.0, 0.0])
    simulation_core = DeterministicSimulationCore(initial_state)
    
    # Scenario 1: Multiple predictions with corrections
    print("Scenario 1: Multiple predictions with corrections...")
    
    # Add some initial observations
    base_time = datetime.now()
    for i in range(5):
        simulation_core.add_observation(
            value=10.0 + i * 0.5 + np.random.normal(0, 0.1),
            timestamp=base_time + timedelta(minutes=i*10),
            uncertainty=0.1,
            source="sensor"
        )
    
    # Make multiple predictions
    prediction_ids = []
    for i in range(3):
        target_time = base_time + timedelta(minutes=50 + i*20)
        prediction, event_id = simulation_core.make_prediction(
            target_time=target_time,
            model_name="linear_trend",
            confidence_level=0.95
        )
        prediction_ids.append(prediction.id)
        print(f"Made prediction {i+1}: {prediction.predicted_value:.2f}")
    
    # Simulate truth arriving and reconcile predictions
    print("Reconciling predictions with truth...")
    reconciliation_times = []
    
    for i, pred_id in enumerate(prediction_ids):
        # Simulate actual value (with some deviation from prediction)
        actual_value = 12.0 + i * 0.3 + np.random.normal(0, 0.2)
        
        start_time = time.time()
        event_id = simulation_core.reconcile_prediction(
            prediction_id=pred_id,
            actual_value=actual_value,
            timestamp=base_time + timedelta(minutes=60 + i*20)
        )
        end_time = time.time()
        
        reconciliation_times.append(end_time - start_time)
        print(f"Reconciled prediction {i+1}: Actual={actual_value:.2f}, "
              f"Time={reconciliation_times[-1]*1000:.2f}ms")
    
    # Scenario 2: Rollback operations
    print("\nScenario 2: Rollback operations...")
    
    # Add more actions after predictions
    for i in range(3):
        simulation_core.add_observation(
            value=15.0 + i * 0.2,
            timestamp=base_time + timedelta(minutes=100 + i*10),
            uncertainty=0.1,
            source="sensor"
        )
    
    # Perform rollback to before the last observations
    rollback_time = base_time + timedelta(minutes=95)
    start_time = time.time()
    rolled_back_events = simulation_core.rollback_to_timestamp(rollback_time)
    end_time = time.time()
    
    rollback_time_ms = (end_time - start_time) * 1000
    print(f"Rollback completed in {rollback_time_ms:.2f}ms")
    print(f"Rolled back {len(rolled_back_events)} events")
    
    # Scenario 3: Stress test with many actions
    print("\nScenario 3: Stress test with many actions...")
    
    stress_test_start = time.time()
    num_actions = 100
    
    for i in range(num_actions):
        if i % 3 == 0:
            # Add observation
            simulation_core.add_observation(
                value=20.0 + i * 0.1 + np.random.normal(0, 0.05),
                timestamp=base_time + timedelta(minutes=200 + i*2),
                uncertainty=0.05,
                source="stress_test"
            )
        elif i % 3 == 1:
            # Make prediction
            target_time = base_time + timedelta(minutes=200 + i*2 + 10)
            prediction, _ = simulation_core.make_prediction(
                target_time=target_time,
                model_name="linear_trend"
            )
        else:
            # Create quantum branch
            new_state = np.array([0.5 + i*0.001, 0.5 - i*0.001])
            simulation_core.create_branch(
                new_state=new_state,
                probability=0.1,
                metadata={"stress_test": True}
            )
    
    stress_test_end = time.time()
    stress_test_time = stress_test_end - stress_test_start
    
    print(f"Stress test completed: {num_actions} actions in {stress_test_time:.3f}s")
    print(f"Average time per action: {stress_test_time/num_actions*1000:.2f}ms")
    
    # Collect performance metrics
    performance_metrics = {
        "reconciliation_times_ms": reconciliation_times,
        "mean_reconciliation_time_ms": np.mean(reconciliation_times),
        "std_reconciliation_time_ms": np.std(reconciliation_times),
        "rollback_time_ms": rollback_time_ms,
        "rolled_back_events": len(rolled_back_events),
        "stress_test_time_s": stress_test_time,
        "stress_test_actions": num_actions,
        "avg_action_time_ms": stress_test_time/num_actions*1000
    }
    
    # Get system state
    system_state = simulation_core.get_simulation_metrics()
    
    # Collect experiment data
    experiment_data = {
        "experiment_name": "rollback_performance",
        "timestamp": datetime.now().isoformat(),
        "performance_metrics": performance_metrics,
        "system_state": system_state,
        "scenarios": {
            "predictions_made": len(prediction_ids),
            "reconciliations_performed": len(reconciliation_times),
            "rollback_operations": 1,
            "stress_test_actions": num_actions
        }
    }
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save experiment results
    results_file = "results/rollback_performance_results.json"
    with open(results_file, 'w') as f:
        json.dump(experiment_data, f, indent=2)
    
    print(f"Experiment results saved to {results_file}")
    
    # Create CSV summary
    csv_data = []
    
    # Reconciliation performance data
    for i, recon_time in enumerate(reconciliation_times):
        csv_data.append({
            "operation_type": "reconciliation",
            "operation_id": i+1,
            "time_ms": recon_time * 1000,
            "timestamp": datetime.now().isoformat()
        })
    
    # Rollback performance data
    csv_data.append({
        "operation_type": "rollback",
        "operation_id": 1,
        "time_ms": rollback_time_ms,
        "timestamp": datetime.now().isoformat()
    })
    
    # Stress test data
    csv_data.append({
        "operation_type": "stress_test",
        "operation_id": 1,
        "time_ms": stress_test_time * 1000,
        "timestamp": datetime.now().isoformat()
    })
    
    csv_df = pd.DataFrame(csv_data)
    csv_file = "results/rollback_performance_summary.csv"
    csv_df.to_csv(csv_file, index=False)
    print(f"CSV summary saved to {csv_file}")
    
    # Create visualizations
    print("Creating visualizations...")
    visualizer = MultiverseVisualizer()
    
    # Create comprehensive dashboard
    figures = visualizer.create_dashboard(simulation_core, "results")
    
    print("Visualizations saved to results/")
    
    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)
    print(f"Reconciliations performed: {len(reconciliation_times)}")
    print(f"Mean reconciliation time: {performance_metrics['mean_reconciliation_time_ms']:.2f}ms")
    print(f"Rollback time: {performance_metrics['rollback_time_ms']:.2f}ms")
    print(f"Stress test: {num_actions} actions in {stress_test_time:.3f}s")
    print(f"Average action time: {performance_metrics['avg_action_time_ms']:.2f}ms")
    print(f"Total events in system: {system_state['simulation']['total_events']}")
    print("="*50)
    
    return experiment_data


if __name__ == "__main__":
    run_rollback_performance_experiment()
