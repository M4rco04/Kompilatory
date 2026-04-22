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
// REGUŁY PARSERA (Składnia)
// ==========================================

program                 : 'PROGRAM' IDENTIFIER ';' block '.' EOF ;

block                   : declarations compoundStatement ;

declarations            : variableDeclarationPart subprogramDeclarations ;

variableDeclarationPart : 'VAR' variableDeclaration+ 
                        | /* pusto */ 
                        ;

variableDeclaration     : identifierList ':' type ';' ;

identifierList          : IDENTIFIER (',' IDENTIFIER)* ;

type                    : 'INTEGER' | 'REAL' | 'BOOLEAN' | 'CHAR' ;

subprogramDeclarations  : subprogramDeclaration* ;

subprogramDeclaration   : subprogramHead ';' block ';' ;

subprogramHead          : 'PROCEDURE' IDENTIFIER 
                        | 'FUNCTION' IDENTIFIER ':' type 
                        ;

compoundStatement       : 'BEGIN' statementList 'END' ;

statementList           : statement (';' statement)* ;

statement               : assignmentStatement
                        | compoundStatement
                        | ifStatement
                        | whileStatement
                        | emptyStatement 
                        ;

assignmentStatement     : IDENTIFIER ASSIGN expression ;

ifStatement             : 'IF' expression 'THEN' statement ('ELSE' statement)? ;

whileStatement          : 'WHILE' expression 'DO' statement ;

emptyStatement          : /* pusto */ ;

// --- Wyrażenia i priorytety ---
expression              : simpleExpression (REL_OP simpleExpression)? ;

simpleExpression        : term ((ADD_OP | 'OR') term)* ;

term                    : factor ((MUL_OP | INT_OP | 'AND') factor)* ;

factor                  : 'NOT' factor
                        | ADD_OP factor
                        | IDENTIFIER
                        | NUMBER
                        | BOOLEAN_CONST
                        | '(' expression ')' 
                        ;

// ==========================================
// REGUŁY LEXERA (Tokeny)
// ==========================================

ASSIGN          : ':=' ;
COLON           : ':' ;

REL_OP          : '=' | '<>' | '<' | '<=' | '>' | '>=' ;
ADD_OP          : '+' | '-' ;
MUL_OP          : '*' | '/' ;
INT_OP          : 'DIV' | 'MOD' ;

BOOLEAN_CONST   : 'TRUE' | 'FALSE' ;

IDENTIFIER      : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER          : [0-9]+ ('.' [0-9]+)? ;

COMMENT         : ( '{' .*? '}' | '(*' .*? '*)' ) -> skip ;
WS              : [ \t\r\n]+ -> skip ;
```

---

