// Wygenerowano z programu: TestTekstu
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

char pojedynczy_znak;
int dlugosc_tekstu;
char tekst_w_tablicy[11];


int main(int argc, char *argv[]) {
    pojedynczy_znak = 'A';
    printf("Test 1 - Znak: %c\n", pojedynczy_znak);
    dlugosc_tekstu = strlen("Witaj Swiecie!");
    printf("Test 3 - Dlugosc tekstu \"Witaj Swiecie!\" to: %d\n", dlugosc_tekstu);
    printf("Test 4 - Proste laczenie: %s\n", _concat("Konwerter ", "Pascal2C"));
    printf("Test 5 - Wielokrotna konkatenacja: %s\n", _concat(_concat("To ", "jest "), _concat("bardzo ", "dlugi tekst!")));
    tekst_w_tablicy[1] = 'P';
    tekst_w_tablicy[2] = 'a';
    tekst_w_tablicy[3] = 's';
    tekst_w_tablicy[4] = 'c';
    tekst_w_tablicy[5] = 'a';
    tekst_w_tablicy[6] = 'l';
    /* Pobieramy trzeci element i przypisujemy do zmiennej pojedynczy_znak */
    pojedynczy_znak = tekst_w_tablicy[3];
    printf("Test 7 - Trzeci element tablicy (indeks 3) to: %c\n", pojedynczy_znak);
    printf("Test 8 - Pierwszy element tablicy (indeks 1) to: %c\n", tekst_w_tablicy[1]);
    printf("Test 6 - Znak: %c  | Dlugosc: %d ", pojedynczy_znak, dlugosc_tekstu);
    printf("\n");
return 0;
}
