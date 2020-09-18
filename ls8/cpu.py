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
        self.reg[7] = 0xF4;
        self.fl = 0;
        self.fg = 0;
        self.fe = 0;

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
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b];
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def pop(self):
        rn = self.ram[self.pc + 1];
        v = self.ram[self.reg[7]];
        self.reg[rn] = v;
        self.reg[7] += 1;
        self.pc += 2;
        print('Reg: ' + str(self.reg[7]) + ' | Value: ' + str(self.reg[rn]));
    
    def push(self):
        self.reg[7] -= 1;
        rn = self.ram[self.pc + 1];
        v = self.reg[rn];
        self.ram[self.reg[7]] = v;
        self.pc += 2;
        print('Reg: ' + str(self.reg[7]) + ' | Value: ' + str(self.ram[self.reg[7]]));

    def push_value(self, value):
        self.reg[7] -= 1;
        self.ram[self.reg[7]] = value;

    def pop_value(self):
        v = self.ram[self.reg[7]];
        self.reg[7] += 1;
        return v;

    def compare(self, regA, regB):
        if regA < regB:
            self.fl = 1;
        elif regA > regB:
            self.fg = 1;
        else:
            self.fe = 1;

    def reset(self):
        self.fl = 0;
        self.fg = 0;
        self.fe = 0;

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

            # self.trace();

            opcode = self.ram[self.pc];

            # print(str(opcode) + ' - ' + str(self.pc));

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
            elif opcode == 70: # POP
                self.pop();
            elif opcode == 69: # PUSH
                self.push();
            elif opcode == 80: # CALL
                self.push_value(self.pc + 2);
                self.pc = self.reg[self.ram[self.pc + 1]];
            elif opcode == 33: # RETURN
                pass;
            elif opcode == 167: # COMPARE
                self.reset();
                # SET FLAG
                self.compare(self.reg[self.ram[self.pc + 1]], self.reg[self.ram[self.pc + 2]]);
                self.pc += 3;
            elif opcode == 0b01010110: # JNE
                if self.fe == 0:
                    self.pc = self.reg[self.ram[self.pc + 1]];
                else:
                    self.pc += 2;
            elif opcode == 0b01010101: # JEQ
                if self.fe == 1:
                    self.pc = self.reg[self.ram[self.pc + 1]];
                else:
                    self.pc += 2;
            elif opcode == 0b01010100: # JMP
                self.pc = self.reg[self.ram[self.pc + 1]];
            elif opcode == 1: # Halt/Stop
                self.running = False;
