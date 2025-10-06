# Rollback Multiverse

A research repository implementing quantum-inspired branching and collapse for speculative futures with AI prediction and temporal reasoning.

## Features

- **Quantum-inspired branching**: Simulate multiple possible futures without real quantum hardware
- **AI prediction**: Temporal reasoning with rollback reconciliation
- **Deterministic simulation**: Explicit reconciliation by action arrival timestamps
- **Reproducible experiments**: CSV outputs and JSON summaries

## Project Structure

```
rollback-multiverse/
├── src/
│   ├── __init__.py
│   ├── quantum_branching.py      # Quantum-inspired branching system
│   ├── ai_prediction.py          # AI prediction and temporal reasoning
│   ├── rollback_reconciliation.py # Rollback reconciliation system
│   ├── simulation_core.py        # Deterministic simulation core
│   └── visualization.py          # Matplotlib plotting utilities
├── experiments/
│   ├── __init__.py
│   ├── basic_branching.py        # Basic branching experiment
│   ├── prediction_accuracy.py    # AI prediction accuracy test
│   └── rollback_performance.py   # Rollback reconciliation performance
├── results/                      # Generated experiment outputs
├── tests/
│   ├── __init__.py
│   ├── test_quantum_branching.py
│   ├── test_ai_prediction.py
│   └── test_rollback_reconciliation.py
├── requirements.txt
└── setup.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run experiments:
```bash
python -m experiments.basic_branching
python -m experiments.prediction_accuracy
python -m experiments.rollback_performance
```

## Core Concepts

### Quantum-inspired Branching
- Simulates multiple possible futures simultaneously
- Each branch represents a different outcome probability
- Collapse occurs when definitive information arrives

### AI Prediction & Temporal Reasoning
- Predicts future states based on current information
- Maintains confidence intervals and uncertainty
- Updates predictions as new information arrives

### Rollback Reconciliation
- Corrects predictions when truth arrives
- Uses timestamp-based ordering for deterministic results
- Maintains audit trail of all corrections
