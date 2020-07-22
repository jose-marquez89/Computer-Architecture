"""CPU functionality."""

import sys
import logging

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
# logging.disable(logging.DEBUG)


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
        valid_for_address = 0

        with open(prog_path, 'r') as f:
            prog = f.readlines()
            logging.debug(f"File Split: {prog}")
            for line in prog:
                if line.startswith("#"):
                    continue
                self.ram_write(valid_for_address, int(line[:8], 2))
                valid_for_address += 1

        logging.debug(f"RAM: {self.ram}")

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

    def add(self):
        operand_a = self.pc + 1
        operand_b = self.pc + 2
        rp_a = self.ram_read(operand_a)
        rp_b = self.ram_read(operand_b)
        self.registers[rp_a] += self.registers[rp_b]
        return True

    def push(self, from_call=False):
        """Push the content of the specified register on to the stack"""
        self.sp -= 1

        # Get the instruction directly after call, if subroutine
        if from_call:
            self.ram_write(self.sp, self.pc + 2)
            return True

        logging.debug(f"Pushing to stack at address {hex(self.sp)}")
        copy_reg = self.ram_read(self.pc + 1)
        logging.debug(f"copy_reg (PUSH): {copy_reg}")

        self.ram_write(self.sp, self.registers[copy_reg])
        return True

    def pop(self, from_ret=False):
        logging.debug(f"Popping from stack at address {hex(self.sp)}")
        if self.sp == 0xF4:
            print("Program attempted to pop from an empty stack. Aborting.")
            return False

        # if returning from subroutine, set pc
        if from_ret:
            self.pc = self.ram_read(self.sp)
            self.sp += 1
            return True

        copy_reg = self.ram_read(self.pc + 1)

        self.registers[copy_reg] = self.ram_read(self.sp)
        self.sp += 1
        return True

    def call(self):
        """Call subroutine and change pc"""
        self.push(from_call=True)
        self.pc = self.registers[self.ram_read(self.pc + 1)]
        return -1

    def ret(self):
        """Return from subroutine and change pc"""
        self.pop(from_ret=True)
        return -1

    def build_interpreter(self):
        self.interpreter = {0b00000001: self.hlt,
                            0b10000010: self.ldi,
                            0b01000111: self.prn,
                            0b01000110: self.pop,
                            0b01000101: self.push,
                            0b01010000: self.call,
                            0b00010001: self.ret}
        return

    def build_alu_ops(self):
        self.alu_ops = {0b10100010: self.mul,
                        0b10100000: self.add}
        return

    def alu(self, op, branch_table):
        """ALU operations."""
        logging.debug(f"Operation Code: {op} - {self.alu_ops[op]}")

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

        logging.debug(f"Start pc: {self.pc}")

        while running:
            op = self.ram_read(self.pc)
            switch = (op & 0b00100000) >> 5
            # Handle with ALU is switch == 1
            if switch:
                self.alu(op, self.alu_ops)
            else:
                running = self.interpreter[self.ram_read(self.pc)]()
                logging.debug(f"Operation Code: {op} - {self.interpreter[op]}")

            # when executing CALL and RET, do not
            if running == -1:
                running = True
            else:
                # Increment PC
                self.pc += ((op >> 6) + 1)

            logging.debug(f"pc: {self.pc}")

        sys.exit()
