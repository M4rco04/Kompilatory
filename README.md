---

# 🚀 Jak uruchomić projekt

Możesz uruchomić skaner na dwa sposoby:

## 1. Tryb analizy pliku (zalecany)

Jeśli masz już plik z kodem (np. `test.py`), przekaż jego nazwę jako argument wiersza poleceń:

```bash
python main.py test.py
```

Program:

* wczyta plik,
* wyświetli listę tokenów w konsoli,
* wygeneruje plik `pokolorowany_kod.html`.

---

## 2. Tryb interaktywny (konsola)

Uruchom skrypt bez argumentów:

```bash
python main.py
```

Program poprosi o wpisanie lub wklejenie kodu bezpośrednio do konsoli.

### Zakończenie wprowadzania (EOF)

* **Windows**: `Ctrl + Z`, następnie `Enter`
* **Linux / macOS**: `Ctrl + D`

---

# ⚙️ Generowanie HTML (Syntax Highlighting)

Po każdym skanowaniu program automatycznie generuje plik:

```
pokolorowany_kod.html
```

Otwórz go w przeglądarce, aby zobaczyć kod z kolorowaniem składni.

---

# 🐍 Język implementacji

**Python**

---

# 📚 Zbiór tokenów i architektura

Skaner opiera się na ręcznie zdefiniowanych automatach.
Do obsługi stałych fragmentów (np. operatorów i słów kluczowych) używana jest funkcja:

```
_create_exact
```

---

## 🧩 Typy tokenów

| Typ Tokenu       | Automat           | Regex (odpowiednik)                                                                              | Opis                           |
| ---------------- | ----------------- | ------------------------------------------------------------------------------------------------ | ------------------------------ |
| FLOATNUMBER      | `float_automat`   | `(?:\d+(?:_\d+)*)?\.\d+(?:_\d+)*(?:[eE][+-]?\d+(?:_\d+)*)? \| \d+(?:_\d+)*[eE][+-]?\d+(?:_\d+)*` | Liczba zmiennoprzecinkowa      |
| NUMBER           | `float_automat`   | `\d+(?:_\d+)*`                                                                                   | Liczba całkowita               |
| BINNUMBER        | `bin_automat`     | `0[bB](?:_?[01])+`                                                                               | Liczba binarna                 |
| OCTNUMBER        | `oct_automat`     | `0[oO](?:_?[0-7])+`                                                                              | Liczba ósemkowa                |
| HEXNUMBER        | `hex_automat`     | `0[xX](?:_?[0-9a-fA-F])+`                                                                        | Liczba szesnastkowa            |
| ID               | `id_automat`      | `[a-zA-Z_][a-zA-Z0-9_]*`                                                                         | Identyfikator                  |
| SPECIAL          | `_create_exact`   | `\b(?:if\|else\|for\|while\|def\|class\|return\|True\|False\|None)\b`                            | Słowa kluczowe                 |
| FSTRING          | `fstring_automat` | —                                                                                                | F-string (obsługa stosu / PDA) |
| STRING           | `string_automat`  | `""".*?""" \| '''.*?''' \| ".*?" \| '.*?'`                                                       | Napisy                         |
| PLUS             | `_create_exact`   | `\+`                                                                                             | Plus                           |
| MINUS            | `_create_exact`   | `-`                                                                                              | Minus                          |
| MUL              | `_create_exact`   | `\*`                                                                                             | Mnożenie                       |
| DIV              | `_create_exact`   | `/`                                                                                              | Dzielenie                      |
| DOUBLESLASH      | `_create_exact`   | `//`                                                                                             | Dzielenie całkowite            |
| DOUBLESTAR       | `_create_exact`   | `\*\*`                                                                                           | Potęgowanie                    |
| PERCENT          | `_create_exact`   | `%`                                                                                              | Modulo                         |
| LPAREN           | `_create_exact`   | `\(`                                                                                             | `(`                            |
| RPAREN           | `_create_exact`   | `\)`                                                                                             | `)`                            |
| LSQB             | `_create_exact`   | `\[`                                                                                             | `[`                            |
| RSQB             | `_create_exact`   | `\]`                                                                                             | `]`                            |
| LBRACE           | `_create_exact`   | `\{`                                                                                             | `{`                            |
| RBRACE           | `_create_exact`   | `\}`                                                                                             | `}`                            |
| EQUAL            | `_create_exact`   | `=`                                                                                              | Przypisanie                    |
| PLUSEQUAL        | `_create_exact`   | `\+=`                                                                                            | `+=`                           |
| MINUSEQUAL       | `_create_exact`   | `-=`                                                                                             | `-=`                           |
| MULEQUAL         | `_create_exact`   | `\*=`                                                                                            | `*=`                           |
| DIVEQUAL         | `_create_exact`   | `/=`                                                                                             | `/=`                           |
| DOUBLESLASHEQUAL | `_create_exact`   | `//=`                                                                                            | `//=`                          |
| COMPARISON       | `_create_exact`   | `==`                                                                                             | Porównanie                     |
| NOTEQUAL         | `_create_exact`   | `!=`                                                                                             | Różne                          |
| LESS             | `_create_exact`   | `<`                                                                                              | Mniejsze                       |
| LESSEQUAL        | `_create_exact`   | `<=`                                                                                             | ≤                              |
| GREATER          | `_create_exact`   | `>`                                                                                              | Większe                        |
| GREATEREQUAL     | `_create_exact`   | `>=`                                                                                             | ≥                              |
| COLON            | `_create_exact`   | `:`                                                                                              | Dwukropek                      |
| COMMA            | `_create_exact`   | `,`                                                                                              | Przecinek                      |
| DOT              | `_create_exact`   | `\.`                                                                                             | Kropka                         |
| BITAND           | `_create_exact`   | `&`                                                                                              | AND                            |
| BITOR            | `_create_exact`   | `\|`                                                                                             | OR                             |
| NEWLINE          | `newline_automat` | `\n \| \r\n`                                                                                     | Nowa linia                     |
| INDENT           | `indent_automat`  | `\t`                                                                                             | Tabulator                      |
| SPACE            | `space_automat`   | `[ \f\v]+`                                                                                       | Spacja                         |
| COMMENT          | `comment_automat` | `#.*`                                                                                            | Komentarz                      |
| ERROR            | —                 | `.`                                                                                              | Błąd leksykalny                |
---
