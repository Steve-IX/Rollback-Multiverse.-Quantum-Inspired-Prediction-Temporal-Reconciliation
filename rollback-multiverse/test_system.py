#!/usr/bin/env python3
"""
Simple test script for the rollback multiverse system.
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test that all modules can be imported."""
    try:
        from environments import OneHPDuel, GridworldChase
        from quantum_branching import AmplitudeBrancher
        from predictive_agent import PredictiveAgent
        from rollback_engine import RollbackReconciler
        from metrics import MetricsCollector
        print("+ All imports successful")
        return True
    except ImportError as e:
        print(f"- Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of each component."""
    try:
        # Test environment
        from environments import OneHPDuel
        env = OneHPDuel(seed=42)
        obs = env.reset()
        print(f"+ OneHPDuel environment: {obs}")
        
        # Test quantum branching
        from quantum_branching import AmplitudeBrancher
        brancher = AmplitudeBrancher(n_hypotheses=4)
        entropy = brancher.entropy()
        print(f"+ AmplitudeBrancher entropy: {entropy:.3f}")
        
        # Test predictive agent
        from predictive_agent import PredictiveAgent
        agent = PredictiveAgent(["attack", "block", "idle"], seed=0)
        action, probs = agent.predict_opponent()
        print(f"+ PredictiveAgent prediction: {action}")
        
        # Test rollback engine
        from rollback_engine import RollbackReconciler
        engine = RollbackReconciler()
        obs, r0, r1, info = engine.simulate_frame(env, "attack", "block")
        print(f"+ RollbackReconciler: rollback={info['rollback']}")
        
        return True
    except Exception as e:
        print(f"- Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Rollback Multiverse System")
    print("=" * 40)
    
    success = True
    success &= test_imports()
    success &= test_basic_functionality()
    
    if success:
        print("\n+ All tests passed! System is working correctly.")
    else:
        print("\n- Some tests failed. Check the errors above.")
        sys.exit(1)
