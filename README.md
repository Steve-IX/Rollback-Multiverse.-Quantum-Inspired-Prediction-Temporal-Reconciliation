# Rollback Multiverse

A research framework for exploring quantum-inspired branching and rollback reconciliation in deterministic simulations.

## Quickstart

```bash
pip install -r requirements.txt
python -m src.experiments.run_experiments
```

## Project Structure

```
rollback-multiverse/
├── src/
│   ├── environments.py      # OneHPDuel, GridworldChase environments
│   ├── quantum_branching.py # AmplitudeBrancher implementation
│   ├── predictive_agent.py  # PredictiveAgent with quantum hypotheses
│   ├── rollback_engine.py   # RollbackReconciler for latency simulation
│   ├── metrics.py           # Performance and accuracy metrics
│   └── experiments/         # Experiment configurations and runners
├── notebooks/               # Jupyter notebooks for analysis
└── results/                 # Experiment outputs
```

## Key Metrics

- **Rollback Rate**: Frequency of rollback events per simulation
- **Prediction Accuracy**: Correctness of opponent action predictions
- **Entropy Evolution**: Shannon entropy of quantum amplitude distributions
- **Latency Impact**: Performance degradation under network delays

## Experiment Matrix

| Environment | Latency (ms) | Jitter (ms) | Rollback Rate | Notes |
|-------------|--------------|-------------|---------------|-------|
| OneHPDuel   | 30           | 5           | Baseline      | 1 HP double-KO |
| OneHPDuel   | 100          | 20          | High          | Network stress |
| Gridworld   | 30           | 5           | Spatial       | Chase dynamics |

## Optional: Qiskit Integration

For quantum hardware experiments, install qiskit and use `notebooks/04_qiskit_mapping.ipynb` to map amplitude distributions to quantum circuits.