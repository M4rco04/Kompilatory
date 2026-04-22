# 📄 Dokumentacja Projektu: Pascal2C Converter

## 👤 Dane autora
- **Imię i nazwisko:** Marek Górny  
- **Kontakt:** 📧 marekgorny1231@gmail.com  

---

## ⚙️ Założenia programu

### 🔄 Rodzaj translatora
Program jest **kompilatorem źródło-źródło** (*source-to-source compiler*).

Proces nie obejmuje generowania kodu maszynowego, lecz transformację wysokopoziomową między dwoma językami trzeciej generacji.

---

### 🧑‍💻 Język implementacji
- **Język:** 🐍 Python  
- **Narzędzia wspomagające:** 🛠️ ANTLR (generator parserów)

### 🎯 Ogólne cele programu
Głównym celem projektu jest stworzenie narzędzia umożliwiającego automatyczną translację kodu źródłowego zapisanego w języku **Pascal** na czytelny i kompilowalny kod w języku **C**.

Program ma za zadanie:

- 🔁 Mapowanie struktur sterujących:
  - `if`
  - `while`
  - `for`
  - `repeat-until`
- 🔧 Transformację definicji typów oraz zmiennych
- 🧩 Obsługę specyficznych dla Pascala elementów (np. zagnieżdżone procedury)
- 📝 Zachowanie komentarzy i logicznej struktury kodu źródłowego

---

### 📦 Planowany wynik działania programu
Konwerter Pascala do C.
Wynikiem działania programu będzie plik tekstowy o rozszerzeniu `.c`, który po kompilacji standardowym kompilatorem (np. **GCC**) zachowa semantykę oryginalnego programu napisanego w Pascalu.

### Zbiór tokenów

| Kategoria | Nazwa Tokenu | Opis / Wyrażenie Regularne | Przykłady w Pascalu |
| --------- | ------------ | -------------------------- | ------------------- |
| Słowa kluczowe | KEYWORD | Słowa kluczowe w PASCAL | "PROGRAM, VAR, BEGIN, END, INTEGER, REAL, IF, THEN, ELSE, WHILE, DO" |
| Operatory Relacyjne | REL_OP | Operatory porównania | "=, <>, <, <=, >, >=" |
| Operatory Dodawania | ADD_OP | Dodawanie i odejmowanie | "+, -" |
| Operatory Mnożenia | MUL_OP | Mnożenie i dzielenie | "*, /" |
| Operatory całkowite | INT_OP | Dzielenie całkowite i modulo | DIV, MOD |
| Operatory logiczne | LOG_OP | Operatory logiczne | AND, OR, NOT |
| Znak przypisania | ASSIGN | Operator przypisania wartości. | := |
| Interpunkcja | | Znaki strukturalne | "; , . ( )" |
| Dwukropek | COLON | Separator typu / deklaracji| : |
| Identyfikatory | IDENTIFIER | Nazwy zmiennych i programu: [a-zA-Z_][a-zA-Z0-9_]* | "licznik, suma_1" |
| Liczby | NUMBER | Całkowite i zmiennoprzecinkowe: [0-9]+ ('.' [0-9]+)? | "42, 3.14" |
| Stałe logiczne | BOOLEAN_CONST | Wartości logiczne | TRUE, FALSE |
| Komentarze | COMMENT | Komentarze blokowe | { komentarz }, (* komentarz *) |
| Typy danych | TYPE | Typy wbudowane | INTEGER, REAL, BOOLEAN, CHAR |
| Procedury/Funkcje | SUBPROGRAM | Definicje podprogramów | PROCEDURE, FUNCTION |
| Białe znaki | WS | "Spacje, taby, nowe linie. | "spacja, \n, \t" |




---

