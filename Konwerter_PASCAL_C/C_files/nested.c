// Wygenerowano z programu: NestedTest
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

int global_x;

void OuterProc(int param_a) {
    int local_y;

    int InnerFunc(int param_b) {
        int local_z;


        local_z = 5;
        /* InnerFunc ma dostęp do:
      1. Swoich zmiennych lokalnych (local_z) i parametrów (param_b)
      2. Zmiennych lokalnych i parametrów procedury nadrzędnej (local_y, param_a)
      3. Zmiennych globalnych programu (global_x) */
        return global_x + param_a + local_y + param_b + local_z;
    }


    local_y = 10;
    printf("Wartosci w OuterProc:\n");
    printf("param_a = %d\n", param_a);
    printf("local_y = %d\n", local_y);
    /* Wywołanie zagnieżdżonej funkcji wewnątrz procedury nadrzędnej */
    printf("Wynik zagniezdzonej funkcji InnerFunc: %d\n", InnerFunc(20));
}


int main(int argc, char *argv[]) {
    global_x = 100;
    printf("Uruchamiam program glowny...\n");
    OuterProc(2);
    return 0;
}
