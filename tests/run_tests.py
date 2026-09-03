"""
Standalone Python Test Runner Script.
Runs all pytest test cases and reports results cleanly.
"""
import sys
import os

# Set current directory to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

def run():
    print("=" * 70)
    print("🧪 Running Employee REST API Automated Test Suite")
    print("=" * 70)
    
    try:
        import pytest
        # Run pytest programmatically
        exit_code = pytest.main([
            os.path.join(PROJECT_ROOT, 'tests'),
            '-v',
            '--tb=short',
            '-s'
        ])
        if exit_code == 0:
            print("\n✅ All API tests PASSED successfully!")
        else:
            print(f"\n❌ Test suite failed with exit code: {exit_code}")
        return exit_code
    except ImportError:
        print("⚠️ pytest not found in current Python environment. Falling back to unittest runner.")
        import unittest
        loader = unittest.TestLoader()
        suite = loader.discover(os.path.join(PROJECT_ROOT, 'tests'))
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run())
