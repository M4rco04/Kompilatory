program ObliczanieSilni;

{ ==========================================
  1. Wersja rekurencyjna
  ========================================== }
function SilniaRekurencyjna(n: integer): longint;
begin
  if n <= 1 then
    SilniaRekurencyjna := 1
  else
    SilniaRekurencyjna := n * SilniaRekurencyjna(n - 1);
end;

{ ==========================================
  2. Wersja iteracyjna z pętlą REPEAT..UNTIL
  ========================================== }
function SilniaIteracyjna(n: integer): longint;
var
  wynik: longint;
  i: integer;
begin
  wynik := 1;
  i := 1;
  
  if n > 0 then
  begin
    repeat
      wynik := wynik * i;
      i := i + 1;
    until i > n;
  end;
  
  SilniaIteracyjna := wynik;
end;

var
  liczba: integer;

begin
  Write('Podaj liczbe naturalna (>= 0): ');
  ReadLn(liczba);

  if liczba < 0 then
    WriteLn('Blad! Silnia jest zdefiniowana tylko dla liczb nieujemnych.')
  else
  begin
    WriteLn('---');
    WriteLn('Wynik za pomoca rekurencji: ', SilniaRekurencyjna(liczba));
    WriteLn('Wynik za pomoca iteracji:   ', SilniaIteracyjna(liczba));
  end;
  
  WriteLn('Wcisnij ENTER, aby zakonczyc...');
  ReadLn;
end.
