// Wygenerowano z programu: WypelnianieMacierzy
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int macierz[6][6];
int i, j;

int main(int argc, char *argv[]) {
    Randomize();
    for (i = 1; i <= 5; i++) {
            for (j = 1; j <= 5; j++) {
            macierz[i][j] = Random(11);

    }

    }
    printf("Zawartosc macierzy (5x5):");
    for (i = 1; i <= 5; i++) {
            for (j = 1; j <= 5; j++) {
            printf("%d ", macierz[i][j]);

    }
    printf("\n");

    }
    printf("%d ", "Nacisnij ENTER, aby zakonczyc...");
    ReadLn();
    return 0;
}
