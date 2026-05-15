from antlr4.error.ErrorListener import ErrorListener


# ==========================================
# 1. Główne Klasy Wyjątków
# ==========================================
class CompilerException(Exception):
    """Bazowa klasa dla wszystkich błędów naszego kompilatora."""
    pass


class SyntaxError(CompilerException):
    pass


class SemanticError(CompilerException):
    pass


# ==========================================
# 2. Przechwytywanie Błędów ANTLR
# ==========================================
class CustomErrorListener(ErrorListener):
    """Zastępuje domyślne zachowanie ANTLR - zatrzymuje proces przy pierwszym błędzie."""

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"Błąd składniowy w Linii {line}, Kolumnie {column}: {msg}")


# ==========================================
# 3. Tabela Symboli z obsługą Zasięgów (Scopes)
# ==========================================
class SymbolTable:
    """Zarządza zmiennymi, sprawdzając ich deklaracje i zakres widoczności."""

    def __init__(self):
        # Inicjalizujemy ze stosem - na dnie jest zakres globalny
        self.scopes = [{}]

    def enter_scope(self):
        """Wywoływane przy wejściu do nowej procedury/funkcji."""
        self.scopes.append({})

    def exit_scope(self):
        """Wywoływane przy wyjściu z procedury/funkcji."""
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare_variable(self, name: str, var_type: str, line: int):
        """Rejestruje nową zmienną w aktualnym zasięgu."""
        name_lower = name.lower()
        current_scope = self.scopes[-1]

        if name_lower in current_scope:
            raise SemanticError(
                f"Błąd semantyczny (Linia {line}): Zmienna '{name}' została już zadeklarowana w tym zasięgu.")

        current_scope[name_lower] = var_type

    def get_variable_type(self, name: str, line: int):
        """Pobiera typ zmiennej. Szuka od zasięgu lokalnego aż do globalnego."""
        name_lower = name.lower()

        for scope in reversed(self.scopes):
            if name_lower in scope:
                return scope[name_lower]

        raise SemanticError(f"Błąd semantyczny (Linia {line}): Użycie niezadeklarowanej zmiennej '{name}'.")

    def exists(self, name: str) -> bool:
        """Sprawdza, czy zmienna w ogóle istnieje bez rzucania błędu."""
        name_lower = name.lower()
        for scope in reversed(self.scopes):
            if name_lower in scope:
                return True
        return False
