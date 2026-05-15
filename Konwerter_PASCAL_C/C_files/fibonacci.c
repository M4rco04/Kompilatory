// Wygenerowano z programu: NtyWyrazFibonacciego
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

int n, i;
int a, b, c;


int main(int argc, char *argv[]) {
    printf("--- Obliczanie n-tego wyrazu Ciagu Fibonacciego ---\n");
    printf("Podaj, ktory wyraz ciagu chcesz obliczyc (n >= 0): ");
    scanf("%d", &n);
    if (n == 0) {
        printf("Wyraz nr 0 to: 0\n");
    } else {
        if (n == 1) {
            printf("Wyraz nr 1 to: 1\n");
        } else {
            a = 0;
            b = 1;
            for (i = 2; i <= n; i++) {
                c = a + b;
                a = b;
                b = c;
            }
            printf("Wyraz nr %d  to: %d\n", n, b);
        }
    }
    printf("\n");
    printf("Nacisnij ENTER, aby zakonczyc...\n");
    getchar();
    return 0;
}
