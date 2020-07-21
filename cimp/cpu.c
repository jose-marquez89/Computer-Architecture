#include <stdio.h>
#include <stdlib.h>

struct random_access {
	int memory[256];
	int mar;
	int mdr;
};

int main()
{
	struct random_access *ram;
	int prog[] = {0b00001000, 0b01001000,
	              0b00001010, 0b10000000};
	int i, j;
	ram = malloc(sizeof(struct random_access));

	for (i=0; i<16; i++) {
		printf("%i\n", ram->memory[i]);
	}
	for (j=0; j<5; j++) {
		printf("%i\n", prog[i]);
	}

	return 0;
}
