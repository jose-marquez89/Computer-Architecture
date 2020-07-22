"""CPU functionality."""

import sys
import logging

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.disable(logging.DEBUG)


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Boot the CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.ir = 0
        self.fl = 0

        self.registers[7] = 0xF4
        self.sp = self.registers[7]

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

    def prn(self):
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

    def push(self):
        self.sp -= 1
        copy_reg = self.pc + 1
        self.ram_write(self.sp, self.registers[copy_reg])
        return True

    def pop(self):
        if self.sp == 0xF4:
            print("Program attempted to pop from an empty stack. Aborting.")
            return False
        copy_reg = self.pc + 1
        self.registers[copy_reg] = self.ram_read(self.sp)
        self.sp += 1
        return True

    def build_interpreter(self):
        self.interpreter = {0b00000001: self.hlt,
                            0b10000010: self.ldi,
                            0b01000111: self.prn,
                            0b10000110: self.pop,
                            0b01000101: self.push}
        logging.debug(f"(codes, functions) -> {self.interpreter.items()}")
        return

    def build_alu_ops(self):
        self.alu_ops = {0b10100010: self.mul}
        logging.debug(f"(ALU codes, functions) -> {self.alu_ops.items()}")
        return

    def alu(self, op, branch_table):
        """ALU operations."""

        if op in branch_table:
            return branch_table[op]()
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
        self.build_interpreter()
        self.build_alu_ops()

        running = True

        while running:
            op = self.ram_read(self.pc)
            logging.debug(f"Operation Code: {op}")
            switch = (op & 0b00100000) >> 5
            # Handle with ALU is switch == 1
            if switch:
                self.alu(op, self.alu_ops)
            else:
                running = self.interpreter[self.ram_read(self.pc)]()
            # Increment PC
            self.pc += ((op >> 6) + 1)

        sys.exit()
