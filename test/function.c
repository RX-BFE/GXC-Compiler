#include <stdio.h>
#include <stdlib.h>

int tambah(int a, int b)
{
    return a + b;
}

int main(int argc, char** argv)
{
    int result = tambah(10, 20);
    printf("%d\n", result);
    return 0;
}