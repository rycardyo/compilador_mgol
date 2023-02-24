#include <stdio.h>
typedef char literal[256];
void main(void)
{
	/*----Variaveis temporarias----*/
	int T1;
	int T2;
	int T3;
	int T4;
	int T5;
	/*------------------------------*/
	literal	A	;
	int	D	, B	;
	float	C	;
	printf("Digite B:");
	scanf("%d", &B);
	printf("Digite A:");
	scanf("%s", A);
	T1 = D > 2.5;
	if (T1) {
		T2 = B <= 4;
		if (T2) {
			printf("B esta entre 2 e 4");
		}
	}
	C = 5.7;
	T3 = B + 2;
	B = T3;
	T4 = B + 5;
	B = T4;
	T5 = C + 7;
	C = T5;
	D = B;
	C = 5.0;
	printf("\nB=\n");
	printf("%d", D);
	printf("\n");
	printf("%f", C);
	printf("\n");
	printf("%s", A);
}
