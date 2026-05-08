// Wygenerowano z programu: ObliczanieSilni
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int liczba;

int main(int argc, char *argv[]) {
    printf("Podaj liczbe naturalna (>= 0): ");
    ReadLn(liczba);
    if (liczba < 0) {
        printf("Blad! Silnia jest zdefiniowana tylko dla liczb nieujemnych.");
    } else {
            printf("---");
    printf("%d ", "Wynik za pomoca rekurencji: ", SilniaRekurencyjna(liczba));
    printf("%d ", "Wynik za pomoca iteracji:   ", SilniaIteracyjna(liczba));

    }
    printf("%d ", "Wcisnij ENTER, aby zakonczyc...");
    ReadLn();
    return 0;
}
