import argparse
from collections import Counter
from functools import lru_cache

ERROR_MSG_FILE_NOT_FOUND = "Error: The file '{}' does not exist"
ERROR_MSG_PERMISSION_DENIED = "Error: Permission denied for '{}'"


@lru_cache(maxsize=None)
def count_unique_characters(input_string: str) -> int:
    """
    Count the number of unique characters in the given string.

    Typical usage examples:
    >>> count_unique_characters("hello")
    3
    >>> count_unique_characters("abcdef")
    6
    >>> count_unique_characters("aabbcc")
    0
    >>> count_unique_characters("")
    0

    Atypical behavior (errors):
    If a non-string type is passed:
    >>> count_unique_characters(12345)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    TypeError: Expected a string, but got int
    """

    # Validate the input
    if not isinstance(input_string, str):
        raise TypeError(f"Expected a string, but got {type(input_string).__name__}")

    char_counter = Counter(input_string)
    unique_count = sum(1 for _, count in char_counter.items() if count == 1)
    return unique_count


def read_file(file_path: str) -> str:
    """
    Read the content of the file.



    Atypical behavior (errors):
    If the file does not exist:
    >>> read_file('non_existent_file.txt')
    Error: The file 'non_existent_file.txt' does not exist
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(ERROR_MSG_FILE_NOT_FOUND.format(file_path))
    except PermissionError:
        print(ERROR_MSG_PERMISSION_DENIED.format(file_path))
        return None


def process_arguments(args) -> None:
    """
    Process input arguments and execute the appropriate action.

    Typical usage examples:
    >>> class Args: pass
    >>> args = Args()
    >>> args.file = None
    >>> args.string = 'hello'
    >>> process_arguments(args)
    The string 'hello' has 3 unique characters.

    Atypical behavior (errors):
    If no arguments are provided:
    >>> args = Args()
    >>> args.file = None
    >>> args.string = None
    >>> process_arguments(args)
    Error: Please provide either --string or --file as input.
    """
    if args.file:
        content = read_file(args.file)
        if content:
            unique_count = count_unique_characters(content)
            print(f"File '{args.file}' has {unique_count} unique characters.")
    elif args.string:
        unique_count = count_unique_characters(args.string)
        print(f"The string '{args.string}' has {unique_count} unique characters.")
    else:
        print("Error: Please provide either --string or --file as input.")


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Count unique characters in a string or a file.")
    parser.add_argument('--string', type=str, help="Input string to process")
    parser.add_argument('--file', type=str, help="Path to the file to process")
    parser.add_argument('--test', action='store_true', help="Run doctests and exit")

    args = parser.parse_args()


# Run doctests if --test is provided
    if args.test:
        import doctest
        doctest.testmod()
        return

    # Otherwise, process the input arguments
    process_arguments(args)


if __name__ == "__main__":
    main()

