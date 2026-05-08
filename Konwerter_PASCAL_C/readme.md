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
- **Narzędzia wspomagające:** 🛠️ ANTLR (generator parserów) - [Testowanie gramatyki](http://lab.antlr.org/)

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

---

## Zbiór tokenów

| Kategoria | Nazwa tokenu | Regex / Definicja | Opis / wyrażenie | Przykłady w Pascalu |
| :--- | :--- | :--- | :--- | :--- |
| **Słowa kluczowe (program)** | `KEYWORD_PROGRAM` | `PROGRAM` | deklaracja programu | `PROGRAM` |
| **Słowa kluczowe (blok)** | `KEYWORD_VAR`, `KEYWORD_BEGIN`, `KEYWORD_END` | `VAR`, `BEGIN`, `END` | sekcje programu | `VAR, BEGIN, END` |
| **Sterowanie** | `KEYWORD_IF`, `KEYWORD_THEN`, `KEYWORD_ELSE` | `IF`, `THEN`, `ELSE` | instrukcje warunkowe | `IF THEN ELSE` |
| **Pętle** | `KEYWORD_WHILE`, `KEYWORD_DO`, `KEYWORD_FOR`, `KEYWORD_TO`, `KEYWORD_REPEAT`, `KEYWORD_UNTIL` | `WHILE`, `DO`, `FOR`, `TO`, `REPEAT`, `UNTIL` | pętle | `WHILE, FOR, REPEAT UNTIL` |
| **Case** | `KEYWORD_CASE`, `KEYWORD_OF` | `CASE`, `OF` | instrukcja wyboru | `CASE OF` |
| **Podprogramy** | `KEYWORD_PROCEDURE`, `KEYWORD_FUNCTION` | `PROCEDURE`, `FUNCTION` | procedury i funkcje | `PROCEDURE, FUNCTION` |
| **Tablice** | `KEYWORD_ARRAY` | `ARRAY` | deklaracja tablicy | `ARRAY` |
| **Typy danych** | `TYPE_INTEGER`, `TYPE_REAL`, `TYPE_BOOLEAN`, `TYPE_CHAR`, `TYPE_LONGINT` | `INTEGER`, `REAL`, `BOOLEAN`, `CHAR`, `LONGINT` | typy wbudowane | `INTEGER, REAL, BOOLEAN...` |
| **Operatory relacyjne** | `REL_OP` | `= \| <> \| < \| <= \| > \| >=` | porównania | `=, <>, <, <=, >, >=` |
| **Operatory arytmetyczne** | `ADD_OP` | `\+ \| \-` | dodawanie / odejmowanie | `+ , -` |
| **Operatory arytmetyczne** | `MUL_OP` | `\* \| /` | mnożenie / dzielenie | `* , /` |
| **Operatory całkowite** | `INT_OP` | `DIV \| MOD` | dzielenie całkowite i modulo | `DIV, MOD` |
| **Operatory logiczne** | `LOG_OP_AND`, `LOG_OP_OR`, `LOG_OP_NOT` | `AND`, `OR`, `NOT` | logika | `AND, OR, NOT` |
| **Przypisanie** | `ASSIGN` | `:=` | przypisanie wartości | `:=` |
| **Separatory** | `PUNCT_SEMI` | `;` | średnik | `;` |
| **Separatory** | `PUNCT_COMMA` | `,` | przecinek | `,` |
| **Separatory** | `PUNCT_DOT` | `\.` | kropka | `.` |
| **Zakres (tablice)** | `PUNCT_DOTDOT` | `\.\.` | operator zakresu | `..` |
| **Nawiasy okrągłe** | `PUNCT_LPAREN`, `PUNCT_RPAREN` | `\(`, `\)` | nawiasy grupujące / parametry | `( )` |
| **Nawiasy kwadratowe** | `PUNCT_LBRACKET`, `PUNCT_RBRACKET` | `\[`, `\]` | indeksowanie tablic | `[ ]` |
| **Dwukropek** | `COLON` | `:` | typy i deklaracje | `:` |
| **Identyfikatory** | `IDENTIFIER` | `[a-zA-Z_][a-zA-Z0-9_]*` | nazwy zmiennych/funkcji | `x, suma_1, _temp` |
| **Liczby** | `NUMBER` | `[0-9]+(\.[0-9]+)?` | liczby całkowite i rzeczywiste | `42, 3.14` |
| **Stałe logiczne** | `BOOLEAN_CONST` | `TRUE \| FALSE` | wartości logiczne | `TRUE, FALSE` |
| **Stałe tekstowe/znakowe** | `STRING` | `'(''\|[^'])*'` | napisy i pojedyncze znaki | `'hello', 'a'` |
| **Komentarze** | `COMMENT` | `\{.*?\} \| \(\*.*?\*\)` | `{ }`, `(* *)` | `{ komentarz }` |
| **Białe znaki** | `WS` | `[ \t\r\n]+` | spacje, taby, nowe linie | `\n \t space` |
| **Koniec wejścia** | `EOF` | *(koniec strumienia wejściowego)* | koniec pliku | — |

## Gramatyka formatu

Gramatyka zapisana w notacji generatora **ANTLR4**.

```antlr
grammar Pascal;

// ==========================================
// PARSER
// ==========================================

program
    : KEYWORD_PROGRAM IDENTIFIER (PUNCT_LPAREN identifierList PUNCT_RPAREN)? PUNCT_SEMI block PUNCT_DOT EOF
    ;

block
    : declarations compoundStatement
    ;

declarations
    : variableDeclarationPart subprogramDeclarations
    ;

variableDeclarationPart
    : KEYWORD_VAR variableDeclaration+
    | /* puste */
    ;

variableDeclaration
    : identifierList COLON type PUNCT_SEMI
    ;

identifierList
    : IDENTIFIER (PUNCT_COMMA IDENTIFIER)*
    ;

// --- Obsługa typów i tablic ---
type
    : simpleType
    | arrayType
    ;

simpleType
    : TYPE_INTEGER
    | TYPE_REAL
    | TYPE_BOOLEAN
    | TYPE_CHAR
    | TYPE_LONGINT
    ;

arrayType
    : KEYWORD_ARRAY PUNCT_LBRACKET indexRange (PUNCT_COMMA indexRange)* PUNCT_RBRACKET KEYWORD_OF type
    ;

indexRange
    : sign? constant PUNCT_DOTDOT sign? constant
    ;

sign
    : ADD_OP
    ;

// --- Podprogramy ---
subprogramDeclarations
    : subprogramDeclaration*
    ;

subprogramDeclaration
    : subprogramHead PUNCT_SEMI block PUNCT_SEMI
    ;

subprogramHead
    : KEYWORD_PROCEDURE IDENTIFIER formalParameterList?
    | KEYWORD_FUNCTION IDENTIFIER formalParameterList? COLON type
    ;

formalParameterList
    : PUNCT_LPAREN formalParameterGroup (PUNCT_SEMI formalParameterGroup)* PUNCT_RPAREN
    ;

formalParameterGroup
    : identifierList COLON type
    ;

// --- Zmienne ---
variable
    : IDENTIFIER (PUNCT_LBRACKET expression (PUNCT_COMMA expression)* PUNCT_RBRACKET)?
    ;

// --- Instrukcje ---
compoundStatement
    : KEYWORD_BEGIN statementList KEYWORD_END
    ;

statementList
    : statement (PUNCT_SEMI statement)*
    ;

statement
    : assignmentStatement
    | compoundStatement
    | ifStatement
    | whileStatement
    | forStatement
    | repeatStatement
    | caseStatement
    | procedureCall
    | /* puste */
    ;

assignmentStatement
    : variable ASSIGN expression
    ;

caseStatement
    : KEYWORD_CASE expression KEYWORD_OF caseElement+ KEYWORD_END
    ;

caseElement
    : caseLabelList COLON statement PUNCT_SEMI
    ;

caseLabelList
    : constant (PUNCT_COMMA constant)*
    ;

constant
    : NUMBER
    | STRING
    | BOOLEAN_CONST
    ;

procedureCall
    : IDENTIFIER (PUNCT_LPAREN argumentList? PUNCT_RPAREN)?
    ;

argumentList
    : expression (PUNCT_COMMA expression)*
    ;

ifStatement
    : KEYWORD_IF expression KEYWORD_THEN statement (KEYWORD_ELSE statement)?
    ;

whileStatement
    : KEYWORD_WHILE expression KEYWORD_DO statement
    ;

repeatStatement
    : KEYWORD_REPEAT statementList KEYWORD_UNTIL expression
    ;

forStatement
    : KEYWORD_FOR IDENTIFIER ASSIGN expression KEYWORD_TO expression KEYWORD_DO statement
    ;

// ==========================================
// WYRAŻENIA
// ==========================================

expression
    : simpleExpression (REL_OP simpleExpression)?
    ;

simpleExpression
    : term ((ADD_OP | LOG_OP_OR) term)*
    ;

term
    : factor ((MUL_OP | INT_OP | LOG_OP_AND) factor)*
    ;

factor
    : LOG_OP_NOT factor
    | ADD_OP factor
    | procedureCall
    | variable
    | NUMBER
    | BOOLEAN_CONST
    | STRING
    | PUNCT_LPAREN expression PUNCT_RPAREN
    ;

// ==========================================
// LEXER
// ==========================================

// --- słowa kluczowe ---
KEYWORD_PROGRAM   : P R O G R A M ;
KEYWORD_VAR       : V A R ;
KEYWORD_BEGIN     : B E G I N ;
KEYWORD_END       : E N D ;
KEYWORD_IF        : I F ;
KEYWORD_THEN      : T H E N ;
KEYWORD_ELSE      : E L S E ;
KEYWORD_WHILE     : W H I L E ;
KEYWORD_DO        : D O ;
KEYWORD_FOR       : F O R ;
KEYWORD_TO        : T O ;
KEYWORD_PROCEDURE : P R O C E D U R E ;
KEYWORD_FUNCTION  : F U N C T I O N ;
KEYWORD_REPEAT    : R E P E A T ;
KEYWORD_UNTIL     : U N T I L ;
KEYWORD_CASE      : C A S E ;
KEYWORD_OF        : O F ;
KEYWORD_ARRAY     : A R R A Y ;

// --- typy ---
TYPE_INTEGER : I N T E G E R ;
TYPE_REAL    : R E A L ;
TYPE_BOOLEAN : B O O L E A N ;
TYPE_CHAR    : C H A R ;
TYPE_LONGINT : L O N G I N T ;

// --- operatory ---
REL_OP  : '=' | '<>' | '<' | '<=' | '>' | '>=' ;
ADD_OP  : '+' | '-' ;
MUL_OP  : '*' | '/' ;
INT_OP  : D I V | M O D ;

// --- logiczne ---
LOG_OP_AND : A N D ;
LOG_OP_OR  : O R ;
LOG_OP_NOT : N O T ;

// --- przypisanie ---
ASSIGN : ':=' ;

// --- interpunkcja ---
PUNCT_SEMI     : ';' ;
PUNCT_COMMA    : ',' ;
PUNCT_DOT      : '.' ;
PUNCT_LPAREN   : '(' ;
PUNCT_RPAREN   : ')' ;
PUNCT_LBRACKET : '[' ;
PUNCT_RBRACKET : ']' ;
PUNCT_DOTDOT   : '..' ;

// --- inne ---
COLON : ':' ;

// --- stringi ---
STRING
    : '\'' ( '\'\'' | ~'\'' )* '\''
    ;

// --- wartości ---
BOOLEAN_CONST
    : T R U E
    | F A L S E
    ;

IDENTIFIER
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

NUMBER
    : [0-9]+ ('.' [0-9]+)?
    ;

// --- komentarze ---
COMMENT
    : ('{' .*? '}' | '(*' .*? '*)') -> channel(HIDDEN)
    ;

// --- białe znaki ---
WS
    : [ \t\r\n]+ -> channel(HIDDEN)
    ;

// ==========================================
// CASE INSENSITIVE
// ==========================================

fragment A:[aA]; fragment B:[bB]; fragment C:[cC];
fragment D:[dD]; fragment E:[eE]; fragment F:[fF];
fragment G:[gG]; fragment H:[hH]; fragment I:[iI];
fragment J:[jJ]; fragment K:[kK]; fragment L:[lL];
fragment M:[mM]; fragment N:[nN]; fragment O:[oO];
fragment P:[pP]; fragment Q:[qQ]; fragment R:[rR];
fragment S:[sS]; fragment T:[tT]; fragment U:[uU];
fragment V:[vV]; fragment W:[wW]; fragment X:[xX];
fragment Y:[yY]; fragment Z:[zZ];
```

---

