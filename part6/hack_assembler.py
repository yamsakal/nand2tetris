from code import Code
from parser import Parser, InstructionTypes, FileEndException
from symbol_table import SymbolTable


class HackAssembler:
    # Keeps track of the next available symbol address
    NEXT_SYMBOL_ADDRESS = 16

    def __init__(self, parser: Parser, symbol_table: SymbolTable, code: Code):
        self.parser = parser
        self.symbol_table = symbol_table
        self.code = code

    @classmethod
    def create(cls, file_path: str):
        return cls(
            parser=Parser.open(file_path), symbol_table=SymbolTable(), code=Code()
        )

    def first_pass(self):
        """
        Iterates through the file for the first time and only writes labels and symbols to the symbol table.
        """
        line_index = 0
        while self.parser.has_more_lines():

            try:
                self.parser.advance()
            except FileEndException:
                break
            instruction_type = self.parser.instruction_type()
            if instruction_type == InstructionTypes.L:
                symbol = self.parser.symbol()
                if not self.symbol_table.contains(symbol):
                    self.symbol_table.add_entry(symbol, line_index)
            else:
                line_index += 1

    def second_pass(self, output_file):
        """
        Iterating through the file again and writing the commands translated to "0/1" binary language.
        """
        # starting from the beginning of the file again
        self.parser.asm_file.seek(0)

        instruction_to_handler = {
            InstructionTypes.A: self.handle_a,
            InstructionTypes.L: self.handle_l,
            InstructionTypes.C: self.handle_c,
        }
        while self.parser.has_more_lines():

            try:
                self.parser.advance()
            except FileEndException:
                break
            instruction_type = self.parser.instruction_type()

            instruction_to_handler[instruction_type](output_file)

    @staticmethod
    def int_to_binary_16(num: int) -> str:
        """
        Converts a integer to a binary 16 bit with left 0 padding.
        """
        return bin(num).replace("0b", "").zfill(16)

    def handle_a(self, output_file):
        """
        Writes A command types to the output file - Using the symbol table address.
        """
        symbol = self.parser.symbol()

        # @1 for example
        if symbol.isnumeric():
            output = symbol
        else:
            # @R0 for example
            if not self.symbol_table.contains(symbol):
                self.symbol_table.add_entry(symbol, self.NEXT_SYMBOL_ADDRESS)
                self.NEXT_SYMBOL_ADDRESS += 1
            output = self.symbol_table.get_address(symbol)

        output_file.write(self.int_to_binary_16(int(output)))

    def handle_l(self, output_file):
        pass

    def handle_c(self, output_file):
        """
        Writes C command types to output file - By translating each part of them to it's binary representation.
        """
        output_file.write(
            f"{111}{self.code.comp(self.parser.comp())}{self.code.dest(self.parser.dest())}{self.code.jump(self.parser.jump())}"
        )
