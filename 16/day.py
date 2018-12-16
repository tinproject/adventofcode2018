import re


RE_SAMPLE = re.compile(
    r"Before:\s+\[(?P<br0>\d+), (?P<br1>\d+), (?P<br2>\d+), (?P<br3>\d+)\]\s*\n"
    r"(?P<op>\d+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)\s*\n"
    r"After:\s+\[(?P<r0>\d+), (?P<r1>\d+), (?P<r2>\d+), (?P<r3>\d+)\]\s*",
    re.MULTILINE
)
RE_INSTRUCTION = re.compile(r"\n\n((?P<instruction>\d+ \d+ \d+ \d+)\s*\n)+")


class OpNames:
    all_opnames = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
                   'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr', ]
    addr = 'addr'
    addi = 'addi'
    mulr = 'mulr'
    muli = 'muli'
    banr = 'banr'
    bani = 'bani'
    borr = 'borr'
    bori = 'bori'
    setr = 'setr'
    seti = 'seti'
    gtir = 'gtir'
    gtri = 'gtri'
    gtrr = 'gtrr'
    eqir = 'eqir'
    eqri = 'eqri'
    eqrr = 'eqrr'


class Processor:
    def __init__(self, registers=None, opcode_table=None):
        regs = registers or [0, 0, 0, 0]
        self.registers = [r for r in regs]
        self.opcode_table = dict() if not opcode_table else {k: v for k, v in opcode_table.items()}

    def set_state(self, registers):
        if len(registers) != 4:
            raise ValueError
        self.registers = registers

    def test_register_state(self, state):
        return all(a == b for a, b in zip(self.registers, state))

    def execute_instruction(self, op, a, b, c):
        if op not in self.opcode_table:
            print(op, a, b, c, self.opcode_table)
            raise ValueError(f"Unkown operation: {op}")
        opname = self.opcode_table[op]
        getattr(self, opname)(a, b, c)

    def run_program(self, program):
        for instruction in program:
            self.execute_instruction(*instruction)

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


def behaves_like(opname, instruction, before, after):
    processor = Processor(before)
    getattr(processor, opname)(*instruction[1:])

    return processor.test_register_state(after)


def get_opnames_sample_behaves_like(instruction, before, after):
    candidates = set()
    for opname in OpNames.all_opnames:
        if behaves_like(opname, instruction, before, after):
            candidates.add(opname)
    return candidates


def get_num_of_opcodes_sample_behaves_like(instruction, before, after):
    return len(get_opnames_sample_behaves_like(instruction, before, after))


def get_samples():
    with open('./input', 'rt') as f:
        data = f.read()

    samples = []
    for s in RE_SAMPLE.finditer(data):
        sample = (
            tuple(int(s[k]) for k in ['op', 'a', 'b', 'c']),
            tuple(int(s[k]) for k in ['br0', 'br1', 'br2', 'br3']),
            tuple(int(s[k]) for k in ['r0', 'r1', 'r2', 'r3']),
        )
        samples.append(sample)
    return samples


def get_program():
    with open('./input', 'rt') as f:
        data = f.read()
    program = data[data.find("\n\n\n"):]

    instructions = []
    for line in program.splitlines():
        if line:
            instruction = tuple(int(v.strip()) for v in line.strip().split(' ') if v)
            instructions.append(instruction)
    return instructions


def get_opcode_opname_translation(samples):
    opcodes = {}

    # get unique samples behave like for opcode
    samples_opnames = list(set((s[0][0], tuple(sorted(get_opnames_sample_behaves_like(*s)))) for s in samples))
    samples_opnames = [(s[0], set(s[1])) for s in samples_opnames]

    while len(opcodes) < 16:
        for s in sorted(samples_opnames, key=lambda x: len(x[1])):
            opcode = s[0]
            opnames = s[1]
            num_opnames = len(opnames)
            if num_opnames == 1:
                # direct association
                opcodes[opnames.pop()] = opcode
                samples_opnames.remove(s)
            elif num_opnames > 1:
                for opname in list(opnames):
                    if opname in opcodes:
                        opnames.remove(opname)

    return {v: k for k, v in opcodes.items()}


def solve():

    # Part 1
    samples = get_samples()
    number_of_samples = sum(1 for s in samples if get_num_of_opcodes_sample_behaves_like(*s) >= 3)

    print(f"Part1 - The number of samples that behave like three or more opcodes is: {number_of_samples}")

    # Part 2
    opcode_table = get_opcode_opname_translation(samples)
    program = get_program()
    processor = Processor(opcode_table=opcode_table)
    processor.run_program(program)

    value_at_reg0 = processor.registers[0]
    print(f"Part2 - The value at register 0 after executing the test program is: {value_at_reg0}")


if __name__ == "__main__":
    solve()
