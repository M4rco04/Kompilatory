// Wygenerowano z programu: WypelnianieMacierzy
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int macierz[6][6];
int i, j;


int main(int argc, char *argv[]) {
    srand(time(NULL));
    for (i = 1; i <= 5; i++) {
            for (j = 1; j <= 5; j++) {
            macierz[i][j] = (rand() % 11);

    }

    }
    printf("Zawartosc macierzy (5x5):\n");
    for (i = 1; i <= 5; i++) {
            for (j = 1; j <= 5; j++) {
            printf("%d ", macierz[i][j]);

    }
    printf("\n");

    }
    printf("Nacisnij ENTER, aby zakonczyc...\n");
    getchar();
    return 0;
}
