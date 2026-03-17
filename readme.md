# Zbiór tokenów

| Typ Tokenu | Automat           | Regex                | Opis wzorca                                      |
|------------|------------------|----------------------|--------------------------------------------------|
| NUMBER     | number_automat   | `[0-9]+`             | Jedna lub więcej cyfr.                          |
| ID         | id_automat       | `[a-zA-Z][a-zA-Z0-9]*` | Litera, po której następuje dowolna liczba liter lub cyfr. |
| PLUS       | plus_automat     | `\+`                 | Dosłownie znak plusa.                           |
| MINUS      | minus_automat    | `-`                  | Dosłownie znak minusa.                          |
| MUL        | mul_automat      | `\*`                 | Dosłownie znak gwiazdki (mnożenia).             |
| DIV        | div_automat      | `/`                  | Dosłownie ukośnik (dzielenia).                  |
| LPAREN     | lparen_automat   | `\(`                 | Nawias otwierający.                             |
| RPAREN     | rparen_automat   | `\)`                 | Nawias zamykający.                              |
