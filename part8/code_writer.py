import itertools
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

    def __init__(self, output_file, path: str, vm_file_name: str):
        """
        initialise a new codeWriter class
        """
        self.output_file = output_file
        self.vm_file_name = vm_file_name
        self.path = path
        self.loop_counter = 0

    @classmethod
    def create(cls, path: str):
        """
        create new output file
        """
        output_file = open(path, "w")
        return cls(output_file=output_file, path=path, vm_file_name="")

    def set_vm_file_name(self, vm_file_path: str):
        self.vm_file_name = os.path.basename(vm_file_path).split(".")[0]

    def arithmetic_to_asm(self, command: str):
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
        return arithmetic_methods_mapping[command]()

    def push_pop_to_asm(self, command: str, segment: str, arg2: int):
        push_pop_method_mapping = {"push": self.push_to_asm, "pop": self.pop_to_asm}
        return push_pop_method_mapping[command](segment, arg2)

    def write_list_as_asm(self, commands_list: List[str]):
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
                f"@{self.vm_file_name}.{arg2}",
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
            return ["@SP", "M=M-1", "A=M", "D=M", f"@{self.vm_file_name}.{arg2}", "M=D"]
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

    def lt_to_asm(self) -> List[str]:
        return self.compare_to_asm("lt")

    def gt_to_asm(self) -> List[str]:
        return self.compare_to_asm("gt")

    def eq_to_asm(self) -> List[str]:
        return self.compare_to_asm("eq")

    def init_to_asm(self) -> List[str]:
        """
        bootstrap code
        """
        return ["@256", "D=A", "@SP", "M=D"] + self.call_to_asm("Sys.init", 0)

    def lable_to_asm(self, label: str):
        """
        return label
        """
        return [f"({label})"]

    def goto_to_asm(self, label: str):
        """
        write the 'goto' command
        """
        return [f"@{label}", "0;JMP"]

    def if_to_asm(self, label: str) -> List[str]:
        """
        write the 'if' command
        """
        return ["@SP", "M=M-1", "A=M", "D=M", f"@{label}", "D;JNE"]

    def function_to_asm(self, function_name: str, num_args: int) -> List[str]:
        """
        write the 'function' command
        """
        return [f"({function_name})"] + list(itertools.chain.from_iterable([["@SP", "A=M", "M=0", "@SP", "M=M+1"] for _ in range(1, num_args + 1)]))


    def _push_addr_to_asm(self, label: str):
        """
        push address of given label
        """
        return [
            f"@{label}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def _push_value_to_asm(self, label: str):
        """
        push address of given label
        """
        return [
            f"@{label}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        ]

    def call_to_asm(self, function_name: str, num_args: int) -> List[str]:
        """
        write the 'call function' to assembly code
        """
        self.loop_counter += 1
        ret_addr_label = f"{function_name}{self.loop_counter}"

        return (
            self._push_addr_to_asm(ret_addr_label)
            + self._push_value_to_asm("LCL")
            + self._push_value_to_asm("ARG")
            + self._push_value_to_asm("THIS")
            + self._push_value_to_asm("THAT")
            + ["@SP", "D=M", f"@{5 + num_args}", "D=D-A", "@ARG", "M=D"]
            + ["@SP", "D=M", "@LCL", "M=D"]
            + self.goto_to_asm(function_name)
            + self.lable_to_asm(f"{ret_addr_label}")
        )

    def return_to_asm(self) -> List[str]:
        """
        write the 'return' command to assembly code
        """
        return [
            "@LCL",
            "D=M",
            "@R9",  # endFrame
            "M=D",
            "@5",
            "A=D-A",
            "D=M",
            "@R10",
            "M=D",  # retAddr
            "@SP",
            "M=M-1",
            "A=M",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",  # ARG = pop()
            "@ARG",
            "D=M+1",
            "@SP",
            "M=D",  # SP = ARG + 1
            # Restore THAT
            "@R9",
            "M=M-1",
            "A=M",
            "D=M",
            "@THAT",
            "M=D",
            # Restore THIS
            "@R9",
            "M=M-1",
            "A=M",
            "D=M",
            "@THIS",
            "M=D",
            # Restore ARG
            "@R9",
            "M=M-1",
            "A=M",
            "D=M",
            "@ARG",
            "M=D",
            # Restore LCL
            "@R9",
            "M=M-1",
            "A=M",
            "D=M",
            "@LCL",
            "M=D",
            f"@R10",
            "A=M",
            "0;JMP"
        ]

    def exit_to_asm(self):
        return ["(EXIT)", "@EXIT", "0;JMP"]
