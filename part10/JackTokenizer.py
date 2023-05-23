import collections
import re
from enum import Enum
from typing import Iterator

"""
Token type enum
"""


class TokenType(Enum):
    KEYWORD = 1
    SYMBOL = 2
    INTEGER_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTIFIER = 5


"""
KeyWords enum
"""


class keyWords(Enum):
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 11
    LET = 12
    DO = 13
    IF = 14
    ELSE = 15
    WHILE = 16
    RETURN = 17
    TRUE = 18
    FALSE = 19
    NULL = 20
    THIS = 21


"""
Token type dictionary
"""
keyWordsDict = {
    "class": keyWords.CLASS,
    "method": keyWords.METHOD,
    "function": keyWords.FUNCTION,
    "constructor": keyWords.CONSTRUCTOR,
    "int": keyWords.INT,
    "boolean": keyWords.BOOLEAN,
    "char": keyWords.CHAR,
    "void": keyWords.VOID,
    "var": keyWords.VAR,
    "static": keyWords.STATIC,
    "field": keyWords.FIELD,
    "let": keyWords.LET,
    "do": keyWords.DO,
    "if": keyWords.IF,
    "else": keyWords.ELSE,
    "while": keyWords.WHILE,
    "return": keyWords.RETURN,
    "true": keyWords.TRUE,
    "false": keyWords.FALSE,
    "null": keyWords.NULL,
    "this": keyWords.THIS,
}
"""
Symbols enum
"""
symbolDict = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}

KEYWORD_REGEX = "|".join(keyWordsDict.keys())
SYMBOLS = {
    r"{",
    r"}",
    r"(",
    r")",
    r"[",
    r"]",
    r".",
    ";",
    ",",
    r"+",
    "-",
    r"*",
    "/",
    "&",
    "\\",
    r"<",
    r">",
    "=",
    "~",
    ",",
}
SYMBOL_REGEX = "[" + re.escape("|".join(SYMBOLS)) + "]"
INTEGER_CONSTANT_REGEX = r"\d+"
STRING_CONSTANT_REGEX = r"\"[^\"]*\""
IDENTIFIER_REGEX = r"\w+"
REGEX = re.compile(
    f"{KEYWORD_REGEX}|{SYMBOL_REGEX}|{INTEGER_CONSTANT_REGEX}|{STRING_CONSTANT_REGEX}|{IDENTIFIER_REGEX}"
)

TOKEN_TYPE_MAPPING = collections.OrderedDict(
    [
        (INTEGER_CONSTANT_REGEX, TokenType.INTEGER_CONSTANT),
        (STRING_CONSTANT_REGEX, TokenType.STRING_CONSTANT),
        (KEYWORD_REGEX, TokenType.KEYWORD),
        (SYMBOL_REGEX, TokenType.SYMBOL),
        (IDENTIFIER_REGEX, TokenType.IDENTIFIER),
    ]
)


class JackTokenizer:
    def __init__(self, jack_file, current_token):
        """
        Initialize JackTokenizer class
        """
        self.jack_file = jack_file
        self.jack_content = jack_file.read()
        self.jack_content = self.ignore_comments()
        self.current_token = current_token
        self.tokens = self.get_all_tokens()

    def ignore_comments(self):
        """
        Removes all comments from jack content
        """
        removed_inline_comments = re.sub(
            r"(\/\/.*\n)|(\/\*.*?\*\/)", "\n", self.jack_content
        )
        removed_multiline_comments = re.sub(
            r"\/\*\*(.|\n)*\*\/", "\n", removed_inline_comments
        )
        return removed_multiline_comments

    def get_all_tokens(self):
        """
        :return: All tokens by a big regex contains all types of tokens.
        """
        return re.findall(REGEX, self.jack_content)

    def has_more_tokens(self):
        """
        :return: if theres more tokens
        """
        return len(self.tokens) > 0

    def advance(self):
        """
        update current_token to be the next token
        """
        self.current_token = self.tokens.pop(0)

    def token_type(self) -> TokenType:
        """
        :return: the token type of current_token
        """
        for regex, token_type in TOKEN_TYPE_MAPPING.items():
            if re.match(re.compile(regex), self.current_token):
                return token_type

    def key_word(self):
        return f"<keyword> {self.current_token} </keyword>"

    def symbol(self):
        return f"<symbol> {symbolDict.get(self.current_token, self.current_token)} </symbol>"

    def identifier(self):
        return f"<identifier> {self.current_token} </identifier>"

    def in_val(self):
        return f"<integerConstant> {self.current_token} </integerConstant>"

    def string_val(self):
        return f"<stringConstant> {self.current_token[1 : len(self.current_token) - 1]} </stringConstant>"

    def tokenize_file(self) -> Iterator[str]:
        """
        Tokenizes the whole file.
        :return: List of tokenized output
        """
        token_type_to_line_formatter = {
            TokenType.SYMBOL: self.symbol,
            TokenType.KEYWORD: self.key_word,
            TokenType.STRING_CONSTANT: self.string_val,
            TokenType.INTEGER_CONSTANT: self.in_val,
            TokenType.IDENTIFIER: self.identifier,
        }
        yield "<tokens>"
        while self.has_more_tokens():
            self.advance()
            yield token_type_to_line_formatter[self.token_type()]()
        yield "</tokens>"
        yield ""
