program NtyWyrazFibonacciego;

var
  n, i: integer;
  a, b, c: longint;

begin
  writeln('--- Obliczanie n-tego wyrazu Ciagu Fibonacciego ---');
  write('Podaj, ktory wyraz ciagu chcesz obliczyc (n >= 0): ');
  readln(n);

  if n = 0 then
    writeln('Wyraz nr 0 to: 0')
  else if n = 1 then
    writeln('Wyraz nr 1 to: 1')
  else
  begin
    a := 0;
    b := 1;

    for i := 2 to n do
    begin
      c := a + b;
      a := b;
      b := c;
    end;

    writeln('Wyraz nr ', n, ' to: ', b);
  end;

  writeln;
  writeln('Nacisnij ENTER, aby zakonczyc...');
  readln;
end.