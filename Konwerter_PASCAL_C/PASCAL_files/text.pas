PROGRAM TestTekstu;

VAR
    pojedynczy_znak : CHAR;
    dlugosc_tekstu : INTEGER;
    tekst_w_tablicy : ARRAY [1..10] OF CHAR;

BEGIN
    pojedynczy_znak := 'A';
    WriteLn('Test 1 - Znak: ', pojedynczy_znak);

    dlugosc_tekstu := length('Witaj Swiecie!');
    WriteLn('Test 3 - Dlugosc tekstu "Witaj Swiecie!" to: ', dlugosc_tekstu);

    WriteLn('Test 4 - Proste laczenie: ', concat('Konwerter ', 'Pascal2C'));

    WriteLn('Test 5 - Wielokrotna konkatenacja: ',
            concat(
                concat('To ', 'jest '),
                concat('bardzo ', 'dlugi tekst!')
            )
    );

    tekst_w_tablicy[1] := 'P';
    tekst_w_tablicy[2] := 'a';
    tekst_w_tablicy[3] := 's';
    tekst_w_tablicy[4] := 'c';
    tekst_w_tablicy[5] := 'a';
    tekst_w_tablicy[6] := 'l';

    { Pobieramy trzeci element i przypisujemy do zmiennej pojedynczy_znak }
    pojedynczy_znak := tekst_w_tablicy[3];
    WriteLn('Test 7 - Trzeci element tablicy (indeks 3) to: ', pojedynczy_znak);

    WriteLn('Test 8 - Pierwszy element tablicy (indeks 1) to: ', tekst_w_tablicy[1]);

    Write('Test 6 - Znak: ', pojedynczy_znak, ' | Dlugosc: ', dlugosc_tekstu);
    WriteLn();
END.