import logging
from pathlib import Path

from minification_station.logging.decorators import log_exceptions, log_function_call


class FileProcessor:
    def __init__(self, output_filepath: Path) -> None:
        self.output_file = output_filepath

    @log_exceptions
    # @log_function_call
    def process_file(self, file_path: str) -> None:
        with self.output_file.open("a") as outfile:
            with open(file_path) as infile:
                content = infile.read().replace("\n", "\\n")
                outfile.write(content)
                outfile.write("\n")
            logging.debug(f"Processed file: {file_path}")

    @log_exceptions
    # @log_function_call
    def process_files(self, file_paths: list[str]) -> None:
        # Clear the output file before processing multiple files
        self.output_file.write_text("")  # Clear the output file
        for file_path in file_paths:
            self.process_file(file_path)
