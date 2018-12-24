import re


def get_data():
    with open('./input', 'rt') as f:
        values = [line.strip() for line in f.readlines()]
    return values


class Processor:
    _RE_IP_PRAGMA = re.compile(r"^#ip\s(?P<reg>\d+)$")
    _RE_INSTRUCTION = re.compile(r"(?P<op>[a-z]+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)\s*")
    _REGISTER_NUMBER = 6

    def __init__(self, registers=None):
        regs = registers or [0] * self._REGISTER_NUMBER
        self.registers = [r for r in regs]
        self.init_program_memory()

    def init_program_memory(self):
        self.instruction_pointer = 0
        self.instruction_pointer_bound_to_reg = None
        self.program_memory = []

    def set_state(self, registers):
        if len(registers) != self._REGISTER_NUMBER:
            raise ValueError
        self.registers = registers

    def get_register_value(self, reg):
        return self.registers[reg]

    def set_register_value(self, reg, value):
        self.registers[reg] = value

    def test_register_state(self, state):
        return all(a == b for a, b in zip(self.registers, state))

    def execute_instruction(self):
        if self.instruction_pointer_bound_to_reg is not None:
            self.set_register_value(self.instruction_pointer_bound_to_reg, self.instruction_pointer)

        # print(f"ip={self.instruction_pointer} {self.registers} ", end="")
        op, a, b, c = self.program_memory[self.instruction_pointer]
        getattr(self, op)(a, b, c)
        # print(f"{op} {a} {b} {c} {self.registers}")

        if self.instruction_pointer_bound_to_reg is not None:
            self.instruction_pointer = self.get_register_value(self.instruction_pointer_bound_to_reg)
        # Point to next instruction
        self.instruction_pointer += 1

    def run(self):
        program_size = len(self.program_memory)
        print(f"Instruction Pointer bound to register: {self.instruction_pointer_bound_to_reg}")
        print(f"Running assembly program:")
        [print(f"{i:03} - {v[0]} {v[1]} {v[2]} {v[3]}") for i, v in enumerate(self.program_memory)]

        while self.instruction_pointer < program_size:
            self.execute_instruction()

    def load_program(self, program):
        self.init_program_memory()

        for line in program:
            m = self._RE_INSTRUCTION.match(line)
            if m:
                op = m.group('op')
                a = int(m.group('a'))
                b = int(m.group('b'))
                c = int(m.group('c'))
                self.program_memory.append((op, a, b, c))
            m = self._RE_IP_PRAGMA.match(line)
            if m:
                self.instruction_pointer_bound_to_reg = int(m.group('reg'))

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = 1 if a > self.registers[b] else 0

    def gtri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > b else 0

    def gtrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] > self.registers[b] else 0

    def eqir(self, a, b, c):
        self.registers[c] = 1 if a == self.registers[b] else 0

    def eqri(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == b else 0

    def eqrr(self, a, b, c):
        self.registers[c] = 1 if self.registers[a] == self.registers[b] else 0


def solve():
    data = get_data()

    # Part 1
    processor = Processor()
    processor.load_program(data)
    processor.run()
    reg0_value = processor.get_register_value(0)
    print(f"Part1 - The value left in register 0 after programs halts is: {reg0_value}")

    # Part 2
    processor = Processor()
    processor.set_register_value(0, 1)
    processor.set_register_value(0, 1)
    processor.load_program(data)
    processor.program_memory.pop()
    processor.run()
    reg1_value = processor.get_register_value(1)
    r0 = 0
    for i in range(1, reg1_value+1):
        d, m = divmod(reg1_value, i)
        if m == 0:
            r0 += d

    print(f"Part2 - The value left in register 0 after programs halts is: {r0}")


if __name__ == "__main__":
    solve()
