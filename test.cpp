#include <stdio.h>
#include <math.h>

int solve (double a, double b, double c, double* x1, double* x2);
const int SS_INF_ROOTS = -1;
int main()
{

    printf("Enter coefficients for solving a equation\n");
    double a = 0, b = 0, c = 0;
    scanf("%lg %lg %lg", &a, &b, &c);

    double x1 = 0, x2 = 0;
    int nroots = solve( a, b, c, &x1, &x2);
    switch (nroots){
        case 0: printf ("no roots\n");
                break;
        case 1: printf ("x = %lg\n", x1);
                break;
        case 2: printf ("x1 = %lg, x2 = %lg\n", x1, x2);
                break;
        case SS_INF_ROOTS: printf("any number\n");
                break;
        default: printf("error\n");
                return 1;
    return 0;
    }
}
int solve(double a, double b, double c, double* x1, double* x2){
    if (a ==0){
        if (b == 0){
            return (c == 0)?SS_INF_ROOTS:0;
        }
        else{
            *x1 = -c/b;
        return 1;
        }
    }
    else{
        double diskr;
        diskr = b*b - 4*a*c;
        if (diskr == 0){
*x1 = *x2 = -b/ (2*a);
            return 1;
        }
        else if (diskr < 0) {
            return 0;
        }
        else{
            *x1 = -b + sqrt(diskr);
            *x2 = -b - sqrt(diskr);
            return 2;
        }
    }
}
