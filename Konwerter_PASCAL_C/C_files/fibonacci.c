// Wygenerowano z programu: NtyWyrazFibonacciego
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int n, i;
int a, b, c;

int main(int argc, char *argv[]) {
    printf("--- Obliczanie n-tego wyrazu Ciagu Fibonacciego ---");
    printf("%d ", "Podaj, ktory wyraz ciagu chcesz obliczyc (n >= 0): ");
    readln(n);
    if (n == 0) {
        printf("Wyraz nr 0 to: 0");
    } else {
        if (n == 1) {
        printf("Wyraz nr 1 to: 1");
    } else {
            a = 0;
    b = 1;
    for (i = 2; i <= n; i++) {
            c = a + b;
    a = b;
    b = c;

    }
    printf("%d ", "Wyraz nr ", n, " to: ", b);

    }
    }
    printf("\n");
    printf("%d ", "Nacisnij ENTER, aby zakonczyc...");
    readln();
    return 0;
}
