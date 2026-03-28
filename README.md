# Język implementacji

Python

# Zbiór tokenów

| Typ Tokenu | Automat           | Regex                | Opis wzorca                                      |
|------------|------------------|----------------------|--------------------------------------------------|
| FLOATNUMBER     | number_automat   | `(?:\d+(?:_\d+)*)?\.\d+(?:_\d+)*(?:[eE][+-]?\d+(?:_\d+)*)?\|\d+(?:_\d+)*[eE][+-]?\d+(?:_\d+)*`             | Liczba zmiennoprzecinkowa (z notacją naukową) |
| BINNUMBER | | `0[bB](?:_?[01])+` | Liczba binarna |
| OCTNUMBER | | `0[oO](?:_?[0-7])+` | Liczba ósemkowa |
| HEXNUMBER | | `0[xX](?:+?[0-9a-fA-F])+` | Liczba szesnastkowa |
| ID         | id_automat       | `[a-zA-Z_][a-zA-Z0-9_]*` | Litera, po której następuje dowolna liczba liter lub cyfr |
| PLUS       | plus_automat     | `+`                 | Znak plusa                         |
| MINUS      | minus_automat    | `-`                  | Znak minusa                         |
| MUL        | mul_automat      | `*`                 | Mnożenie        |
| DIV        | div_automat      | `/`                  | Dzielenie              |
| DOUBLESLASH | | `//` | Dzielenie całkowite |
| DOUBLESTAR | | `**` | Potęgowanie |
| PERCENT | | `%` | Modulo, reszta z dzielenia |
| LPAREN     | lparen_automat   | `(`                 | Nawias otwierający                         |
| RPAREN     | rparen_automat   | `)`                 | Nawias zamykający                         |
| LSQB | | `[` | Nawias otwierający kwadratowy |
| RSQB | | `]` | Nawias zamykający kwadratowy |
| LBRACE | | `{` | Klamra otwierająca |
| RBRACE | | `}` | Klamra zamykająca |
| EQUAL | | `=` | Przypisanie |
| PLUSEQUAL | | `+=` | Przypisanie z dodaniem |
| MINUSEQUAL | | `-=` | Przypisanie z odejmowaniem |
| MULEQUAL | | `*=` | Przypisanie z mnożeniem |
| DIVEQUAL | | `/=` | Przypisanie z dzieleniem |
| DOUBLESLASHEQUAL | | `//=` | Przypisanie z dzieleniem całkowitym |
| COMPARISON | | `==` | Porównanie wartości |
| NOTEQUAL | | `!=` | Nierówne |
| LESS | | `<` | Mniejsze |
| LESSEQUAL | | `<=` | Mniejsze lub równe |
| GREATER | | `>` | Większe |
| GREATEREQUAL | | `>=` | Większe lub równe |
| COLON | | `:` | Dwukropek |
| COMMA | | `,` | Przecinek |
| DOT | | `\.` | Kropka |
| BITAND | | `&` | Bitowe AND |
| BITOR | | `\|` | Bitowe OR |
| NEWLINE | | `\n` | Enter |
| INDENT | | `\t` | Tabulator |
| SPACE | | `\s` | Spacja |
| ERROR | | | Błąd |
| COMMENT | | `(#.*)\|('''.*''')` | Komentarz |
