class Code:
    DEST = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "ADM": "111",
    }
    JUMP = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }
    COMP = {
        "0": ("101010", 0),
        "1": ("111111", 0),
        "-1": ("111000", 0),
        "D": ("001100", 0),
        "A": ("110000", 0),
        "!D": ("001101", 0),
        "!A": ("110001", 0),
        "-D": ("001111", 0),
        "-A": ("110011", 0),
        "D+1": ("011111", 0),
        "A+1": ("110111", 0),
        "D-1": ("001110", 0),
        "A-1": ("110010", 0),
        "D+A": ("000010", 0),
        "D-A": ("010011", 0),
        "A-D": ("000111", 0),
        "D&A": ("000000", 0),
        "D|A": ("010101", 0),
        "M": ("110000", 1),
        "!M": ("110001", 1),
        "-M": ("110011", 1),
        "M+1": ("110111", 1),
        "M-1": ("110010", 1),
        "D+M": ("000010", 1),
        "D-M": ("010011", 1),
        "M-D": ("000111", 1),
        "D&M": ("000000", 1),
        "D|M": ("010101", 1),
    }

    def dest(self, unparsed_instruction: str):
        """
        Converts dest command to its binary opcode
        """
        return self.DEST[unparsed_instruction]

    def comp(self, unparsed_instruction: str):
        """
        Converts comp command to its binary opcode
        """
        instruction = self.COMP[unparsed_instruction]
        return str(instruction[1]) + instruction[0]

    def jump(self, unparsed_instruction: str):
        """
        Converts jump command to its binary opcode
        """
        return self.JUMP[unparsed_instruction]
