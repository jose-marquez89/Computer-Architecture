"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Boot the CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.ir = 0
        self.fl = 0
        self.alu_ops = None

        self.registers[7] = 0xF4

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        prog_path = sys.argv[1]

        with open(prog_path, 'r') as f:
            prog = f.readlines()
            for address, line in enumerate(prog):
                self.ram_write(address, int(line[:8], 2))

    def hlt(self):
        return False

    def prn(self, op):
        operand = self.pc + 1
        print(self.registers[self.ram_read(operand)])
        return True

    def ldi(self):
        operand_a = self.pc + 1
        operand_b = self.pc + 2
        self.registers[self.ram_read(operand_a)] = self.ram_read(operand_b)
        return True

    def mul(self):
        operand_a = self.pc + 1
        operand_b = self.pc + 2
        rp_a = self.ram_read(operand_a)
        rp_b = self.ram_read(operand_b)
        self.registers[rp_a] *= self.registers[rp_b]
        return True

    def build_alu_ops(self):
        self.alu_ops = {0b10100010: self.mul}

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # TODO: implement a branch tree

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print("TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.load()
        self.interpreter = {0b00000001: self.halt,
                            0b10000010: self.ldi}

        running = True

        while running:
            running = self.interpreter[self.ram[self.pc]]()
            self.pc += ((self.ram[self.pc] >> 6) + 1)

        sys.exit()
