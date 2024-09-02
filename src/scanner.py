import sys
from typing import List, Optional

from .token import Token, TokenType


class Scanner:
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str):
        """
        Initializes the scanner with the given source code.

        :param source: The source code to be scanned.
        """
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error = False

    def scan_tokens(self) -> List[Token]:
        """
        Scans the entire source code and returns a list of tokens.

        :return: A list of tokens identified in the source code.
        """
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        """Scans a single token from the source."""
        char = self.advance()

        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
                # Implement block comment or division as needed
            case " " | "\r" | "\t":
                pass  # Ignore whitespace
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _ if char.isdigit():
                self.number()
            case _ if char.isalpha() or char == "_":
                self.identifier()
            case _:
                self.error = True
                print(
                    f"[line {self.line}] Error: Unexpected character: {char}",
                    file=sys.stderr,
                )

    def is_at_end(self) -> bool:
        """Checks if the scanner has reached the end of the source."""
        return self.current >= len(self.source)

    def advance(self) -> str:
        """Advances the current position and returns the current character."""
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Optional[object] = None) -> None:
        """Adds a token of the given type to the token list."""
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        """Matches the next character against an expected character."""
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        """Peeks at the current character without advancing."""
        return "\0" if self.is_at_end() else self.source[self.current]

    def string(self) -> None:
        """Handles string literals."""
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error = True
            print(
                f"[line {self.line}] Error: Unterminated string.",
                file=sys.stderr,
            )
            return

        self.advance()  # Consume the closing "
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self) -> None:
        """Handles number literals."""
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()  # Consume the dot
            while self.peek().isdigit():
                self.advance()

        value = float(self.source[self.start : self.current])
        self.add_token(TokenType.NUMBER, value)

    def peek_next(self) -> str:
        """Peeks at the next character without advancing."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def identifier(self) -> None:
        """Handles identifiers and reserved keywords."""
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start : self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)
