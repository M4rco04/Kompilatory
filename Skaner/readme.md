# 🐍 Język implementacji
Python

---

# 📖 Opis Projektu
Projekt implementuje własny analizator leksykalny (skaner) dla prostych wyrażeń matematycznych. Narzędzie to pobiera tekst od użytkownika i dzieli go na mniejsze jednostki znaczeniowe, zwane tokenami. Podczas skanowania program automatycznie ignoruje wszelkie białe znaki, takie jak spacje. 

Proces rozpoznawania opiera się na koncepcji automatów skończonych – dla każdego znaku uruchamiana jest lista dedykowanych funkcji sprawdzających stany dopasowania. Jeżeli analizator natrafi na symbol, który nie pasuje do żadnego z automatów, przerywa działanie i rzuca wyjątek `SyntaxError` ze wskazaniem nieoczekiwanego znaku oraz jego pozycji.

---

# 📚 Zbiór tokenów
Do przechowywania rodzajów dopasowanych elementów wykorzystywana jest klasa `Token` dziedzicząca po `Enum`. Poniższa tabela opisuje pełen zbiór:

| Typ Tokenu | Automat | Regex | Opis wzorca | Wartość wewnętrzna Enuma |
|---|---|---|---|---|
| **NUMBER** | number_automat | `[0-9]+` | Jedna lub więcej cyfr. | "liczba" |
| **ID** | id_automat | `[a-zA-Z][a-zA-Z0-9]*` | Litera, po której następuje dowolna liczba liter lub cyfr. | "identyfikator" |
| **PLUS** | plus_automat | `+` | Znak plusa. | "+" |
| **MINUS** | minus_automat | `-` | Znak minusa. | "-" |
| **MUL** | mul_automat | `*` | Mnożenie. | "*" |
| **DIV** | div_automat | `/` | Dzielenie. | "/" |
| **LPAREN** | lparen_automat | `(` | Nawias otwierający. | "(" |
| **RPAREN** | rparen_automat | `)` | Nawias zamykający. | ")" |

*W pliku źródłowym zdefiniowano także awaryjny token `ERROR` o wartości `?`.*

---

# 📂 Struktura plików
* **`main.py`**: Skrypt uruchomieniowy. Pyta użytkownika o wyrażenie (`input()`), przekazuje je do skanera, uruchamia główną pętlę i na koniec wypisuje na ekran przetworzone dane.
* **`utility\skaner.py`**: Główna logika programu. Znajduje się tu klasa `Skaner` zarządzająca przepływem znaków, przechowująca stany (`0`, `1`, `3`) i wywołująca odpowiednie automaty weryfikujące poprawność.
* **`utility\token.py`**: Zbiór stałych w postaci typu wyliczeniowego `Enum`, które etykietują sklasyfikowane fragmenty tekstu.

---

# 🚀 Uruchomienie i przykład działania
Aby skorzystać ze skanera, uruchom projekt w konsoli:
`python main.py`

**Przykład wykonania:**
1. Konsola wyświetli zachętę: `Wprowadź wyrażenie matematyczne`.
2. Wpisz np.: `zmienna + 10`
3. Program przetworzy wejście pętlą `loop()` i wygeneruje na wyjściu wynikowe krotki w formacie `(Token.TYP, wartość)`.