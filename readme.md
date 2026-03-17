# Język implementacji

Python

# Zbiór tokenów

| Typ Tokenu | Automat           | Regex                | Opis wzorca                                      |
|------------|------------------|----------------------|--------------------------------------------------|
| NUMBER     | number_automat   | `[0-9]+`             | Jedna lub więcej cyfr.                          |
| ID         | id_automat       | `[a-zA-Z][a-zA-Z0-9]*` | Litera, po której następuje dowolna liczba liter lub cyfr. |
| PLUS       | plus_automat     | `+`                 | Znak plusa.                           |
| MINUS      | minus_automat    | `-`                  | Znak minusa.                          |
| MUL        | mul_automat      | `*`                 | Mnożenie.             |
| DIV        | div_automat      | `/`                  | Dzielenie.                  |
| LPAREN     | lparen_automat   | `(`                 | Nawias otwierający.                             |
| RPAREN     | rparen_automat   | `)`                 | Nawias zamykający.                              |
