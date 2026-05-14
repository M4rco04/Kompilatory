// Wygenerowano z programu: WypelnianieMacierzy
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

int macierz[6][6];
int i, j;


int main(int argc, char *argv[]) {
    srand(time(NULL));
            macierz[i][j] = (rand() % 11);


    printf("Zawartosc macierzy (5x5):\n");
            printf("%d ", macierz[i][j]);

    printf("\n");

    printf("Nacisnij ENTER, aby zakonczyc...\n");
    getchar();
    return 0;
}
