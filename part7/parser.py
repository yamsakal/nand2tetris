from enum import Enum
import re


class CommandTypes(Enum):
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Parser:
    """
    Responsible for parsing .vm file into .asm format - line by line.
    """

    def __init__(self, input_file, current_command: str):
        """
        Initializes a new Parser instance
        """
        self.input_file = input_file
        self.current_command = current_command

    @classmethod
    def create(cls, path: str):
        """
        Creates a Parser instance with an opened file.
        """
        input_file = open(path, "r")
        return cls(input_file=input_file, current_command="")

    @property
    def command_as_list(self):
        return re.split(r"\s+", self.current_command)

    def has_more_commands(self) -> bool:
        """
        Checks if we already read all commands
        """
        cur_pos = self.input_file.tell()
        has_more_commands = bool(self.input_file.readline())
        self.input_file.seek(cur_pos)
        return has_more_commands

    def advance(self) -> None:
        """
        Forwards current_command to the next line of the file.
        """
        self.current_command = self.input_file.readline().split("//")[0]
        self.current_command = self.current_command.strip()
        self.current_command = self.current_command.replace("\n", "")

    def command_type(self) -> CommandTypes:
        """
        Extract command_type from the command
        """
        dict_command_types = {
            "push": CommandTypes.C_PUSH,
            "pop": CommandTypes.C_POP,
            "add": CommandTypes.C_ARITHMETIC,
            "sub": CommandTypes.C_ARITHMETIC,
            "neg": CommandTypes.C_ARITHMETIC,
            "or": CommandTypes.C_ARITHMETIC,
            "and": CommandTypes.C_ARITHMETIC,
            "not": CommandTypes.C_ARITHMETIC,
            "lt": CommandTypes.C_ARITHMETIC,
            "gt": CommandTypes.C_ARITHMETIC,
            "eq": CommandTypes.C_ARITHMETIC,
        }
        return dict_command_types[self.command_as_list[0]]

    def arg1(self) -> str:
        """
        Extracts the first arg from the command
        """
        command_list = self.current_command.split()
        if len(command_list) == 1:
            return command_list[0]
        return command_list[1]

    def arg2(self) -> int:
        """
        Extract the second argument from the command
        """
        return int(self.command_as_list[-1])

    def action(self) -> str:
        """
        Extracts the action from the command
        """
        return self.command_as_list[0]
