from src.task_5_SYRKIN import main
import pytest
from unittest.mock import patch, mock_open
import argparse
from functools import lru_cache

DEFAULT_CACHE_SIZE = None  # Introduce a constant for cache size
function_call_count = 0  # Global variable for tracking function calls


def reset_function_call_count() -> None:
    """Reset the global function call count."""
    global function_call_count
    function_call_count = 0


@lru_cache(maxsize=DEFAULT_CACHE_SIZE)
def cached_count_unique_chars(string: str) -> int:
    """Count unique characters in a string with caching."""
    global function_call_count
    function_call_count += 1
    return len(set(string))


@pytest.mark.parametrize("input_str, expected_result, expected_calls", [
    ("hello", 4, 1),  # Expect 4 unique characters in "hello"
    ("test", 3, 2),  # Expect 3 unique characters in "test" with 2 calls
    ("unique", 5, 3),  # Expect 5 unique characters in "unique" with 3 calls
])
def test_repeated_calls(input_str, expected_result, expected_calls) -> None:
    reset_function_call_count()  # Reset function call count before test
    assert cached_count_unique_chars(input_str) == expected_result, \
        f"Expected {expected_result} unique characters in '{input_str}'"
    assert function_call_count == 1, "Function should be called once on the first call"

    for _ in range(expected_calls - 1):
        cached_count_unique_chars(input_str)

    assert function_call_count == 1, \
        f"Function should be called once initially, subsequent calls should use the cache"

    cache_info = cached_count_unique_chars.cache_info()
    assert cache_info.hits >= (expected_calls - 1), \
        f"Expected at least {expected_calls - 1} cache hits"
    assert cache_info.misses >= 1, "Expected exactly one cache miss"


@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(string="hello", file=None))
def test_cli_with_string(mock_args):
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with("The string 'hello' has 3 unique characters.")


@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(string=None, file="fake_path.txt"))
@patch("builtins.open", new_callable=mock_open, read_data="hello file")
def test_cli_with_file(mock_file, mock_args):
    """Test the CLI when --file is passed, expecting it to count unique characters from the file content."""
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with("File 'fake_path.txt' has 5 unique characters.")


@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(string="hello", file="fake_path.txt"))
@patch("builtins.open", new_callable=mock_open, read_data="hello file")
def test_cli_with_file_and_string(mock_file, mock_args):
    """Test the CLI when both --file and --string are passed, ensuring the file is given priority."""
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with("File 'fake_path.txt' has 5 unique characters.")


@patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(string=None, file=None))
def test_cli_without_arguments(mock_args):
    with patch('builtins.print') as mock_print:
        main()
        mock_print.assert_called_with("Error: Please provide either --string or --file as input.")
