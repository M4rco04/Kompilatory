PROGRAM NiezgodnoscTypowTest;

VAR
    liczba: INTEGER;
    znak: CHAR;
    logika: BOOLEAN;

BEGIN
    { 1. Poprawne przypisania }
    liczba := 100;
    znak := 'A';
    logika := TRUE;

    { 2. NIEZGODNOŚĆ TYPÓW  }

    { Przykład A: Przypisanie znaku do liczby }
    liczba := 'Z';

    { Przykład B: Przypisanie liczby do zmiennej logicznej }
    logika := 42;

    { Przykład C: Próba wykonania operacji matematycznej na znaku }
    liczba := znak + 10;
END.