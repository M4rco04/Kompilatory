import html
from typing import List, Tuple
from .token import Token


class HtmlGenerator:
    def __init__(self, tokens: List[Tuple[Token, str]]):
        self.tokens = tokens

        self.color_map = {
            Token.SPECIAL: "keyword",
            Token.IMPORT: "import",
            Token.STRING: "string",
            Token.COMMENT: "comment",
            Token.FLOATNUMBER: "number",
            Token.HEXNUMBER: "number",
            Token.BINNUMBER: "number",
            Token.OCTNUMBER: "number",
            Token.ERROR: "error",

            Token.PLUS: "operator", Token.MINUS: "operator", Token.MUL: "operator",
            Token.DIV: "operator", Token.DOUBLESLASH: "operator", Token.DOUBLESTAR: "operator",
            Token.PERCENT: "operator", Token.EQUAL: "operator", Token.PLUSEQUAL: "operator",
            Token.MINUSEQUAL: "operator", Token.MULEQUAL: "operator", Token.DIVEQUAL: "operator",
            Token.DOUBLESLASHEQUAL: "operator", Token.COMPARISON: "operator", Token.NOTEQUAL: "operator",
            Token.LESS: "operator", Token.LESSEQUAL: "operator", Token.GREATER: "operator",
            Token.GREATEREQUAL: "operator", Token.BITAND: "operator", Token.BITOR: "operator",

            Token.COLON: "colon"
        }

    def _get_css_class(self, token_type: Token) -> str:
        return self.color_map.get(token_type, "")

    def _format_fstring(self, value: str) -> str:
        result = ""
        in_brace = False
        current_chunk = ""

        for char in value:
            if char == '{' and not in_brace:
                if current_chunk:
                    result += f'<span class="string">{html.escape(current_chunk)}</span>'
                    current_chunk = ""
                in_brace = True
                current_chunk += char
            elif char == '}' and in_brace:
                current_chunk += char
                result += f'<span class="fstring-var">{html.escape(current_chunk)}</span>'
                current_chunk = ""
                in_brace = False
            else:
                current_chunk += char

        if current_chunk:
            if in_brace:
                result += f'<span class="fstring-var">{html.escape(current_chunk)}</span>'
            else:
                result += f'<span class="string">{html.escape(current_chunk)}</span>'

        return result

    def generate(self, output_filename: str = "pokolorowany_kod.html") -> None:
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='pl'>",
            "<head>",
            "<meta charset='utf-8'>",
            f"<title>{output_filename}</title>",
            "<style>",
            "  body { background-color: #2b2b2b; color: #a9b7c6; font-family: 'Consolas', 'Courier New', monospace; padding: 20px; font-size: 16px; line-height: 1.4; }",
            "  .keyword { color: #cc7832; font-weight: bold; }",
            "  .import { color: #7D0552; }"
            "  .string { color: #6a8759; }",
            "  .number { color: #6897bb; }",
            "  .comment { color: #808080; font-style: italic; }",
            "  .operator { color: #cc7832; }",
            "  .error { background-color: #ff0000; color: #ffffff; font-weight: bold; padding: 0 2px; border-radius: 2px; }",
            "  .fstring-var { color: #9876aa; font-weight: bold; }",
            "  .colon { color: #cc7832; font-weight: bold; }",
            "  .bracket-1 { color: #e8bf6a; font-weight: bold; }",
            "  .bracket-2 { color: #4da6ff; font-weight: bold; }",
            "</style>",
            "</head>",
            "<body>",
            "<pre><code>"
        ]

        open_brackets = {Token.LPAREN, Token.LSQB, getattr(Token, "LBRACE", None)}
        close_brackets = {Token.RPAREN, Token.RSQB, getattr(Token, "RBRACE", None)}

        bracket_depth = 0

        for token_type, value in self.tokens:

            if getattr(token_type, "name", "") == "FSTRING" or token_type == getattr(Token, "FSTRING", None):
                html_parts.append(self._format_fstring(value))
                continue

            escaped_value = html.escape(value)

            if token_type in open_brackets:
                css_class = "bracket-1" if bracket_depth % 2 == 0 else "bracket-2"
                bracket_depth += 1
                html_parts.append(f'<span class="{css_class}">{escaped_value}</span>')
                continue

            elif token_type in close_brackets:
                bracket_depth = max(0, bracket_depth - 1)
                css_class = "bracket-1" if bracket_depth % 2 == 0 else "bracket-2"
                html_parts.append(f'<span class="{css_class}">{escaped_value}</span>')
                continue

            css_class = self._get_css_class(token_type)

            if css_class:
                html_parts.append(f'<span class="{css_class}">{escaped_value}</span>')
            else:
                html_parts.append(escaped_value)

        html_parts.extend([
            "</code></pre>",
            "</body>",
            "</html>"
        ])

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write("".join(html_parts))
            print(f"Pomyślnie wygenerowano plik HTML: {output_filename}")
        except Exception as e:
            print(f"Błąd podczas zapisywania pliku HTML: {e}")