#!/usr/bin/env python3
"""
Test runner script for TT Scraper server.
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage."""
    print("Running TT Scraper server tests...")
    print("=" * 50)

    # Change to server directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        '--verbose',
        '--tb=short',
        '--cov=.',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--cov-fail-under=100',
        'tests/'
    ]

    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ All tests passed with 100% coverage!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
