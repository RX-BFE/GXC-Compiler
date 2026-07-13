#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** argv)
{
    int x = 10;
    int y = 5;
    int a = x > y;
    int b = x == 10;
    int c = x != y;
    int d = x >= y;
    int e = x <= 20;
    int f = x < 100;
    printf("%d\n", a);
    printf("%d\n", b);
    printf("%d\n", c);
    printf("%d\n", d);
    printf("%d\n", e);
    printf("%d\n", f);
    int g = (x + y) > 10;
    int h = x * 2 == 20;
    printf("%d\n", g);
    printf("%d\n", h);
    return 0;
}