#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define HLT 0b00000001
#define LDI 0b10000010
#define PRN 0b01000111

struct random_access {
	int memory[256];
	int mar;
	int mdr;
};

/* Function prototypes */
void prn(int reg_a);
int ram_read(int mem_addr);
void ram_write(int mem_addr, int mem_data);
void load(void);
int hlt(void);
int ldi(int operand_a, int operand_b, int pc);
int mul(void);
void alu(int op, int reg_a, int reg_b);
/* TODO: define the functions */

int main()
{
	int pc;
	int running = 1;
	int prog[] = {0b00001000, 0b01001000,
	              0b00001010, 0b10000000};
	struct random_access *ram;
	ram = malloc(sizeof(struct random_access));

	while (running == TRUE){
		switch ()
		/* TODO: write all cases */
	}

	return 0;
}

int hlt(void) {
	return FALSE;
}

int ldi(int op_a, int op_b, int pc) {
	op_a = pc + 1;
	op_b = pc + 2;
	/* TODO: point to the register that needs to be changed */
}
