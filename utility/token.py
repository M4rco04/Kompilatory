from enum import Enum


class Token(Enum):
    NUMBER = "liczba"
    ID = "identyfikator"
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    ERROR = "?"
