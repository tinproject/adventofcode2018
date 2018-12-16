import re

RE_SAMPLE = re.compile(
    r"Before:\s+\[(?P<br0>\d+), (?P<br1>\d+), (?P<br2>\d+), (?P<br3>\d+)\]\s*\n"
    r"(?P<op>\d+) (?P<a>\d+) (?P<b>\d+) (?P<c>\d+)\s*\n"
    r"After:\s+\[(?P<r0>\d+), (?P<r1>\d+), (?P<r2>\d+), (?P<r3>\d+)\]\s*",
    re.MULTILINE
)
RE_INSTRUCTION = re.compile(r"^(?P<op>\d+), (?P<a>\d+), (?P<b>\d+), (?P<c>\d+)$")


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
    def __init__(self, registers=None):
        regs = registers or [0, 0, 0, 0]
        self.registers = [r for r in regs]

    def set_state(self, registers):
        if len(registers) != 4:
            raise ValueError
        self.registers = registers

    def test_register_state(self, state):
        return all(a == b for a, b in zip(self.registers, state))

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


def get_num_of_opcodes_sample_behaves_like(instruction, before, after):
    candidates = set()
    for opname in OpNames.all_opnames:
        if behaves_like(opname, instruction, before, after):
            candidates.add(opname)
    return len(candidates)


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


def solve():

    # Part 1
    samples = get_samples()
    number_of_samples = sum(1 for s in samples if get_num_of_opcodes_sample_behaves_like(*s) >= 3)
    print(f"Part1 - The number of samples that behave like three or more opcodes is: {number_of_samples}")

    # Part 2
    print(f"Part2 - ... is: {None}")


if __name__ == "__main__":
    solve()
