from sys import argv

from deduct_lang.lexer import Lexer

with open(argv[-1]) as f:
    code = f.read()

tokens = Lexer(code).consume_all()

print("tokens", "".join(tokens))
