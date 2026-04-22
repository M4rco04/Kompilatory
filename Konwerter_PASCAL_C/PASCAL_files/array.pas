PROGRAM Tablice;
VAR
  wektor : ARRAY [1..100] OF INTEGER;
  macierz : ARRAY [0..9, 0..9] OF REAL;
  i, j : INTEGER;
BEGIN
  wektor[1] := 42;
  macierz[i, j] := wektor[i] + 3.14;
END.
