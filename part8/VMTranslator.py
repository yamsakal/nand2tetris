import os
import sys
from os import listdir
from pathlib import Path

from code_writer import CodeWriter
from parser import Parser, CommandTypes


def push_pop(parser, code_writer):
    return code_writer.push_pop_to_asm(parser.action(), parser.arg1(), parser.arg2())


PARSING_MAPPING = {
    CommandTypes.C_ARITHMETIC: lambda parser, code_writer: code_writer.arithmetic_to_asm(
        parser.action()
    ),
    CommandTypes.C_PUSH: push_pop,
    CommandTypes.C_POP: push_pop,
    CommandTypes.C_GOTO: lambda parser, code_writer: code_writer.goto_to_asm(
        parser.arg1()
    ),
    CommandTypes.C_IF: lambda parser, code_writer: code_writer.if_to_asm(parser.arg1()),
    CommandTypes.C_LABEL: lambda parser, code_writer: code_writer.lable_to_asm(
        parser.arg1()
    ),
    CommandTypes.C_CALL: lambda parser, code_writer: code_writer.call_to_asm(
        parser.arg1(), parser.arg2()
    ),
    CommandTypes.C_FUNCTION: lambda parser, code_writer: code_writer.function_to_asm(
        parser.arg1(), parser.arg2()
    ),
    CommandTypes.C_RETURN: lambda parser, code_writer: code_writer.return_to_asm(),
}


class UnsupportedCommandTypeError(Exception):
    pass


def is_multi_file(path: str) -> bool:
    if Path(path).is_dir():
        return True
    elif path.endswith(".vm"):
        return False
    raise Exception()  # TODO custom


def output_file_name(input_path: str):
    return (
        os.path.join(input_path, Path(input_path).name) + ".asm"
        if is_multi_file(input_path)
        else input_path.split(".")[0] + ".asm"
    )


def parse(path: str, code_writer: CodeWriter):

    # Updating the vm_file_name to the current vm file name
    code_writer.set_vm_file_name(path)

    # Creates a new parser
    parser = Parser.create(path)

    # Iterating through the file and converting each line from .vm to .asm format
    while parser.has_more_commands():
        parser.advance()
        if parser.current_command == "":
            continue
        command_type = parser.command_type()

        # Calls the writer function with parsed arguments
        if command_type not in PARSING_MAPPING:
            raise UnsupportedCommandTypeError()
        asm_command = PARSING_MAPPING[command_type](parser, code_writer)

        # Writes the VM commands as comments for comfort
        code_writer.write_list_as_asm([rf"// {parser.current_command}"])
        code_writer.write_list_as_asm(asm_command)


def main():
    # Initialize the parser with the input file as argument
    path = sys.argv[1]

    # Initialize the code_writer
    code_writer = CodeWriter.create(output_file_name(path))

    if is_multi_file(path):
        code_writer.write_list_as_asm(code_writer.init_to_asm())
        for f in listdir(path):
            if f.endswith(".vm"):
                parse(os.path.join(path, f), code_writer)
    else:
        parse(path, code_writer)

    # Writes the EXIT loop at the end
    code_writer.write_list_as_asm(code_writer.exit_to_asm())

    # Closing the output file
    code_writer.close()


if __name__ == "__main__":
    main()
