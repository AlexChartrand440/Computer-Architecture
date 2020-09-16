"""CPU functionality."""

import sys;

# 1 2 4 8 16 32 64 128

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8;
        self.ram = [0] * 255;
        self.running = True;
        self.pc = 0;

    def load(self):
        """Load a program into memory."""

        address = 0;

        if len(sys.argv) < 2:
            print('No program specified to load!');
            return;

        try:
            print(sys.argv[1]);
            with open(sys.argv[1]) as f:
                for line in f:
                    temp = line.split('#');
                    trimmed = temp[0].strip();
                    if len(trimmed) > 0 and len(trimmed) == 8:
                        # print(int(trimmed, 2));
                        self.ram[address] = int(trimmed, 2);
                        address += 1;
        except:
            print('Error loading program: ' + sys.argv[1]);

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b];
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""  
        while self.running:

            opcode = self.ram[self.pc];

            if opcode == 130: # Save to REG
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2];
                self.pc += 3;
            elif opcode == 71: # Print REG
                print(self.reg[self.ram[self.pc + 1]]);
                self.pc += 2;
            elif opcode == 162: # Multiply REG's
                print('REG: ' + str(self.reg[self.ram[self.pc + 1]]));
                print('REG: ' + str(self.reg[self.ram[self.pc + 2]]));
                self.alu('MULT', self.ram[self.pc + 1], self.ram[self.pc + 2]);
                self.pc += 3;
            elif opcode == 1: # Halt/Stop
                self.running = False;
