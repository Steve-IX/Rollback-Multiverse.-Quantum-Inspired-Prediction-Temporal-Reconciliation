"""
Test runner for the rollback multiverse system.

This script runs all unit tests to verify the system works correctly.
"""

import sys
import os
import subprocess

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def run_tests():
    """Run all unit tests."""
    print("Running unit tests for rollback multiverse system...")
    print("="*60)
    
    test_files = [
        "tests/test_quantum_branching.py",
        "tests/test_ai_prediction.py", 
        "tests/test_rollback_reconciliation.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        print(f"\nRunning {test_file}...")
        try:
            result = subprocess.run([sys.executable, test_file], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✓ {test_file} passed")
            else:
                print(f"✗ {test_file} failed")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"✗ {test_file} timed out")
            all_passed = False
        except Exception as e:
            print(f"✗ {test_file} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
