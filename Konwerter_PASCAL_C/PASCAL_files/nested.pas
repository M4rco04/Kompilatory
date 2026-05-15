program NestedTest;

var
  global_x: integer;

procedure OuterProc(param_a: integer);
var
  local_y: integer;

  { --- ZAGNIEŻDŻONA FUNKCJA --- }
  function InnerFunc(param_b: integer): integer;
  var
    local_z: integer;
  begin
    local_z := 5;

    { InnerFunc ma dostęp do:
      1. Swoich zmiennych lokalnych (local_z) i parametrów (param_b)
      2. Zmiennych lokalnych i parametrów procedury nadrzędnej (local_y, param_a)
      3. Zmiennych globalnych programu (global_x) }

    InnerFunc := global_x + param_a + local_y + param_b + local_z;
  end;

begin
  local_y := 10;

  writeln('Wartosci w OuterProc:');
  writeln('param_a = ', param_a);
  writeln('local_y = ', local_y);

  { Wywołanie zagnieżdżonej funkcji wewnątrz procedury nadrzędnej }
  writeln('Wynik zagniezdzonej funkcji InnerFunc: ', InnerFunc(20));
end;

{ --- GŁÓWNY BLOK PROGRAMU --- }
begin
  global_x := 100;

  writeln('Uruchamiam program glowny...');
  OuterProc(2);
end.