import sys

from parser import Parser, CommandTypes
from code_writer import CodeWriter


class UnsupportedCommandTypeError(Exception):
    pass


def main():
    # Initialize the parser with the input file as argument
    path = sys.argv[1]
    parser = Parser.create(path)

    # Initialize the code_writer with the output path .asm
    output_path = path.split(".")[0] + ".asm"
    code_writer = CodeWriter.create(output_path)

    # Iterating through the file and converting each line from .vm to .asm format
    while parser.has_more_commands():
        parser.advance()
        if parser.current_command == "":
            continue
        command_type = parser.command_type()
        if command_type == CommandTypes.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.action())

        elif command_type in [CommandTypes.C_PUSH, CommandTypes.C_POP]:
            code_writer.write_push_pop(parser.action(), parser.arg1(), parser.arg2())
        else:
            raise UnsupportedCommandTypeError()

    # Closing the output file
    code_writer.close()


if __name__ == "__main__":
    main()
