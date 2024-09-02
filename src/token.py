from enum import Enum, auto


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    STAR = auto()
    SLASH = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    # End of file
    EOF = auto()


class Token:
    def __init__(self, type, lexeme, literal, line):
        """
        Initializes a new token.

        :param type: The TokenType of the token (e.g., TokenType.LEFT_PAREN).
        :param lexeme: The actual string or character representation of the token (e.g., '(').
        :param literal: The literal value of the token, if applicable (e.g., the value of a number).
        :param line: The line number where the token appears in the source code.
        """
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        """
        Returns a string representation of the token for debugging purposes.

        :return: A formatted string showing the type, lexeme and literal.
        """
        literal_str = "null" if self.literal is None else str(self.literal)
        return f"{self.type.name} {self.lexeme} {literal_str}"
