from .token import Token
from typing import List, Tuple
from collections.abc import Callable


class Skaner:

    def __init__(self, expression: str):
        self.tokens: List[Tuple[Token, str]] = []
        self.expression: str = expression

        self.states: List[int] = [0] * 8
        self.automats: List[Callable[[str, int], None]] = [
            self.number_automat,
            self.id_automat,
            self.plus_automat,
            self.minus_automat,
            self.mul_automat,
            self.div_automat,
            self.lparen_automat,
            self.rparen_automat,
        ]

    def loop(self) -> None:
        i = 0
        while i < len(self.expression):
            char = self.expression[i]

            if char.isspace():
                i += 1
                continue

            token_found = self.scan_next_token(i)

            if token_found:
                i += len(token_found[1])
            else:
                raise SyntaxError(f"Nieoczekiwany znak '{char}' na pozycji {i+1}")

    def scan_next_token(self, start_pos: int) -> Tuple[Token, str] | None:
        self.reset_states()
        temp_token = ""
        last_valid_token = None

        for j in range(start_pos, len(self.expression)):
            char = self.expression[j]
            if char.isspace() and not temp_token:
                continue

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

    def get_accepted_token_type(self):
        if self.states[0] == 1:
            return Token.NUMBER
        if self.states[1] == 1:
            return Token.ID
        if self.states[2] == 1:
            return Token.PLUS
        if self.states[3] == 1:
            return Token.MINUS
        if self.states[4] == 1:
            return Token.MUL
        if self.states[5] == 1:
            return Token.DIV
        if self.states[6] == 1:
            return Token.LPAREN
        if self.states[7] == 1:
            return Token.RPAREN
        return None

    def reset_states(self):
        self.states = [0] * 8

    def number_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state in [0, 1]:
            if char.isdigit():
                self.states[idx] = 1
            else:
                self.states[idx] = 3

    def id_automat(self, char: str, idx: int) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 1 if char.isalpha() else 3
        elif state == 1:
            self.states[idx] = 1 if (char.isalnum()) else 3

    def _single_char_automat(self, char: str, idx: int, target: str) -> None:
        state = self.states[idx]
        if state == 0:
            self.states[idx] = 1 if char == target else 3
        elif state == 1:
            self.states[idx] = 3

    def plus_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, "+")

    def minus_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, "-")

    def mul_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, "*")

    def div_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, "/")

    def lparen_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, "(")

    def rparen_automat(self, char: str, idx: int) -> None:
        self._single_char_automat(char, idx, ")")

    def __str__(self) -> str:
        return "\n".join([f"({t[0]}, {t[1]})" for t in self.tokens])
