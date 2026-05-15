// Wygenerowano z programu: ObliczanieSilni
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

/* Helper do obslugi tekstow z Pascala */
char* _concat(const char* s1, const char* s2) {
    char* res = (char*)malloc(strlen(s1) + strlen(s2) + 1);
    strcpy(res, s1); strcat(res, s2); return res;
}

int liczba;

int SilniaRekurencyjna(int n) {


    if (n <= 1) {
        return 1;
    } else {
        return n * SilniaRekurencyjna(n - 1);
    }
}

int SilniaIteracyjna(int n) {
    int wynik;
    int i;


    wynik = 1;
    i = 1;
    if (n > 0) {
        do {
            wynik = wynik * i;
            i = i + 1;
        } while (!(i > n));
    }
    return wynik;
}


int main(int argc, char *argv[]) {
    printf("Podaj liczbe naturalna (>= 0): ");
    scanf("%d", &liczba);
    if (liczba < 0) {
        printf("Blad! Silnia jest zdefiniowana tylko dla liczb nieujemnych.\n");
    } else {
        printf("---\n");
        printf("Wynik za pomoca rekurencji: %d\n", SilniaRekurencyjna(liczba));
        printf("Wynik za pomoca iteracji:   %d\n", SilniaIteracyjna(liczba));
    }
    printf("Wcisnij ENTER, aby zakonczyc...\n");
    getchar();
    return 0;
}
