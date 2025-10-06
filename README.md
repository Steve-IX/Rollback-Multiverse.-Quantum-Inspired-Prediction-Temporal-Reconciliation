# 🌌 Rollback Multiverse

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research](https://img.shields.io/badge/type-research-purple.svg)](https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation)

**A cutting-edge research framework implementing quantum-inspired branching and collapse for speculative futures with AI prediction and temporal reasoning.**

The Rollback Multiverse system allows for speculative execution of multiple possible futures until definitive information arrives, combining quantum mechanics principles with AI prediction and rollback reconciliation techniques from distributed systems.

## 🌟 Key Features

### 🔮 Quantum-Inspired Branching
- **Multiple simultaneous futures**: Simulate multiple possible outcomes existing in superposition
- **Wave function collapse**: System collapses to single reality when measurements occur
- **Entropy calculation**: Track uncertainty using von Neumann entropy
- **Branch evolution**: Allow branches to evolve over time using linear transformations
- **Probability normalization**: Ensure all branch probabilities sum to 1.0

### 🤖 AI Prediction Engine
- **Temporal reasoning**: Predict future states based on historical data
- **Multiple prediction models**: Linear trend and exponential smoothing models
- **Confidence intervals**: Provide uncertainty bounds for all predictions
- **Prediction accuracy tracking**: Measure how well predictions match reality
- **Extensible model system**: Easy to add new prediction algorithms

### ⚡ Rollback Reconciliation
- **Timestamp-based ordering**: Ensure deterministic behavior based on action arrival times
- **Truth reconciliation**: Correct predictions when actual values arrive
- **Rollback functionality**: Roll back entire system to any previous timestamp
- **Causal chain tracking**: Maintain dependencies between actions
- **Temporal consistency validation**: Ensure proper temporal ordering

### 🎮 Gaming Environments
- **OneHPDuel**: High-stakes 1 HP combat simulation with double-KO mechanics
- **GridworldChase**: Spatial pursuit dynamics with environmental constraints
- **Network latency simulation**: Realistic network conditions with jitter
- **Rollback performance metrics**: Comprehensive rollback event tracking

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation.git
cd Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation

# Install dependencies
pip install -r requirements.txt

# Run system validation
python test_system.py

# Run comprehensive experiments
python example_usage.py

# Launch interactive notebooks
jupyter notebook notebooks/
```

## 📁 Project Architecture

```
rollback-multiverse/
├── src/                           # Core system modules
│   ├── quantum_branching.py       # AmplitudeBrancher - quantum-inspired branching
│   ├── ai_prediction.py          # AI prediction and temporal reasoning
│   ├── rollback_engine.py        # RollbackReconciler - network latency simulation
│   ├── rollback_reconciliation.py # Advanced rollback reconciliation system
│   ├── simulation_core.py        # DeterministicSimulationCore - unified interface
│   ├── environments.py           # OneHPDuel, GridworldChase environments
│   ├── predictive_agent.py       # PredictiveAgent with quantum hypotheses
│   ├── visualization.py          # Matplotlib plotting and dashboard creation
│   ├── metrics.py                # Performance and accuracy metrics
│   └── experiments/              # Experiment framework
│       ├── exp_configs.py        # Experiment configurations
│       └── run_experiments.py    # Main experiment runner
├── notebooks/                    # Interactive analysis
│   ├── 01_intro_simulation.ipynb # Introduction to the system
│   ├── 02_latency_tradeoffs.ipynb # Network latency impact analysis
│   ├── 03_branch_entropy.ipynb  # Quantum entropy evolution
│   └── 04_qiskit_mapping.ipynb  # Quantum hardware integration
├── experiments/                  # Standalone experiments
│   ├── basic_branching.py        # Fundamental quantum branching demo
│   ├── prediction_accuracy.py    # AI prediction accuracy testing
│   └── rollback_performance.py   # Rollback operation performance
├── tests/                        # Comprehensive test suite
│   ├── test_quantum_branching.py
│   ├── test_ai_prediction.py
│   └── test_rollback_reconciliation.py
├── results/                      # Generated outputs
│   ├── *.png                     # Visualization exports
│   ├── *.json                    # Experiment summaries
│   └── *.csv                     # Tabular data exports
└── rollback-multiverse/          # Package distribution
```

## 🧪 Experiment Matrix

| Environment | Latency (ms) | Jitter (ms) | Rollback Rate | Research Focus |
|-------------|--------------|-------------|---------------|----------------|
| OneHPDuel   | 30           | 5           | Baseline      | High-stakes decision making |
| OneHPDuel   | 100          | 20          | High          | Network stress tolerance |
| Gridworld   | 30           | 5           | Spatial       | Multi-agent coordination |
| Gridworld   | 100          | 20          | High Spatial  | Complex environment dynamics |

## 📊 Key Metrics & Analytics

- **Rollback Rate**: Frequency of rollback events per simulation
- **Prediction Accuracy**: Correctness of opponent action predictions  
- **Entropy Evolution**: Shannon entropy of quantum amplitude distributions
- **Latency Impact**: Performance degradation under network delays
- **Branch Convergence**: How quickly multiple futures collapse to reality
- **Reconciliation Efficiency**: Speed of correction when truth arrives

## 🎯 Usage Examples

### Basic Quantum Branching
```python
from src.quantum_branching import AmplitudeBrancher
import numpy as np

# Initialize quantum branching system
brancher = AmplitudeBrancher(n_hypotheses=4)

# Sample a hypothesis based on quantum amplitudes
hypothesis_index, probabilities = brancher.sample_hypothesis()
print(f"Sampled hypothesis {hypothesis_index} with probabilities: {probabilities}")

# Apply unitary-like mixing (quantum evolution)
brancher.apply_unitary_like_mix(mix=0.1)

# Collapse to specific hypothesis (measurement)
brancher.collapse_to_hypothesis(2)
```

### AI Prediction with Rollback
```python
from src.simulation_core import DeterministicSimulationCore
from datetime import datetime, timedelta
import numpy as np

# Initialize deterministic simulation
simulation = DeterministicSimulationCore(initial_state=np.array([1.0, 0.0]))

# Add observation with uncertainty
simulation.add_observation(value=10.0, uncertainty=0.1, source="sensor")

# Create quantum branches for different futures
simulation.create_branch(new_state=np.array([0.7, 0.3]), probability=0.5)
simulation.create_branch(new_state=np.array([0.2, 0.8]), probability=0.3)

# Make temporal prediction
target_time = datetime.now() + timedelta(hours=1)
prediction, confidence = simulation.make_prediction(target_time)

# Reconcile when truth arrives
simulation.reconcile_prediction(prediction.id, actual_value=12.0)
```

### Gaming Environment with Rollback
```python
from src.environments import OneHPDuel
from src.rollback_engine import RollbackReconciler

# Initialize environment and rollback system
env = OneHPDuel()
rollback_engine = RollbackReconciler()

# Simulate frame with network latency
obs, rewards, info = rollback_engine.simulate_frame(
    env=env,
    a0_local="attack",
    a1_local="block", 
    latency_ms=(50, 75),  # Different latencies for each player
    jitter_ms=(10, 15)    # Network jitter
)

# Check if rollback occurred
if info.get("rollback", False):
    print("Rollback event detected - correcting simulation state")
```

## 🔬 Research Applications

### Speculative Execution
- **Multi-future simulation**: Run multiple possible outcomes simultaneously
- **Quantum-inspired branching**: Apply quantum mechanics principles to classical computing
- **Temporal reasoning**: Understand system evolution over time

### AI Prediction Systems
- **Uncertainty quantification**: Provide confidence bounds for predictions
- **Rollback correction**: Update predictions when ground truth arrives
- **Temporal consistency**: Maintain logical ordering of events

### Network Gaming & Distributed Systems
- **Latency compensation**: Handle network delays in real-time systems
- **Rollback netcode**: Correct for prediction errors in networked games
- **Deterministic simulation**: Ensure reproducible results across systems

## 🧪 Running Experiments

```bash
# Basic quantum branching demonstration
python experiments/basic_branching.py

# AI prediction accuracy testing
python experiments/prediction_accuracy.py

# Rollback performance benchmarking
python experiments/rollback_performance.py

# Comprehensive system example
python example_usage.py

# Run all unit tests
python run_tests.py

# System integration tests
python test_system.py
```

## 🔧 Installation & Dependencies

### Core Requirements
```bash
pip install numpy>=1.21.0 pandas>=1.3.0 matplotlib>=3.5.0
```

### Optional Quantum Integration
```bash
pip install qiskit  # For quantum hardware experiments
```

### Development Dependencies
```bash
pip install pytest jupyter notebook  # For testing and notebooks
```

## 📈 Visualization & Outputs

The system generates rich visualizations and data exports:

- **Branch Evolution Plots**: Quantum amplitude development over time
- **Prediction Accuracy Charts**: AI prediction vs. actual values
- **Rollback Timeline**: When and why rollbacks occur
- **Entropy Evolution**: Uncertainty changes over simulation
- **System Metrics Dashboard**: Comprehensive performance overview

## 🔮 Optional: Qiskit Integration

For quantum hardware experiments, the system can map amplitude distributions to quantum circuits:

```bash
pip install qiskit
jupyter notebook notebooks/04_qiskit_mapping.ipynb
```

This allows you to:
- Run quantum circuits on real hardware
- Compare quantum vs. classical branching behavior
- Explore quantum advantage in prediction systems

## 📚 Documentation

- **[Project Summary](PROJECT_SUMMARY.md)**: Comprehensive technical overview
- **[Jupyter Notebooks](notebooks/)**: Interactive tutorials and analysis
- **[API Documentation](src/)**: Source code with detailed docstrings
- **[Experiment Results](results/)**: Generated outputs and visualizations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](rollback-multiverse/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](rollback-multiverse/LICENSE) file for details.

## 🙏 Acknowledgments

- **Quantum Mechanics**: Inspired by quantum superposition and collapse principles
- **Rollback Netcode**: Techniques from distributed gaming systems
- **AI Prediction**: Methods from temporal reasoning and uncertainty quantification
- **Research Community**: Built for advancing speculative execution research

## 📞 Contact & Links

- **GitHub**: [@Steve-IX](https://github.com/Steve-IX)
- **Repository**: [Rollback Multiverse](https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation)
- **Issues**: [Report bugs or request features](https://github.com/Steve-IX/Rollback-Multiverse.-Quantum-Inspired-Prediction-Temporal-Reconciliation/issues)

---

**🌟 Star this repository if you find it useful for your research!**