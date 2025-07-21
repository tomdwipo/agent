#!/usr/bin/env python3
"""
Test runner for Audio Transcription Tool with PRD Generation

This script runs all tests for the application, including PRD-related functionality.
Provides detailed test results and coverage information.
"""

import sys
import os
import unittest
import time
from datetime import datetime

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def discover_and_run_tests():
    """Discover and run all tests in the tests directory"""
    print("🔍 Discovering tests...")
    
    # Discover tests in the tests directory
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    if not os.path.exists(test_dir):
        print(f"❌ Test directory not found: {test_dir}")
        return False
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover all tests
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Count total tests
    total_tests = suite.countTestCases()
    print(f"📊 Found {total_tests} tests")
    
    if total_tests == 0:
        print("⚠️  No tests found!")
        return False
    
    return suite


def run_specific_test_modules():
    """Run specific PRD test modules"""
    print("🎯 Running PRD-specific tests...")
    
    test_modules = [
        'tests.test_prd_services',
        'tests.test_prd_ui'
    ]
    
    suite = unittest.TestSuite()
    
    for module_name in test_modules:
        try:
            module = __import__(module_name, fromlist=[''])
            module_suite = unittest.TestLoader().loadTestsFromModule(module)
            suite.addTest(module_suite)
            print(f"✅ Loaded tests from {module_name}")
        except ImportError as e:
            print(f"⚠️  Could not import {module_name}: {e}")
        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")
    
    return suite


def run_test_suite(suite, verbose=True):
    """Run the test suite and return results"""
    if suite.countTestCases() == 0:
        print("❌ No tests to run!")
        return False
    
    print(f"\n🚀 Running {suite.countTestCases()} tests...")
    print("=" * 70)
    
    # Configure test runner
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        stream=sys.stdout,
        buffer=True
    )
    
    # Record start time
    start_time = time.time()
    
    # Run tests
    result = runner.run(suite)
    
    # Record end time
    end_time = time.time()
    duration = end_time - start_time
    
    # Print results summary
    print("=" * 70)
    print(f"⏱️  Test execution time: {duration:.2f} seconds")
    print(f"🧪 Tests run: {result.testsRun}")
    print(f"✅ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    
    if result.failures:
        print(f"❌ Failures: {len(result.failures)}")
        
    if result.errors:
        print(f"💥 Errors: {len(result.errors)}")
    
    if result.skipped:
        print(f"⏭️  Skipped: {len(result.skipped)}")
    
    # Return success status
    return result.wasSuccessful()


def print_test_summary(success, start_time):
    """Print final test summary"""
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration:.2f} seconds")
    
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✨ PRD Generation feature is ready for use.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("🔧 Please fix failing tests before using PRD feature.")
    
    print("=" * 70)


def main():
    """Main test runner function"""
    print("🧪 Audio Transcription Tool - Test Suite")
    print("Including PRD Generation Feature Tests")
    print("=" * 70)
    
    start_time = datetime.now()
    
    # Parse command line arguments
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    prd_only = '--prd-only' in sys.argv
    
    try:
        # Choose test discovery method
        if prd_only:
            print("🎯 Running PRD-specific tests only...")
            suite = run_specific_test_modules()
        else:
            print("🔍 Running all discovered tests...")
            suite = discover_and_run_tests()
        
        # Run tests if suite was created successfully
        if suite and isinstance(suite, unittest.TestSuite):
            success = run_test_suite(suite, verbose=verbose)
        else:
            print("❌ Failed to create test suite!")
            success = False
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        success = False
        
    except Exception as e:
        print(f"\n❌ Unexpected error during test execution: {e}")
        success = False
    
    # Print final summary
    print_test_summary(success, start_time)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


def print_usage():
    """Print usage information"""
    print("""
Usage: uv run run_tests.py [options]

Options:
  --verbose, -v     Run tests with verbose output
  --prd-only        Run only PRD-related tests
  --help, -h        Show this help message

Examples:
  uv run run_tests.py                 # Run all tests
  uv run run_tests.py --verbose       # Run all tests with verbose output
  uv run run_tests.py --prd-only      # Run only PRD tests
  uv run run_tests.py --prd-only -v   # Run only PRD tests with verbose output
""")


if __name__ == '__main__':
    # Check for help argument
    if '--help' in sys.argv or '-h' in sys.argv:
        print_usage()
        sys.exit(0)
    
    # Run main test function
    main()