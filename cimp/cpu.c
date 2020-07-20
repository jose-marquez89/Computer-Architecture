#include <stdio.h>
#include <stdlib.h>

struct ram {
	int memory[256];
	int mar;
	int mdr;
};

int main()
{
	int registers[8];
	int rc;



	for (rc=0; rc<8; rc++) {
		registers[rc] = 0;
	}

	for (rc=0; rc<8; rc++) {
		registers[rc] = rc * 2;
	}

	for (rc=0; rc<8; rc++) {
		printf("%i ", registers[rc]);
	}
	putchar('\n');
	return 0;
}
