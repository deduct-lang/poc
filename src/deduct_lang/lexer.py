__all__ = ("Lexer",)

from collections import deque


class Lexer:
    """字句解析器"""

    def __init__(self, code: str) -> None:
        self.code = deque(code)

        self.tokens = list[str]()
        self.word = None

    def consume_all(self) -> list[str]:
        while self.code:
            self.consume()

        return self.tokens

    def consume(self) -> None:
        char = self.code.popleft()

        match char:
            case "\t" | " " | "　" | "\n":
                self.consume_blank()
            case "{" | "}" | "[" | "]" | "," | "@":
                self.consume_special_character(char)
            case _:
                self.consume_word_character(char)

    def consume_blank(self) -> None:
        self.consume_word()

    def consume_special_character(self, char: str) -> None:
        self.consume_word()
        self.tokens.append(char)

    def consume_word_character(self, char: str) -> None:
        if self.word is None:
            self.word = ""

        self.word += char

    def consume_word(self) -> None:
        if self.word is not None:
            self.tokens.append(self.word)
            self.word = None
