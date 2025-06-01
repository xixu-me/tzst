#!/usr/bin/env python3
"""Test script to verify the main CLI fixes."""

from src.tzst.cli import main


def test_help():
    """Test that --help works and returns exit code 0."""
    result = main(["--help"])
    print(f"Help test: {'PASS' if result == 0 else 'FAIL'} (exit code: {result})")
    return result == 0


def test_invalid_compression_level():
    """Test that invalid compression level returns exit code 1."""
    result = main(["a", "test.tzst", "-l", "25", "file.txt"])
    print(
        f"Invalid compression level test: {'PASS' if result == 1 else 'FAIL'} (exit code: {result})"
    )
    return result == 1


def test_invalid_filter():
    """Test that invalid filter returns exit code 1."""
    result = main(["x", "test.tzst", "--filter", "invalid"])
    print(
        f"Invalid filter test: {'PASS' if result == 1 else 'FAIL'} (exit code: {result})"
    )
    return result == 1


def test_non_integer_compression_level():
    """Test that non-integer compression level returns exit code 1."""
    result = main(["a", "test.tzst", "-l", "abc", "file.txt"])
    print(
        f"Non-integer compression level test: {'PASS' if result == 1 else 'FAIL'} (exit code: {result})"
    )
    return result == 1


if __name__ == "__main__":
    print("Testing main CLI fixes:")
    print("=" * 50)

    tests = [
        test_help,
        test_invalid_compression_level,
        test_invalid_filter,
        test_non_integer_compression_level,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} failed with exception: {e}")

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All main fixes are working correctly!")
    else:
        print("❌ Some fixes still need attention")
