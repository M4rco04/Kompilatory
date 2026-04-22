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

### Zbiór tokenów
| Kategoria | Nazwa Tokenu | Opis / Wyrażenie Regularne | Przykłady w Pascalu |
| Słowa kluczowe | | Słowa kluczowe w PASCAL | "PROGRAM, VAR, BEGIN, END, INTEGER, REAL, IF, THEN, ELSE, WHILE, DO" |
| Operatory Relacyjne | REL_OP | Operatory porównania | "=, <>, <, <=, >, >=" |
| Operatory Dodawania | ADD_OP | Dodawanie i odejmowanie | "+, -" |
| Operatory Mnożenia | MUL_OP | Mnożenie i dzielenie | "*, /" |
| Znak przypisania | ASSIGN | Operator przypisania wartości. | := |
| Interpunkcja | | Znaki strukturalne | ";, :, ,, ., (, )" |
Identyfikatory,IDENTIFIER,Nazwy zmiennych i programu: [a-zA-Z_][a-zA-Z0-9_]*,"licznik, suma_1"
Liczby,NUMBER,Całkowite i zmiennoprzecinkowe: [0-9]+ ('.' [0-9]+)?,"42, 3.14"
Białe znaki,WS,"Spacje, taby, nowe linie. W parserze są pomijane (-> skip).","spacja, \n, \t"

Wynikiem działania programu będzie plik tekstowy o rozszerzeniu `.c`, który po kompilacji standardowym kompilatorem (np. **GCC**) zachowa semantykę oryginalnego programu napisanego w Pascalu.

---

