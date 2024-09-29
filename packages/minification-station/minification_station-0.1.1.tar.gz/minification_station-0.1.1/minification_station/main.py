import logging
import os
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING

from tqdm import tqdm

from minification_station.config.args import get_parsed_args
from minification_station.config.enviornment_setup import (
    OUTPUT_PATH,
    current_date,
    initialize_application,
    validate_directory,
)
from minification_station.processing.file_processor import FileProcessor
from minification_station.traversal.directory_traversal import DirectoryTraversal

if TYPE_CHECKING:
    from argparse import Namespace


def log_progress(index: int, total: int, message: str) -> None:
    """Log progress with index and total count."""
    logging.info(f"[{index}/{total}] {message}")


def main() -> None:
    args: Namespace = get_parsed_args()
    initialize_application()

    directory = args.directory
    validate_directory(directory)
    output_file: str = current_date + "-" +  os.path.basename(directory) + ".txt"
    output_path: Path = OUTPUT_PATH / output_file

    logging.info(
        f"Starting the script with directory: {directory} and output file: {output_file}",
    )
    sleep(2)

    try:
        traversal = DirectoryTraversal(directory=directory)
        file_paths = traversal.get_files()
        total_files = len(file_paths)
        logging.info(f"Total number of files to process: {total_files}")

        processor = FileProcessor(output_filepath=output_path)
        for file_path in tqdm(file_paths, desc="Processing files", unit="file"):
            processor.process_file(file_path)

        logging.info(f"Combined file written to {output_path}")
    except Exception:
        logging.exception("An error occurred")


if __name__ == "__main__":
    main()
