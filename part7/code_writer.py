import os
from typing import List


class CodeWriter:
    """
    handles the parsing of single .vm file
    """

    SEGMENT_TO_AMS = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
    }
    loop_counter = 0
    OPERATOR_DICT = {"eq": "JEQ", "lt": "JLT", "gt": "JGT"}

    def __init__(self, output_file, path: str):
        """
        initialise a new codeWriter class
        """
        self.output_file = output_file
        self.path = path
        self.loop_counter = 0

    @classmethod
    def create(cls, path: str):
        """
        create new output file
        """
        output_file = open(path, "w")
        return cls(output_file=output_file, path=path)

    @property
    def file_name(self):
        """
        get the file name
        """
        return os.path.basename(self.path).split(".")[0]

    def write_arithmetic(self, command: str):
        """
        add arithmetics commands into output file
        """
        arithmetic_methods_mapping = {
            "add": self.add_to_asm,
            "sub": self.sub_to_asm,
            "neg": self.neg_to_asm,
            "or": self.or_to_asm,
            "and": self.and_to_asm,
            "not": self.not_to_asm,
            "lt": self.lt_to_asm,
            "gt": self.gt_to_asm,
            "eq": self.eq_to_asm,
        }
        asm_output = arithmetic_methods_mapping[command]()
        self._write_list_as_asm(asm_output)

    def write_push_pop(self, command: str, segment: str, arg2: int):
        push_pop_method_mapping = {"push": self.push_to_asm, "pop": self.pop_to_asm}
        asm_output = push_pop_method_mapping[command](segment, arg2)
        self._write_list_as_asm(asm_output)

    def _write_list_as_asm(self, commands_list: List[str]):
        self.output_file.write("\n".join(commands_list) + "\n")

    def close(self):
        """
        closing the output file
        """
        self.output_file.close()

    def push_to_asm(self, segment: str, arg2: int) -> List[str]:
        """
        add push commands into output file
        """
        if segment == "constant":
            return [f"@{arg2}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif segment == "static":
            return [
                f"@{self.file_name}.{arg2}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
        elif segment == "temp":
            return [f"@{arg2 + 5}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        elif segment == "pointer":
            return [
                f"@{'THIS' if arg2 == 0 else 'THAT'}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]
        else:
            seg_asm = self.SEGMENT_TO_AMS[segment]
            return [
                f"@{arg2}",
                "D=A",
                f"@{seg_asm}",
                "D=D+M",
                "A=D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]

    def pop_to_asm(self, segment: str, arg2: int) -> List[str]:
        """
        add pop commands into output file
        """
        if segment == "static":
            return ["@SP", "M=M-1", "A=M", "D=M", f"@{self.file_name}.{arg2}", "M=D"]
        elif segment == "temp":
            return [
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                f"@{arg2 + 5}",
                "M=D",
            ]
        elif segment == "pointer":
            return [
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                f"@{'THIS' if arg2 == 0 else 'THAT'}",
                "M=D",
            ]
        else:
            seg_asm = self.SEGMENT_TO_AMS[segment]
            return [
                f"@{arg2}",
                "D=A",
                f"@{seg_asm}",
                "A=M",
                "D=A+D",
                "@R10",
                "M=D",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@R10",
                "A=M",
                "M=D",
            ]

    @staticmethod
    def add_to_asm() -> List[str]:
        """
        add 'add' commands into output file
        """
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "M=M+D",
            "@SP",
            "M=M+1",
        ]

    @staticmethod
    def sub_to_asm() -> List[str]:
        """
        add 'sub' commands into output file
        """
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "M=M-D",
            "@SP",
            "M=M+1",
        ]

    @staticmethod
    def neg_to_asm() -> List[str]:
        """
        add 'negate' commands into output file
        """
        return ["@SP", "M=M-1", "A=M", "D=M", "M=M-D", "M=M-D", "@SP", "M=M+1"]

    @staticmethod
    def or_to_asm() -> List[str]:
        """
        add 'or' operator commands into output file
        """
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "M=M|D",
            "@SP",
            "M=M+1",
        ]

    @staticmethod
    def and_to_asm() -> List[str]:
        """
        add 'and' operator commands into output file
        """
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "M=M&D",
            "@SP",
            "M=M+1",
        ]

    @staticmethod
    def not_to_asm() -> List[str]:
        """
        add 'not' operator commands into output file
        """
        return ["@SP", "M=M-1", "A=M", "M=!M", "@SP", "M=M+1"]

    def compare_to_asm(self, command: str) -> List[str]:
        """
        add 'compare' operator commands into output file
        """
        self.loop_counter += 1
        return [
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@SP",
            "M=M-1",
            "A=M",
            "D=M-D",
            f"@TRUE{self.loop_counter}",
            f"D;{self.OPERATOR_DICT[command]}",
            f"(FALSE{self.loop_counter})",
            "@SP",
            "A=M",
            "M=0",
            "@SP",
            "M=M+1",
            f"@CONT{self.loop_counter}",
            "0;JMP",
            f"(TRUE{self.loop_counter})",
            "@SP",
            "A=M",
            "M=-1",
            "@SP",
            "M=M+1",
            f"@CONT{self.loop_counter}",
            "0;JMP",
            f"(CONT{self.loop_counter})",
        ]

    def lt_to_asm(self):
        return self.compare_to_asm("lt")

    def gt_to_asm(self):
        return self.compare_to_asm("gt")

    def eq_to_asm(self):
        return self.compare_to_asm("eq")
