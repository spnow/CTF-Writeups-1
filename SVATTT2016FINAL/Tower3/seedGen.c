#include <stdio.h>

int main(){
	int seed = 0x58411520;
	int i = 0,a,b,c,d,e;
	for(i = 0;i < 0x5000; i++)
	{
		srand(seed);
		a = rand() % 1024;
		b = rand() % 1024;
		c = rand() % 1024;
		d = rand() % 1024;
		e = rand() % 1024;
		if (a == 0xff |b == 0xff |c == 0xff |d == 0xff |e == 0xff )
			printf("%x\n",seed);
		seed +=1;
	}
}
