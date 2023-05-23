import os
import sys
from os import listdir
from pathlib import Path

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


def is_multi_file(path: str) -> bool:
    """
    Checks if a file is a single jack file / directory that might contains multiple jack files.
    """
    if Path(path).is_dir():
        return True
    elif path.endswith(".jack"):
        return False
    raise UnsupportedFilePath()


def tokenize_and_compile(file_name: str) -> None:
    """
    Tokenizing and compiling a single jack file.
    """
    with open(file_name, "r") as jack_file:
        tokenizer = JackTokenizer(jack_file, "")
        tokenized_data = tokenizer.tokenize_file()
    tokenized_file_name = file_name.split(".")[0] + "T" + ".xml"
    with open(tokenized_file_name, "w") as tokenized_file:
        tokenized_file.write("\r\n".join(tokenized_data))

    with open(tokenized_file_name, "r") as tokenized_file:
        compiled_file_name = file_name.split(".")[0] + ".xml"
        with open(compiled_file_name, "w") as compiled_output_file:

            compilation_engine = CompilationEngine(tokenized_file, compiled_output_file)
            compilation_engine.compile_file()


def main():
    """
    Initialize the parser with the input file as argument
    """
    path = sys.argv[1]

    if is_multi_file(path):
        for f in listdir(path):
            if f.endswith(".jack"):
                tokenize_and_compile(os.path.join(path, f))
    else:
        tokenize_and_compile(path)


class UnsupportedFilePath(Exception):
    pass


if __name__ == "__main__":
    main()
