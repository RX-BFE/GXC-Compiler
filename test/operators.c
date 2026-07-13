#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** argv)
{
    int a = 10 + 5;
    int b = 10 - 5;
    int c = 10 * 5;
    int d = 10 / 5;
    int e = 10 % 3;
    printf("%d\n", a);
    printf("%d\n", b);
    printf("%d\n", c);
    printf("%d\n", d);
    printf("%d\n", e);
    int f = 10 + 5 * 2;
    int g = (10 + 5) * 2;
    printf("%d\n", f);
    printf("%d\n", g);
    return 0;
}