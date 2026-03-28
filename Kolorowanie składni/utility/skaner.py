from .token import Token
from typing import List, Tuple
from collections.abc import Callable


class Skaner:

    def __init__(self, expression: str):
        self.tokens: List[Tuple[Token, str]] = []
        self.expression: str = expression

        self.fstring_stack: List[str] = []

        self._config: List[Tuple[Token, Callable[[str, int], None]]] = [
            (Token.SPECIAL, self._create_exact("if")),
            (Token.SPECIAL, self._create_exact("else")),
            (Token.SPECIAL, self._create_exact("for")),
            (Token.SPECIAL, self._create_exact("while")),
            (Token.SPECIAL, self._create_exact("def")),
            (Token.SPECIAL, self._create_exact("class")),
            (Token.SPECIAL, self._create_exact("return")),
            (Token.SPECIAL, self._create_exact("True")),
            (Token.SPECIAL, self._create_exact("False")),
            (Token.SPECIAL, self._create_exact("None")),
            (Token.FLOATNUMBER, self.float_automat),
            (Token.HEXNUMBER, self.hex_automat),
            (Token.BINNUMBER, self.bin_automat),
            (Token.OCTNUMBER, self.oct_automat),
            (Token.FSTRING, self.fstring_automat),
            (Token.ID, self.id_automat),
            (Token.STRING, self.string_automat),
            (Token.COMMENT, self.comment_automat),
            (Token.DOUBLESLASHEQUAL, self._create_exact("//=")),
            (Token.DOUBLESLASH, self._create_exact("//")),
            (Token.DOUBLESTAR, self._create_exact("**")),
            (Token.COMPARISON, self._create_exact("==")),
            (Token.NOTEQUAL, self._create_exact("!=")),
            (Token.LESSEQUAL, self._create_exact("<=")),
            (Token.GREATEREQUAL, self._create_exact(">=")),
            (Token.PLUSEQUAL, self._create_exact("+=")),
            (Token.MINUSEQUAL, self._create_exact("-=")),
            (Token.MULEQUAL, self._create_exact("*=")),
            (Token.DIVEQUAL, self._create_exact("/=")),
            (Token.PLUS, self._create_exact("+")),
            (Token.MINUS, self._create_exact("-")),
            (Token.MUL, self._create_exact("*")),
            (Token.DIV, self._create_exact("/")),
            (Token.PERCENT, self._create_exact("%")),
            (Token.EQUAL, self._create_exact("=")),
            (Token.LESS, self._create_exact("<")),
            (Token.GREATER, self._create_exact(">")),
            (Token.BITAND, self._create_exact("&")),
            (Token.BITOR, self._create_exact("|")),
            (Token.LPAREN, self._create_exact("(")),
            (Token.RPAREN, self._create_exact(")")),
            (Token.LSQB, self._create_exact("[")),
            (Token.RSQB, self._create_exact("]")),
            (Token.LBRACE, self._create_exact("{")),
            (Token.RBRACE, self._create_exact("}")),
            (Token.COLON, self._create_exact(":")),
            (Token.COMMA, self._create_exact(",")),
            (Token.DOT, self._create_exact(".")),
            (Token.NEWLINE, self._create_exact("\n")),
            (Token.INDENT, self._create_exact("\t")),
            (Token.SPACE, self.space_automat),
            (Token.NEWLINE, self.newline_automat),
            (Token.INDENT, self.indent_automat),
        ]

        self.automats: List[Callable[[str, int], None]] = [
            cfg[1] for cfg in self._config
        ]
        self.token_types: List[Token] = [cfg[0] for cfg in self._config]
        self.states: List[int] = [0] * len(self.automats)

    def loop(self) -> None:
        i = 0
        while i < len(self.expression):
            token_found = self.scan_next_token(i)

            if token_found:
                i += len(token_found[1])
            else:
                char = self.expression[i]
                self.tokens.append((Token.ERROR, char))
                i += 1

    def scan_next_token(self, start_pos: int) -> Tuple[Token, str] | None:
        self.reset_states()
        temp_token = ""
        last_valid_token = None

        for j in range(start_pos, len(self.expression)):
            char = self.expression[j]
            temp_token += char

            self.run_all_automats(char)
            current_match = self.get_accepted_token_type()

            if current_match:
                last_valid_token = (current_match, temp_token)

            if all(state == 3 for state in self.states):
                break

        if last_valid_token:
            self.tokens.append(last_valid_token)
            return last_valid_token
        return None

    def run_all_automats(self, char: str):
        for idx, automat in enumerate(self.automats):
            automat(char, idx)

    def get_accepted_token_type(self) -> Token | None:
        for idx, state in enumerate(self.states):
            if state in (1, 10, 11):
                return self.token_types[idx]
        return None

    def reset_states(self):
        self.states = [0] * len(self.automats)
        self.fstring_stack.clear()

    """
    Logiczna definicja automatu
    """

    def _create_exact(self, target: str) -> Callable[[str, int], None]:
        def automat(char: str, idx: int) -> None:
            state = self.states[idx]
            if state == 3 or state == 1:
                self.states[idx] = 3
                return

            chars_matched = 0 if state == 0 else state - 3
            if chars_matched < len(target) and char == target[chars_matched]:
                chars_matched += 1
                self.states[idx] = (
                    1 if chars_matched == len(target) else chars_matched + 3
                )
            else:
                self.states[idx] = 3

        return automat

    def id_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 1 if (char.isalpha() or char == "_") else 3
        elif state == 1:
            self.states[idx] = 1 if (char.isalnum() or char == "_") else 3

    def float_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            if char.isdigit():
                self.states[idx] = 1
            elif char == ".":
                self.states[idx] = 4
            else:
                self.states[idx] = 3
        elif state == 1:
            if char.isdigit():
                self.states[idx] = 1
            elif char == ".":
                self.states[idx] = 10
            elif char in "eE":
                self.states[idx] = 5
            else:
                self.states[idx] = 3
        elif state == 4:
            if char.isdigit():
                self.states[idx] = 10
            else:
                self.states[idx] = 3
        elif state == 10:
            if char.isdigit():
                self.states[idx] = 10
            elif char in "eE":
                self.states[idx] = 5
            else:
                self.states[idx] = 3
        elif state == 5:
            if char in "+-":
                self.states[idx] = 6
            elif char.isdigit():
                self.states[idx] = 11
            else:
                self.states[idx] = 3
        elif state == 6:
            if char.isdigit():
                self.states[idx] = 11
            else:
                self.states[idx] = 3
        elif state == 11:
            if char.isdigit():
                self.states[idx] = 11
            else:
                self.states[idx] = 3
        else:
            self.states[idx] = 3

    def hex_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 4 if char == "0" else 3
        elif state == 4:
            self.states[idx] = 5 if char in "xX" else 3
        elif state in (5, 1):
            self.states[idx] = 1 if char in "0123456789abcdefABCDEF" else 3
        else:
            self.states[idx] = 3

    def bin_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 4 if char == "0" else 3
        elif state == 4:
            self.states[idx] = 5 if char in "bB" else 3
        elif state in (5, 1):
            self.states[idx] = 1 if char in "01" else 3
        else:
            self.states[idx] = 3

    def oct_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 4 if char == "0" else 3
        elif state == 4:
            self.states[idx] = 5 if char in "oO" else 3
        elif state in (5, 1):
            self.states[idx] = 1 if char in "01234567" else 3
        else:
            self.states[idx] = 3

    def string_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            if char == '"':
                self.states[idx] = 4
            elif char == "'":
                self.states[idx] = 5
            else:
                self.states[idx] = 3
        elif state == 4:
            self.states[idx] = 1 if char == '"' else 4
        elif state == 5:
            self.states[idx] = 1 if char == "'" else 5
        else:
            self.states[idx] = 3

    def fstring_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]

        if state in (1, 3):
            self.states[idx] = 3
            return

        if state == 0:
            self.states[idx] = 4 if char in 'fF' else 3
            return

        if state == 4:
            if char in '"\'':
                self.fstring_stack.append(char)
                self.states[idx] = 5
            else:
                self.states[idx] = 3
            return

        if state == 5:
            top = self.fstring_stack[-1]
            if char == top:
                self.fstring_stack.pop()
                if not self.fstring_stack:
                    self.states[idx] = 1
                else:
                    self.states[idx] = 3
            elif char == '{':
                self.fstring_stack.append('{')
                self.states[idx] = 6
            return

        if state == 6:
            top = self.fstring_stack[-1]

            if char in '"\'':
                self.fstring_stack.append(char)
                self.states[idx] = 7
            elif char in '{[(':
                self.fstring_stack.append(char)
            elif char in '}])':
                pairs = {'}': '{', ']': '[', ')': '('}

                if top == pairs.get(char):
                    self.fstring_stack.pop()
                    if len(self.fstring_stack) == 1 and self.fstring_stack[0] in '"\'':
                        self.states[idx] = 5
                else:
                    self.states[idx] = 3
            return

        if state == 7:
            top = self.fstring_stack[-1]
            if char == top:
                self.fstring_stack.pop()
                self.states[idx] = 6
            return

    def comment_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 1 if char == "#" else 3
        elif state == 1:
            self.states[idx] = 3 if char == "\n" else 1
        else:
            self.states[idx] = 3

    def space_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state in (0, 1):
            self.states[idx] = 1 if char == " " else 3
        else:
            self.states[idx] = 3

    def indent_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state in (0, 1):
            self.states[idx] = 1 if char == "\t" else 3
        else:
            self.states[idx] = 3

    def newline_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            if char == "\n":
                self.states[idx] = 1
            elif char == "\r":
                self.states[idx] = 4
            else:
                self.states[idx] = 3
        elif state == 4:
            if char == "\n":
                self.states[idx] = 1
            else:
                self.states[idx] = 3
        else:
            self.states[idx] = 3

    def __str__(self) -> str:
        return "\n".join([f"({t[0]}, {t[1]})" for t in self.tokens])
