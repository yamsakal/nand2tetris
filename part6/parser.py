from enum import Enum


class InstructionTypes(Enum):
    A = 1  # Symbol
    L = 2  # Label
    C = 3  # Normal


class Parser:
    def __init__(self, asm_file):
        """
        parser constructor
        """
        self.the_current_instruction = None
        self.asm_file = asm_file

    @classmethod
    def open(cls, asm_file_path):
        """
        Creates a new Parser instance by opening `asm_file_path`
        :param asm_file_path: Path of the asm_file
        """
        asm_file_path = open(asm_file_path, "r")
        return cls(asm_file_path)

    def has_more_lines(self) -> bool:
        """
        check if there are more lines to read in the file
        :return: true / false
        """
        cur_pos = self.asm_file.tell()
        has_more_lines = bool(self.asm_file.readline())
        self.asm_file.seek(cur_pos)
        return has_more_lines

    def advance(self):
        """
        reads the next command line, ignoring the comments and the empty lines
        :return:
        """
        while self.has_more_lines():

            next_line = self.asm_file.readline()

            if next_line.find("//") != -1:
                next_line = next_line.split(r"//")[0]
            next_line = next_line.strip()

            if next_line != "":
                self.the_current_instruction = next_line
                return
        raise FileEndException()

    def instruction_type(self) -> InstructionTypes:
        """
        :return: the type of the Instruction (A/L/C)
        """
        prefix_instruction_type = {"(": InstructionTypes.L, "@": InstructionTypes.A}
        return prefix_instruction_type.get(
            self.the_current_instruction[0], InstructionTypes.C
        )

    def symbol(self) -> str:
        """
        :return: the symbol of the current instruction. assuming the instruction type is A or L
        """
        if self.the_current_instruction[0] == "(":
            return self.the_current_instruction[
                1 : len(self.the_current_instruction) - 1
            ]
        else:
            return self.the_current_instruction[1:]

    def dest(self) -> str:
        """
        :return: the destination part of thr current instruction. assuming the instruction type is C
        """
        if "=" in self.the_current_instruction:
            return self.the_current_instruction.split("=")[0]
        else:
            return "null"

    def comp(self) -> str:
        """
        :return: the comp part of thr current instruction. assuming the instruction type is C
        """
        if "=" in self.the_current_instruction:
            s = self.the_current_instruction.split("=")[1]

            if ";" in self.the_current_instruction:
                return s.split(";")[0]
            else:
                return s
        else:
            return self.the_current_instruction.split(";")[0]

    def jump(self) -> str:
        """
        :return: the jump part of thr current instruction. assuming the instruction type is C
        """
        if ";" in self.the_current_instruction:
            return self.the_current_instruction.split(";")[1]
        else:
            return "null"


class FileEndException(Exception):
    pass
