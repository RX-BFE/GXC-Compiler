#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
    int sum = 0;
    for (int i = 0; i < 5; i = i + 1) {
    sum = sum + i;
    }
    printf("%d\n", sum);
    return 0;
}