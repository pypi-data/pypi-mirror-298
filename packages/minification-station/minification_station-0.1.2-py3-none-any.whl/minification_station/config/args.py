import argparse
import sys

DEFAULT_OUTPUT_FILE = "output.txt"


def get_parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process files in a directory and combine them into a single output file.",
    )
    parser.add_argument("-d", "--directory", required=True, help="Directory to traverse")
    # parser.add_argument("-o", "--output", required=True, default=DEFAULT_OUTPUT_FILE, help="Output file path")

    return parser.parse_args()
