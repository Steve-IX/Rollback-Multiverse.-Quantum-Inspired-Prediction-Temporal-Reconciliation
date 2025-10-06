"""
Visualization utilities for the rollback multiverse system.

This module provides matplotlib-based plotting functions for visualizing
quantum branching, predictions, and reconciliation events.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import matplotlib.dates as mdates

from quantum_branching import QuantumBranchingSystem, BranchState
from ai_prediction import TemporalReasoningEngine, Prediction, Observation
from rollback_reconciliation import RollbackReconciliationSystem
from simulation_core import DeterministicSimulationCore


class MultiverseVisualizer:
    """
    Visualization class for the rollback multiverse system.
    
    Provides various plotting functions for analyzing simulation results.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (10, 6)):
        """
        Initialize the visualizer.
        
        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
    
    def plot_quantum_branches(self, quantum_system: QuantumBranchingSystem,
                            title: str = "Quantum Branch Evolution") -> plt.Figure:
        """
        Plot the evolution of quantum branches over time.
        
        Args:
            quantum_system: The quantum branching system to visualize
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Get branch summary
        summary = quantum_system.get_branch_summary()
        
        if not summary["branches"]:
            ax.text(0.5, 0.5, "No branches to display", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig
        
        # Extract data for plotting
        branch_ids = [branch["id"][:8] for branch in summary["branches"]]  # Short IDs
        probabilities = [branch["probability"] for branch in summary["branches"]]
        state_norms = [branch["state_norm"] for branch in summary["branches"]]
        
        # Create bar plot
        x_pos = np.arange(len(branch_ids))
        bars = ax.bar(x_pos, probabilities, alpha=0.7)
        
        # Add state norm as secondary y-axis
        ax2 = ax.twinx()
        line = ax2.plot(x_pos, state_norms, 'ro-', linewidth=2, markersize=6)
        
        # Customize plot
        ax.set_xlabel("Branch ID")
        ax.set_ylabel("Probability", color='blue')
        ax2.set_ylabel("State Norm", color='red')
        ax.set_title(title)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(branch_ids, rotation=45)
        
        # Add entropy information
        entropy = summary["entropy"]
        ax.text(0.02, 0.98, f"Entropy: {entropy:.3f}", 
               transform=ax.transAxes, va='top', ha='left',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def plot_prediction_accuracy(self, prediction_engine: TemporalReasoningEngine,
                               title: str = "Prediction Accuracy Over Time") -> plt.Figure:
        """
        Plot prediction accuracy metrics over time.
        
        Args:
            prediction_engine: The prediction engine to analyze
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Extract observations and predictions
        observations = prediction_engine.observations
        predictions = prediction_engine.predictions
        
        if not observations or not predictions:
            ax.text(0.5, 0.5, "Insufficient data for accuracy plot", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig
        
        # Convert to pandas for easier manipulation
        obs_df = pd.DataFrame([
            {
                'timestamp': obs.timestamp,
                'value': obs.value,
                'uncertainty': obs.uncertainty
            }
            for obs in observations
        ])
        
        pred_df = pd.DataFrame([
            {
                'timestamp': pred.timestamp,
                'target_time': pred.target_time,
                'predicted_value': pred.predicted_value,
                'uncertainty': pred.uncertainty
            }
            for pred in predictions
        ])
        
        # Plot observations
        ax.errorbar(obs_df['timestamp'], obs_df['value'], 
                   yerr=obs_df['uncertainty'], fmt='o', 
                   label='Observations', capsize=5)
        
        # Plot predictions
        ax.errorbar(pred_df['target_time'], pred_df['predicted_value'],
                   yerr=pred_df['uncertainty'], fmt='s',
                   label='Predictions', capsize=5)
        
        # Customize plot
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_reconciliation_events(self, reconciliation_system: RollbackReconciliationSystem,
                                 title: str = "Reconciliation Events Timeline") -> plt.Figure:
        """
        Plot the timeline of reconciliation events.
        
        Args:
            reconciliation_system: The reconciliation system to visualize
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Get system state
        state = reconciliation_system.get_system_state()
        
        if not state["recent_reconciliations"]:
            ax.text(0.5, 0.5, "No reconciliation events to display", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig
        
        # Extract reconciliation data
        reconciliations = state["recent_reconciliations"]
        timestamps = [datetime.fromisoformat(r["timestamp"]) for r in reconciliations]
        reasons = [r["reason"] for r in reconciliations]
        
        # Create timeline plot
        y_pos = np.arange(len(timestamps))
        ax.scatter(timestamps, y_pos, s=100, alpha=0.7)
        
        # Add labels
        for i, (timestamp, reason) in enumerate(zip(timestamps, reasons)):
            ax.annotate(reason, (timestamp, i), 
                       xytext=(10, 0), textcoords='offset points',
                       fontsize=8, ha='left')
        
        # Customize plot
        ax.set_xlabel("Time")
        ax.set_ylabel("Reconciliation Event")
        ax.set_title(title)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"Event {i+1}" for i in range(len(timestamps))])
        ax.grid(True, alpha=0.3)
        
        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def plot_simulation_metrics(self, simulation_core: DeterministicSimulationCore,
                              title: str = "Simulation Metrics Overview") -> plt.Figure:
        """
        Plot comprehensive simulation metrics.
        
        Args:
            simulation_core: The simulation core to analyze
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Get metrics
        metrics = simulation_core.get_simulation_metrics()
        
        # Plot 1: Event types distribution
        event_types = metrics["simulation"]["event_types"]
        if event_types:
            ax1.pie(event_types.values(), labels=event_types.keys(), autopct='%1.1f%%')
            ax1.set_title("Event Types Distribution")
        else:
            ax1.text(0.5, 0.5, "No events", ha='center', va='center', transform=ax1.transAxes)
            ax1.set_title("Event Types Distribution")
        
        # Plot 2: Quantum system entropy over time
        quantum_metrics = metrics["quantum_system"]
        ax2.bar(["Entropy"], [quantum_metrics["entropy"]])
        ax2.set_title("Quantum System Entropy")
        ax2.set_ylabel("Entropy")
        
        # Plot 3: Prediction vs Observation counts
        pred_metrics = metrics["prediction_engine"]
        categories = ["Observations", "Predictions"]
        counts = [pred_metrics["num_observations"], pred_metrics["num_predictions"]]
        ax3.bar(categories, counts)
        ax3.set_title("Data Points")
        ax3.set_ylabel("Count")
        
        # Plot 4: Reconciliation system state
        recon_metrics = metrics["reconciliation_system"]
        action_types = recon_metrics["action_types"]
        if action_types:
            ax4.bar(action_types.keys(), action_types.values())
            ax4.set_title("Action Types")
            ax4.set_ylabel("Count")
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax4.text(0.5, 0.5, "No actions", ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title("Action Types")
        
        plt.suptitle(title)
        plt.tight_layout()
        return fig
    
    def plot_branch_probability_evolution(self, quantum_system: QuantumBranchingSystem,
                                        title: str = "Branch Probability Evolution") -> plt.Figure:
        """
        Plot how branch probabilities evolve over time.
        
        Args:
            quantum_system: The quantum branching system
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # This is a simplified version - in a real implementation,
        # you would track probability evolution over time
        summary = quantum_system.get_branch_summary()
        
        if not summary["branches"]:
            ax.text(0.5, 0.5, "No branches to display", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig
        
        # Extract current branch data
        branch_ids = [branch["id"][:8] for branch in summary["branches"]]
        probabilities = [branch["probability"] for branch in summary["branches"]]
        
        # Create probability distribution plot
        ax.bar(branch_ids, probabilities, alpha=0.7)
        ax.set_xlabel("Branch ID")
        ax.set_ylabel("Probability")
        ax.set_title(title)
        ax.set_ylim(0, 1)
        
        # Add probability sum check
        total_prob = sum(probabilities)
        ax.text(0.02, 0.98, f"Total Probability: {total_prob:.3f}", 
               transform=ax.transAxes, va='top', ha='left',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    def plot_prediction_confidence_intervals(self, prediction_engine: TemporalReasoningEngine,
                                           title: str = "Prediction Confidence Intervals") -> plt.Figure:
        """
        Plot prediction confidence intervals over time.
        
        Args:
            prediction_engine: The prediction engine
            title: Plot title
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        predictions = prediction_engine.predictions
        
        if not predictions:
            ax.text(0.5, 0.5, "No predictions to display", 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return fig
        
        # Extract prediction data
        target_times = [pred.target_time for pred in predictions]
        predicted_values = [pred.predicted_value for pred in predictions]
        lower_bounds = [pred.confidence_interval[0] for pred in predictions]
        upper_bounds = [pred.confidence_interval[1] for pred in predictions]
        
        # Plot confidence intervals
        ax.fill_between(target_times, lower_bounds, upper_bounds, 
                       alpha=0.3, label='Confidence Interval')
        ax.plot(target_times, predicted_values, 'o-', 
               label='Predicted Values', linewidth=2)
        
        # Customize plot
        ax.set_xlabel("Target Time")
        ax.set_ylabel("Value")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def save_plot(self, fig: plt.Figure, filepath: str, dpi: int = 300) -> None:
        """
        Save a plot to file.
        
        Args:
            fig: matplotlib Figure object
            filepath: Path to save the plot
            dpi: Resolution for saved plot
        """
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
    
    def create_dashboard(self, simulation_core: DeterministicSimulationCore,
                        save_path: Optional[str] = None) -> List[plt.Figure]:
        """
        Create a comprehensive dashboard of all visualizations.
        
        Args:
            simulation_core: The simulation core to visualize
            save_path: Optional path to save all plots
            
        Returns:
            List of matplotlib Figure objects
        """
        figures = []
        
        # Create all plots
        figures.append(self.plot_quantum_branches(simulation_core.quantum_system))
        figures.append(self.plot_prediction_accuracy(simulation_core.prediction_engine))
        figures.append(self.plot_reconciliation_events(simulation_core.reconciliation_system))
        figures.append(self.plot_simulation_metrics(simulation_core))
        figures.append(self.plot_branch_probability_evolution(simulation_core.quantum_system))
        figures.append(self.plot_prediction_confidence_intervals(simulation_core.prediction_engine))
        
        # Save plots if path provided
        if save_path:
            for i, fig in enumerate(figures):
                filename = f"{save_path}/dashboard_plot_{i+1}.png"
                self.save_plot(fig, filename)
        
        return figures
