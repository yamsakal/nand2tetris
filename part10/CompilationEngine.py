from typing import List
from JackTokenizer import *

op_list = ["+", "-", "=", "&lt;", "&gt;", "/", "*", "|", "&amp;"]


class CompilationEngine:

    statement_list = ["do", "if", "while", "let", "return"]

    def __init__(self, tokenized_file, compiled_output_file):
        self.tokenized_file = tokenized_file
        self.compiled_output_file = compiled_output_file
        self.depth = 0

    def compile_class(self):
        self.read_tokenized_line()  # tokens
        self.write_with_indentation("<class>")
        self.depth += 1
        self.write_with_indentation(self.read_tokenized_line())  # class keyword
        self.write_with_indentation(self.read_tokenized_line())  # class name
        self.write_with_indentation(self.read_tokenized_line())  # {
        command_compilers = {
            "function": self.compile_subroutine_dec,
            "static": self.compile_class_var_dec,
            "do": self.compile_do,
            "field": self.compile_class_var_dec,
            "constructor": self.compile_subroutine_dec,
            "method": self.compile_subroutine_dec,
        }
        while (command := self.peek_command()) != "}":
            command_compilers[command]()

        self.write_with_indentation(self.read_tokenized_line())  # }
        self.depth -= 1
        self.write_with_indentation("</class>")  # </class>
        self.read_tokenized_line()  # tokens
        self.read_tokenized_line()  # empty line

    def peek_command(self):
        """
        Peeks on what is the next command (without moving the file pointer).
        :return: the next command
        """
        last_pos = self.tokenized_file.tell()
        command = self.get_xml_val(self.read_tokenized_line())
        self.tokenized_file.seek(last_pos)
        return command

    def peek_command_twice(self):
        """
        Peeks on what is the next of the next command (without moving the file pointer).
        :return: the next of the next command
        """
        last_pos = self.tokenized_file.tell()
        self.read_tokenized_line()
        command = self.get_xml_val(self.read_tokenized_line())
        self.tokenized_file.seek(last_pos)
        return command

    def compile_class_var_dec(self):
        """
        Compiles a VarDec
        """
        self.write_with_indentation("<classVarDec>")
        self.depth += 1
        while self.peek_command() != ";":
            self.write_with_indentation(self.read_tokenized_line())
        self.write_with_indentation(self.read_tokenized_line())
        self.depth -= 1
        self.write_with_indentation("</classVarDec>")

    def compile_subroutine_dec(self):
        """
        Compiles a SubroutineDec
        """
        self.write_with_indentation("<subroutineDec>")
        self.depth += 1
        self.write_with_indentation(
            self.read_tokenized_line()
        )  # function / method / constructor
        self.write_with_indentation(self.read_tokenized_line())  # type
        self.write_with_indentation(self.read_tokenized_line())  # name
        self.write_with_indentation(self.read_tokenized_line())  # (
        self.compile_parameter_list()  # parameters
        self.write_with_indentation(self.read_tokenized_line())  # )
        self.compile_subroutine_body()
        self.depth -= 1
        self.write_with_indentation("</subroutineDec>")

    def compile_parameter_list(self):
        """
        Compiles a ParameterList
        """
        self.write_with_indentation("<parameterList>")
        self.depth += 1
        while self.peek_command() != ")":
            self.write_with_indentation(
                self.read_tokenized_line()
            )  # <symbol> / <keyword> / </identifier>
        self.depth -= 1
        self.write_with_indentation("</parameterList>")

    def compile_subroutine_body(self):
        """
        Compiles a SubroutineBody
        """
        self.write_with_indentation("<subroutineBody>")
        self.depth += 1
        self.write_with_indentation(self.read_tokenized_line())  # {
        while self.peek_command() == "var":
            self.compile_var_dec()
        self.write_with_indentation("<statements>")
        self.depth += 1
        while self.peek_command() in self.statement_list:
            self.compile_statement()
        self.depth -= 1
        self.write_with_indentation("</statements>")
        self.write_with_indentation(self.read_tokenized_line())  # }
        self.depth -= 1
        self.write_with_indentation("</subroutineBody>")

    def compile_var_dec(self):
        """
        Compiles a VarDev
        """
        self.write_with_indentation("<varDec>")
        self.depth += 1
        while self.peek_command() != ";":
            self.write_with_indentation(self.read_tokenized_line())
        self.write_with_indentation(self.read_tokenized_line())
        self.depth -= 1
        self.write_with_indentation("</varDec>")

    def compile_statement(self):
        """
        Compiles a Statement
        """
        statement_compilers = {
            "let": self.compile_let,
            "do": self.compile_do,
            "return": self.compile_return,
            "if": self.compile_if,
            "while": self.compile_while,
        }
        command = self.peek_command()
        statement_compilers[command]()

    def compile_let(self):
        """
        Compiles a LetStatement
        """
        self.write_with_indentation("<letStatement>")
        self.depth += 1
        while self.peek_command() not in ["=", ";"]:
            if self.peek_command() == "[":
                self.write_with_indentation(self.read_tokenized_line())
                self.compile_expression()
            self.write_with_indentation(self.read_tokenized_line())
        if self.peek_command() == "=":
            self.write_with_indentation(self.read_tokenized_line())  # =
            self.compile_expression()
        self.write_with_indentation(self.read_tokenized_line())  # ;
        self.depth -= 1
        self.write_with_indentation("</letStatement>")

    def compile_if(self):
        """
        Compiles a IfStatement
        """
        self.write_with_indentation("<ifStatement>")
        self.depth += 1
        self.write_with_indentation(self.read_tokenized_line())  # if
        self.write_with_indentation(self.read_tokenized_line())  # (
        self.compile_expression()
        self.write_with_indentation(self.read_tokenized_line())  # )
        self.write_with_indentation(self.read_tokenized_line())  # {
        self.write_with_indentation("<statements>")
        self.depth += 1
        while self.peek_command() != "}":
            self.compile_statement()
        self.depth -= 1
        self.write_with_indentation("</statements>")
        self.write_with_indentation(self.read_tokenized_line())  # }
        if self.peek_command() == "else":
            self.write_with_indentation(self.read_tokenized_line())  # else
            self.write_with_indentation(self.read_tokenized_line())  # {
            self.write_with_indentation("<statements>")
            self.depth += 1
            while self.peek_command() != "}":
                self.compile_statement()
            self.depth -= 1
            self.write_with_indentation("</statements>")
            self.write_with_indentation(self.read_tokenized_line())  # }
        self.depth -= 1
        self.write_with_indentation("</ifStatement>")

    def compile_while(self):
        """
        Compiles a WhileStatement
        """
        self.write_with_indentation("<whileStatement>")
        self.depth += 1
        self.write_with_indentation(self.read_tokenized_line())  # while
        self.write_with_indentation(self.read_tokenized_line())  # (
        self.compile_expression()
        self.write_with_indentation(self.read_tokenized_line())  # )
        self.write_with_indentation(self.read_tokenized_line())  # {
        self.write_with_indentation("<statements>")
        self.depth += 1
        while self.peek_command() != "}":
            self.compile_statement()
        self.depth -= 1
        self.write_with_indentation("</statements>")

        self.write_with_indentation(self.read_tokenized_line())  # }
        self.depth -= 1
        self.write_with_indentation("</whileStatement>")

    def compile_do(self):
        """
        Compiles a DoStatement
        """
        self.write_with_indentation("<doStatement>")
        self.depth += 1
        while (command := self.peek_command()) != ";":
            if command == "(":
                self.write_with_indentation(self.read_tokenized_line())
                self.compile_expression_list()
            else:
                self.write_with_indentation(self.read_tokenized_line())
        self.write_with_indentation(self.read_tokenized_line())
        self.depth -= 1
        self.write_with_indentation("</doStatement>")

    def compile_return(self):
        """
        Compiles a ReturnStatement
        """
        self.write_with_indentation("<returnStatement>")
        self.depth += 1
        self.write_with_indentation(self.read_tokenized_line())  # retrun
        if self.peek_command() != ";":
            self.compile_expression()
        self.write_with_indentation(self.read_tokenized_line())  # ;

        # while self.peek_command() != ";":
        #     self.write_with_indentation(self.read_tokenized_line())
        # self.write_with_indentation(self.read_tokenized_line())
        self.depth -= 1
        self.write_with_indentation("</returnStatement>")

    def compile_expression(self):
        """
        Compiles an Expression
        """
        self.write_with_indentation("<expression>")
        self.depth += 1
        self.compile_term()
        if self.peek_command() in op_list:
            self.write_with_indentation(self.read_tokenized_line())
            self.compile_term()
        self.depth -= 1
        self.write_with_indentation("</expression>")

    def compile_term(self):
        """
        Compiles a Term.
        :return: null
        """
        self.write_with_indentation("<term>")
        self.depth += 1
        # integerConstant | stringConstant | keywordConstant |varName |
        # varName'['expression']' | subroutineCall |'('expression')' |
        # unaryOp term
        if self.peek_command() in ["-", "~"]:
            # unaryOp term
            self.write_with_indentation(self.read_tokenized_line())  # add unaryOp
            self.compile_term()
        elif self.peek_command() == "(":
            # '('expression')'
            self.write_with_indentation(self.read_tokenized_line())  # add '('
            self.compile_expression()
            self.write_with_indentation(self.read_tokenized_line())  # add ')'
        elif self.peek_command_twice() == "[":
            # VarName '[ expression ']'
            self.write_with_indentation(self.read_tokenized_line())  # add VarName
            self.write_with_indentation(self.read_tokenized_line())  # add '['
            self.compile_expression()
            self.write_with_indentation(self.read_tokenized_line())  # add ']'
        elif self.peek_command_twice() in ["(", "."]:
            # subroutineCall
            self.compile_subroutine_call()
        else:
            # integerConstant | stringConstant | keywordConstant |varName
            self.write_with_indentation(self.read_tokenized_line())  # add term
        self.depth -= 1
        self.write_with_indentation("</term>")

    def compile_subroutine_call(self):
        """
        compiles a subroutine call
        :return:
        """
        # subroutineName'(' expressionList ')'
        if self.peek_command_twice() == "(":
            self.write_with_indentation(
                self.read_tokenized_line()
            )  # add subroutineName
            self.write_with_indentation(self.read_tokenized_line())  # add "("
            self.compile_expression_list()
            self.write_with_indentation(self.read_tokenized_line())  # add ")"
        # (className |varName)
        else:
            self.write_with_indentation(
                self.read_tokenized_line()
            )  # add className |varName
            # '.' subroutineName '(' expressionList ')'
            self.write_with_indentation(self.read_tokenized_line())  # add '.'
            self.write_with_indentation(
                self.read_tokenized_line()
            )  # add subroutineName
            self.write_with_indentation(self.read_tokenized_line())  # add "("
            self.compile_expression_list()
            self.write_with_indentation(self.read_tokenized_line())  # add ")"

    def compile_expression_list(self):
        self.write_with_indentation("<expressionList>")
        self.depth += 1
        while self.peek_command() != ")":
            self.compile_expression()
            if self.peek_command() == ")":
                break
            self.write_with_indentation(self.read_tokenized_line())
        self.depth -= 1
        self.write_with_indentation("</expressionList>")

    def compile_file(self):
        """
        Compile the whole file into output file
        """
        self.compile_class()

    @staticmethod
    def get_xml_val(xml_line: str):
        """
        Extracts the xml value from a given xml row
        """
        return re.match(re.compile(".*<.*> (.*) <.*>"), xml_line).group(1)

    def write_with_indentation(self, message: str):
        """
        Writes a message to the output file with the right indentation
        :param message: message to write
        """
        self.compiled_output_file.write(("  " * self.depth) + message + "\r\n")

    def read_tokenized_line(self):
        """
        Reads a single tokenized lone
        """
        return self.tokenized_file.readline().rstrip("\n")
