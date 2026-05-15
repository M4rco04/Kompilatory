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
# 3. Tabela Symboli (Scope, Typy, Funkcje)
# ==========================================
class SymbolTable:
    def __init__(self):
        # Stos zasięgów dla zmiennych: [{ 'nazwa': 'typ' }]
        self.scopes = [{}]
        # Tabela globalnych podprogramów (funkcje/procedury)
        self.functions = {}
        self._register_builtins()

    def _register_builtins(self):
        """Rejestruje domyślne procedury i funkcje wbudowane (np. wejście/wyjście, stringi)."""
        self.declare_function("write", "void", "any", 0)
        self.declare_function("writeln", "void", "any", 0)
        self.declare_function("read", "void", "any", 0)
        self.declare_function("readln", "void", "any", 0)
        self.declare_function("randomize", "void", [], 0)
        self.declare_function("random", "int", ["int"], 0)

        # Funkcje operacji na tekstach
        self.declare_function("length", "int", ["string"], 0)
        self.declare_function("concat", "string", ["string", "string"], 0)

    # --- Weryfikacja tożsamości identyfikatora (Nowość) ---
    def is_variable(self, name: str) -> bool:
        name_lower = name.lower()
        for scope in reversed(self.scopes):
            if name_lower in scope:
                return True
        return False

    def is_function(self, name: str) -> bool:
        return name.lower() in self.functions

    # --- Zasięgi ---
    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    # --- Zmienne ---
    def declare_variable(self, name: str, var_type: str, line: int, is_array: bool = False):
        name_lower = name.lower()
        current_scope = self.scopes[-1]

        if name_lower in current_scope:
            raise SemanticError(
                f"Podwójna deklaracja (Linia {line}): Zmienna '{name}' została już zadeklarowana w tym zasięgu.")

        current_scope[name_lower] = f"{var_type}_array" if is_array else var_type

    def get_variable_type(self, name: str, line: int) -> str:
        name_lower = name.lower()
        for scope in reversed(self.scopes):
            if name_lower in scope:
                return scope[name_lower]

        raise SemanticError(f"Nieznany identyfikator (Linia {line}): Użycie niezadeklarowanej zmiennej '{name}'.")

    # --- Funkcje i Procedury ---
    def declare_function(self, name: str, return_type: str, param_types: list | str, line: int):
        name_lower = name.lower()
        if name_lower in self.functions:
            raise SemanticError(f"Podwójna deklaracja (Linia {line}): Podprogram '{name}' już istnieje.")
        self.functions[name_lower] = {
            'return_type': return_type,
            'params': param_types
        }

    def get_function_info(self, name: str, line: int) -> dict:
        name_lower = name.lower()
        if name_lower not in self.functions:
            raise SemanticError(
                f"Brak podprogramu (Linia {line}): Próba wywołania nieistniejącej funkcji/procedury '{name}'.")
        return self.functions[name_lower]

    # --- Sprawdzanie Typów ---
    def check_type_compatibility(self, expected: str, actual: str, line: int, context: str):
        if expected == "any" or actual == "any":
            return

        exp_base = expected.replace("_array", "")
        act_base = actual.replace("_array", "")

        if exp_base == act_base:
            return

        if exp_base == "float" and act_base == "int":
            return

        if exp_base == "string" and act_base == "char":
            return

        raise SemanticError(
            f"Niezgodność typów (Linia {line}): {context}. Oczekiwano '{exp_base}', otrzymano '{act_base}'. Błędne rzutowanie!"
        )