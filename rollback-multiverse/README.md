# Rollback Multiverse

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A research framework implementing quantum-inspired branching and collapse for speculative futures with AI prediction and temporal reasoning. This system allows for speculative execution of multiple possible futures until definitive information arrives.

## 🌟 Features

- **Quantum-inspired branching**: Simulate multiple possible futures without real quantum hardware
- **AI prediction**: Temporal reasoning with rollback reconciliation  
- **Deterministic simulation**: Explicit reconciliation by action arrival timestamps
- **Reproducible experiments**: CSV outputs and JSON summaries
- **Comprehensive visualization**: Rich plots for understanding system behavior

## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation.git
cd rollback-multiverse

# Install dependencies
pip install -r requirements.txt

# Run system tests
python test_system.py

# Run experiments
python -m src.experiments.run_experiments

# Run comprehensive example
python example_usage.py
```

## 📁 Project Structure

```
rollback-multiverse/
├── src/
│   ├── __init__.py
│   ├── environments.py          # OneHPDuel, GridworldChase environments
│   ├── quantum_branching.py     # AmplitudeBrancher implementation
│   ├── predictive_agent.py      # PredictiveAgent with quantum hypotheses
│   ├── rollback_engine.py       # RollbackReconciler for latency simulation
│   ├── rollback_reconciliation.py # Advanced rollback reconciliation system
│   ├── ai_prediction.py         # AI prediction and temporal reasoning
│   ├── simulation_core.py       # Deterministic simulation core
│   ├── visualization.py         # Matplotlib plotting utilities
│   ├── metrics.py               # Performance and accuracy metrics
│   └── experiments/
│       ├── __init__.py
│       ├── exp_configs.py       # Experiment configurations
│       └── run_experiments.py   # Main experiment runner
├── notebooks/                   # Jupyter notebooks for analysis
│   ├── 01_intro_simulation.ipynb
│   ├── 02_latency_tradeoffs.ipynb
│   ├── 03_branch_entropy.ipynb
│   └── 04_qiskit_mapping.ipynb
├── tests/                       # Unit tests
│   ├── test_quantum_branching.py
│   ├── test_ai_prediction.py
│   └── test_rollback_reconciliation.py
├── results/                     # Generated experiment outputs
├── requirements.txt
├── setup.py
├── test_system.py
├── example_usage.py
└── PROJECT_SUMMARY.md
```

## 🔬 Core Concepts

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

## 📊 Key Metrics

- **Rollback Rate**: Frequency of rollback events per simulation
- **Prediction Accuracy**: Correctness of opponent action predictions
- **Entropy Evolution**: Shannon entropy of quantum amplitude distributions
- **Latency Impact**: Performance degradation under network delays

## 🧪 Experiment Matrix

| Environment | Latency (ms) | Jitter (ms) | Rollback Rate | Notes |
|-------------|--------------|-------------|---------------|-------|
| OneHPDuel   | 30           | 5           | Baseline      | 1 HP double-KO |
| OneHPDuel   | 100          | 20          | High          | Network stress |
| Gridworld   | 30           | 5           | Spatial       | Chase dynamics |

## 🎯 Usage Examples

### Basic Usage
```python
from src.simulation_core import DeterministicSimulationCore
import numpy as np
from datetime import datetime, timedelta

# Initialize system
simulation = DeterministicSimulationCore(np.array([1.0, 0.0]))

# Add observations
simulation.add_observation(value=10.0, uncertainty=0.1, source="sensor")

# Create quantum branches
simulation.create_branch(new_state=np.array([0.7, 0.3]), probability=0.5)

# Make predictions
prediction, _ = simulation.make_prediction(target_time=datetime.now() + timedelta(hours=1))

# Reconcile when truth arrives
simulation.reconcile_prediction(prediction.id, actual_value=12.0)
```

### Running Experiments
```bash
# Run basic branching experiment
python experiments/basic_branching.py

# Run prediction accuracy test
python experiments/prediction_accuracy.py

# Run rollback performance test
python experiments/rollback_performance.py

# Run comprehensive example
python example_usage.py

# Run all tests
python run_tests.py
```

## 🔧 Installation

### Requirements
- Python 3.8+
- NumPy >= 1.21.0
- Pandas >= 1.3.0
- Matplotlib >= 3.5.0

### Optional Dependencies
- Qiskit (for quantum hardware experiments): `pip install qiskit`

## 🧪 Testing

```bash
# Run system tests
python test_system.py

# Run unit tests
python run_tests.py

# Run specific test modules
python -m pytest tests/test_quantum_branching.py
python -m pytest tests/test_ai_prediction.py
python -m pytest tests/test_rollback_reconciliation.py
```

## 📈 Research Applications

This system is designed for research in:
- **Speculative execution**: Running multiple possible futures simultaneously
- **AI prediction accuracy**: Measuring and improving prediction quality
- **Temporal reasoning**: Understanding how systems evolve over time
- **Quantum-inspired computing**: Exploring quantum-like behavior in classical systems
- **Rollback mechanisms**: Correcting predictions when truth arrives

## 🔮 Optional: Qiskit Integration

For quantum hardware experiments, install qiskit and use `notebooks/04_qiskit_mapping.ipynb` to map amplitude distributions to quantum circuits:

```bash
pip install qiskit
jupyter notebook notebooks/04_qiskit_mapping.ipynb
```

## 📚 Documentation

- [Project Summary](PROJECT_SUMMARY.md) - Comprehensive overview of the system
- [Jupyter Notebooks](notebooks/) - Interactive analysis and demonstrations
- [API Documentation](src/) - Source code with comprehensive docstrings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Quantum computing concepts inspired by quantum mechanics
- Rollback netcode techniques from game development
- AI prediction methods from machine learning research

## 📞 Contact

- GitHub: [@Steve-IX](https://github.com/Steve-IX)
- Repository: [Rollback-Multiverse](https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation)
