PROGRAM WypelnianieMacierzy;

VAR
  macierz : ARRAY [1..5, 1..5] OF INTEGER;
  i, j : INTEGER;

BEGIN
  Randomize; 

  FOR i := 1 TO 5 DO
  BEGIN
    FOR j := 1 TO 5 DO
    BEGIN
      macierz[i, j] := Random(11);
    END;
  END;

  WriteLn('Zawartosc macierzy (5x5):');
  FOR i := 1 TO 5 DO
  BEGIN
    FOR j := 1 TO 5 DO
    BEGIN
      Write(macierz[i, j]:4);
    END;
    WriteLn;
  END;
  
  WriteLn('Nacisnij ENTER, aby zakonczyc...');
  ReadLn;
END.
