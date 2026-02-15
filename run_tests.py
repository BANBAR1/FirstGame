"""
Test runner for Word Guessing Game
Run this file to execute all tests
"""

import subprocess
import sys


def main():
    """Run all tests using pytest"""
    print("=" * 60)
    print("Running Word Guessing Game Tests")
    print("=" * 60)
    print()

    # Run pytest with verbose output
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=sys.path[0] if sys.path[0] else "."
    )

    print()
    print("=" * 60)
    if result.returncode == 0:
        print("All tests passed!")
    else:
        print(f"Some tests failed (exit code: {result.returncode})")
    print("=" * 60)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
