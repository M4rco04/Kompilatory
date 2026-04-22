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

## Zbiór tokenów

| Kategoria | Nazwa Tokenu | Opis / Wyrażenie Regularne | Przykłady w Pascalu |
| --------- | ------------ | -------------------------- | ------------------- |
| Słowa kluczowe | KEYWORD | Słowa kluczowe w PASCAL | "PROGRAM, VAR, BEGIN, END, INTEGER, REAL, IF, THEN, ELSE, WHILE, DO" |
| Operatory Relacyjne | REL_OP | Operatory porównania | "=, <>, <, <=, >, >=" |
| Operatory Dodawania | ADD_OP | Dodawanie i odejmowanie | "+, -" |
| Operatory Mnożenia | MUL_OP | Mnożenie i dzielenie | "*, /" |
| Operatory całkowite | INT_OP | Dzielenie całkowite i modulo | DIV, MOD |
| Operatory logiczne | LOG_OP | Operatory logiczne | AND, OR, NOT |
| Znak przypisania | ASSIGN | Operator przypisania wartości. | := |
| Interpunkcja | PUNCT | Znaki strukturalne | "; , . ( )" |
| Dwukropek | COLON | Separator typu / deklaracji| : |
| Identyfikatory | IDENTIFIER | Nazwy zmiennych i programu: [a-zA-Z_][a-zA-Z0-9_]* | "licznik, suma_1" |
| Liczby | NUMBER | Całkowite i zmiennoprzecinkowe: [0-9]+ ('.' [0-9]+)? | "42, 3.14" |
| Stałe logiczne | BOOLEAN_CONST | Wartości logiczne | TRUE, FALSE |
| Komentarze | COMMENT | Komentarze blokowe | { komentarz }, (* komentarz *) |
| Typy danych | TYPE | Typy wbudowane | INTEGER, REAL, BOOLEAN, CHAR |
| Procedury/Funkcje | SUBPROGRAM | Definicje podprogramów | PROCEDURE, FUNCTION |
| Białe znaki | WS | "Spacje, taby, nowe linie. | "spacja, \n, \t" |
| Koniec pliku | EOF | Koniec wejścia | — |

## Gramatyka formatu

Gramatyka zapisana w notacji generatora **ANTLR4**.

```antlr
grammar Pascal;

// ==========================================
// PARSER
// ==========================================

program
    : KEYWORD_PROGRAM IDENTIFIER PUNCT_SEMI block PUNCT_DOT EOF
    ;

block
    : declarations compoundStatement
    ;

declarations
    : variableDeclarationPart subprogramDeclarations
    ;

variableDeclarationPart
    : KEYWORD_VAR variableDeclaration+
    | 
    ;

variableDeclaration
    : identifierList COLON type PUNCT_SEMI
    ;

identifierList
    : IDENTIFIER (PUNCT_COMMA IDENTIFIER)*
    ;

type
    : TYPE
    ;

subprogramDeclarations
    : subprogramDeclaration*
    ;

subprogramDeclaration
    : subprogramHead PUNCT_SEMI block PUNCT_SEMI
    ;

subprogramHead
    : KEYWORD_PROCEDURE IDENTIFIER
    | KEYWORD_FUNCTION IDENTIFIER COLON type
    ;

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
    | 
    ;

assignmentStatement
    : IDENTIFIER ASSIGN expression
    ;

ifStatement
    : KEYWORD_IF expression KEYWORD_THEN statement (KEYWORD_ELSE statement)?
    ;

whileStatement
    : KEYWORD_WHILE expression KEYWORD_DO statement
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
    | IDENTIFIER
    | NUMBER
    | BOOLEAN_CONST
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
KEYWORD_PROCEDURE : P R O C E D U R E ;
KEYWORD_FUNCTION  : F U N C T I O N ;

// --- typy ---
TYPE
    : I N T E G E R
    | R E A L
    | B O O L E A N
    | C H A R
    ;

// --- operatory ---
REL_OP  : '=' | '<>' | '<' | '<=' | '>' | '>=' ;
ADD_OP  : '+' | '-' ;
MUL_OP  : '*' | '/' ;
INT_OP  : D I V | M O D ;

// --- logiczne (rozdzielone dla parsera) ---
LOG_OP_AND : A N D ;
LOG_OP_OR  : O R ;
LOG_OP_NOT : N O T ;

// --- przypisanie ---
ASSIGN : ':=' ;

// --- interpunkcja ---
PUNCT_SEMI   : ';' ;
PUNCT_COMMA  : ',' ;
PUNCT_DOT    : '.' ;
PUNCT_LPAREN : '(' ;
PUNCT_RPAREN : ')' ;

// --- inne ---
COLON : ':' ;

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
    : '{' .*? '}'
    | '(*' .*? '*)'
    -> skip
    ;

// --- białe znaki ---
WS
    : [ \t\r\n]+ -> skip
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

