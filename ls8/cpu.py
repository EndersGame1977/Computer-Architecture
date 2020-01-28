"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # TODO: Step 1: Add the constructor to cpu.py
        # Add list properties to the CPU class to hold 256 bytes of memory.
        self.ram = [0] * 256
        # Add list properties to the CPU class to hold 8 gneneral-purpose registers.
        self.register = [0] * 8
        # Also add properties for any internal registers
        self.pc = 0
        # TODO: Step 10: Implement System Stack
        # stack pointer
        # The self.sp points at the value at the top of the stack (most recently pushed), or at address `F4` if the stack is empty.
        self.sp = 7
        # TODO: Step 3: Implement the core of CPU's run() method
        # Used in the handle_HLT() to stop the while loop in the run()
        self.isPaused = False
        # TODO: Step 10: Implement System Stack
        # Keyboard interrupt. This interrupt triggers when a key is pressed. The value of the key pressed is stored in address 0xF4
        self.register[self.sp] = 0xf4
        # TODO: Step 9: Beautify your run() loop
        # Add the HLT instruction definition to cpu.py so that you can refer to it by name instead of by numeric value.
        # Set up the branch table
        self.branchtable = {
            # TODO: Step 4: Implement the HLT instruction handler
            0b00000001: self.HLT,
            # TODO: Step 5: Add the LDI instruction
            0b10000010: self.LDI,
            # TODO: Step 6: Add the PRN instruction
            0b01000111: self.PRN,
            # TODO: Step 8: Implement a Multiply and Print the Result
            0b10100010: self.MUL,
            # TODO: Step 10: Implement System Stack
            0b10100000: self.ADD,
            0b01000101: self.PUSH,
            # TODO: Step 11: Implement Subroutine Calls
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET
        }

    # TODO: Step 10: Implement System Stack
    def stack_push(self, value):
        ''' Push the value in the given register on the stack. '''
        # Decrement the self.sp
        self.register[self.sp] -= 1
        # Copy the value in the given register to the address pointed to by self.sp
        self.ram_write(self.register[self.sp], value)

    # TODO: Step 10: Implement System Stack
    def stack_pop(self):
        ''' Pop the value at the top of the stack into the given register. '''
        # Copy the value from the address pointed to by self.sp to the given register.
        value = self.ram_read(self.register[self.sp])
        # Increment self.sp
        self.register[self.sp] += 1
        return value

    # TODO: Step 2: Add RAM funcions
    def ram_read(self, address):
        '''
        In CPU, add method ram_read() that access the RAM inside the CPU object.
        Should accept the address to read and return the value stored there
        '''
        return self.ram[address]

    # TODO: Step 2: Add RAM funcions
    def ram_write(self, address, value):
        '''
        In CPU, add method ram_write() that access the RAM inside the CPU object.
        Should accept a value to write, and the address to write it to
        '''
        self.ram[address] = value

    # TODO: Step 7: Un-hardcode the machine code
    def load(self, filename):
        """Load a program into memory."""
        '''
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

        if op == "ADD":
            self.register[register_a] += self.register[register_b]

        # TODO: Step 8: Implement a Multiply and Print the Result
        elif op == "MUL":
            # Multiply the values in two registers together and store the result in registerA.
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

    # TODO: Step 3: Implement the core of CPU's run() method
    def run(self):
        """Run the CPU."""
        '''
        It needs to read the memory address that's stored in register PC, and store that result in IR, the Instruction Register.
        '''
        while not self.isPaused:

            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            # Depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec. Maybe an if-elif cascade...?
            if ir in self.branchtable:
                self.branchtable[ir](operand_a, operand_b)
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

    # TODO: Step 9: Beautify your run() loop
    # TODO: Step 4: Implement the HLT instruction handler
    def HLT(self, operand_a, operand_b):
        '''
        In run() in your switch, exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded. We can consider HLT to be similar to Python's exit() in that we stop whatever we are doing, wherever we are.
        '''
        self.isPaused = True

    # TODO: Step 5: Add the LDI instruction
    def LDI(self, operand_a, operand_b):
        '''
        Set the value of a register to an integer.
        '''
        self.register[operand_a] = operand_b

    # TODO: Step 6: Add the PRN instruction
    def PRN(self, operand_a, operand_b):
        '''
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        '''
        print(self.register[operand_a])

    # TODO: Step 8: Implement a Multiply and Print the Result
    def MUL(self, operand_a, operand_b):
        '''
        MUL is the responsiblity of the ALU, so it would be nice if your code eventually called the alu() function with appropriate arguments to get the work done
        '''
        self.alu("MUL", operand_a, operand_b)

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    # TODO: Step 10: Implement System Stack
    def PUSH(self, operand_a, operand_b):
        ''' Push the value in the given register on the stack. '''
        self.stack_push(self.register[operand_a])

    # TODO: Step 10: Implement System Stack
    def POP(self, operand_a, operand_b):
        ''' Pop the value at the top of the stack into the given register. '''
        self.register[operand_a] = self.stack_pop()

    # TODO: Step 11: Implement Subroutine Calls
    def CALL(self, operand_a, operand_b):
        ''' Calls a subroutine (function) at the address stored in the register. '''
        # The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        self.stack_push(self.pc + 2)
        # The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
        self.pc = self.register[operand_a]

    # TODO: Step 11: Implement Subroutine Calls
    def RET(self, operand_a, operand_b):
        ''' Return from subroutine. '''
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.stack_pop()
