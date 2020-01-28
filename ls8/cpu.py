"""CPU functionality."""

import sys

# Add the HLT instruction definition to cpu.py so that you can refer to it by name instead of by numeric value.

# operation codes:
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers.
        self.ram = [0] * 256
        self.register = [0] * 8
        # Also add properties for any internal registers
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0
        self.isPaused = False

        self.dispatch = {
            HLT: self.op_HLT,
            LDI: self.op_LDI,
            PRN: self.op_PRN,
            MUL: self.op_MUL,
            # PUSH: self.op_PUSH,
            # POP: self.op_POP,
            # CALL: self.op_CALL,
            # RET: self.op_RET,
            # ADD: self.op_ADD
        }

    '''
    TODO: In CPU, add method ram_read() and ram_write() that access the RAM inside the CPU object.
    '''

    def ram_read(self, address):
        '''
        Should accept the address to read and return the value stored there
        '''
        return self.ram[address]

    def ram_write(self, value, address):
        '''
        Should accept a value to write, and the address to write it to
        '''
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        '''
        TODO: Step 7: Un-hardcode the machine code
        In load(), you will now want to use those command line arguments to open a file, read in its contents line by line, and save appropriate data into RAM.
        '''

        address = 0

        fp = open(filename, "r")
        for line in fp:
            # As you process lines from the file, you should be on the lookout for blank lines (ignore them), and you should ignore everything after a #, since that's a comment.
            instruction = line.split("#")[0].strip()
            if instruction == "":
                continue
            # You'll have to convert the binary strings to integer values to store in RAM. The built-in int() function can do that when you specify a number base as the second argument
            value = int(instruction, 2)
            self.ram[address] = value
            address += 1

    def alu(self, op, register_a, register_b):
        """ALU operations."""
        '''
        TODO: Step 8: Implement a Multiply and Print the Result
        '''
        if op == "ADD":
            self.register[register_a] += self.register[register_b]

        # Multiply the values in two registers together and store the result in registerA.
        elif op == "MUL":
            self.register[register_a] *= self.register[register_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        '''
        TODO: Step 3: Implement the core of CPU's run() method
        It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register.
        '''
        while not self.isPaused:

            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # Depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec. Maybe an if-elif cascade...?
            if ir in self.dispatch:
                self.dispatch[ir](operand_a, operand_b)
            else:
                raise Exception(
                    f'Unknown Instruction {bin(ir)} at {hex(self.pc)}')

            # Check out the spec where it talks about instruction layout.
            # The two high bits of the instruction tell you how many operands the instruction has. The value of those two bits plus one is the number of bytes you have to move the `PC`.
            # Use `>>` and an `&` mask to extract those two bits, then add one to the result, then add that to the `PC` to get to the next instruction.

            instruction_size = (ir >> 6) + 1
            instruction_sets_pc = ((ir >> 4) & 0b1) == 1

            if not instruction_sets_pc:
                self.pc += instruction_size

    def op_HLT(self, operand_a, operand_b):
        '''
        TODO: Step 4: Implement the HLT instruction handler
        In run() in your switch, exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded. We can consider HLT to be similar to Python's exit() in that we stop whatever we are doing, wherever we are.
        '''
        self.isPaused = True

    def op_LDI(self, operand_a, operand_b):
        '''
        TODO: Step 5: Add the LDI instruction
        Set the value of a register to an integer.
        '''
        self.register[operand_a] = operand_b

    def op_PRN(self, operand_a, operand_b):
        '''
        TODO: Step 6: Add the PRN instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        '''
        print(self.register[operand_a])

    def op_MUL(self, operand_a, operand_b):
        '''
        TODO: Step 8: Implement a Multiply and Print the Result
        MUL is the responsiblity of the ALU, so it would be nice if your code eventually called the alu() function with appropriate arguments to get the work done.
        '''
        self.alu("MUL", operand_a, operand_b)
