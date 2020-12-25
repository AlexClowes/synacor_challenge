from enum import Enum
import sys


OPS = [
    "halt",
    "set",
    "push",
    "pop",
    "eq",
    "gt",
    "jmp",
    "jt",
    "jf",
    "add",
    "mult",
    "mod",
    "and_",
    "or_",
    "not_",
    "rmem",
    "wmem",
    "call",
    "ret",
    "out",
    "in_",
    "noop",
]
N_ARGS = [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0]


class Status(Enum):
    OK = 0
    HALT = 1


class Registers(dict):
    def __getitem__(self, key):
        if 2 ** 15 <= key < 2 ** 15 + 8:
            return super().__getitem__(key)
        raise ValueError

    def __setitem__(self, key, val):
        if 2 ** 15 <= key < 2 ** 15 + 8:
            super().__setitem__(key, val)
        else:
            raise ValueError


class Computer:
    def __init__(self):
        self.registers = Registers({k: 0 for k in range(2 ** 15, 2 ** 15 + 8)})
        self.memory = [0] * 2 ** 15
        self.instr_ptr = 0
        self.stack = []
        self.status = Status.OK

    def load_prog(self, prog_loc):
        mem_ptr = 0
        with open(prog_loc, mode="br") as f:
            while (prog_word := f.read(2)):
                val = int.from_bytes(prog_word, "little")
                self.memory[mem_ptr] = val
                mem_ptr += 1

    def run(self, prog_loc):
        self.load_prog(prog_loc)
        while self.status == Status.OK:
            opcode = self.memory[self.instr_ptr]
            operation = OPS[opcode]
            n_args = N_ARGS[opcode]
            self.instr_ptr += 1
            args = self.memory[self.instr_ptr : self.instr_ptr + n_args]
            self.instr_ptr += n_args
            getattr(self, operation)(*args)
        if self.status != Status.HALT:
            raise ValueError(f"Program exited with status code {self.status}")

    def _get_val(self, x):
        if 0 <= x < 2 ** 15:
            return x
        elif 2 ** 15 <= x < 2 ** 15 + 8:
            return self.registers[x]
        else:
            raise ValueError(f"Invalid number {x}")

    def halt(self):
        self.status = Status.HALT

    def set(self, a, b):
        self.registers[a] = self._get_val(b)

    def push(self, a):
        self.stack.append(self._get_val(a))

    def pop(self, a):
        self.registers[a] = self.stack.pop()

    def eq(self, a, b, c):
        self.registers[a] = int(self._get_val(b) == self._get_val(c))

    def gt(self, a, b, c):
        self.registers[a] = int(self._get_val(b) > self._get_val(c))

    def jmp(self, a):
        self.instr_ptr = self._get_val(a)

    def jt(self, a, b):
        if self._get_val(a) != 0:
            self.instr_ptr = self._get_val(b)

    def jf(self, a, b):
        if self._get_val(a) == 0:
            self.instr_ptr = self._get_val(b)

    def add(self, a, b, c):
        self.registers[a] = (self._get_val(b) + self._get_val(c)) % (2 ** 15)

    def mult(self, a, b, c):
        self.registers[a] = (self._get_val(b) * self._get_val(c)) % (2 ** 15)

    def mod(self, a, b, c):
        self.registers[a] = self._get_val(b) % self._get_val(c)

    def and_(self, a, b, c):
        self.registers[a] = self._get_val(b) & self._get_val(c)

    def or_(self, a, b, c):
        self.registers[a] = self._get_val(b) | self._get_val(c)

    def not_(self, a, b):
        self.registers[a] = 2 ** 15 - 1 - self._get_val(b)

    def rmem(self, a, b):
        self.registers[a] = self.memory[self._get_val(b)]

    def wmem(self, a, b):
        self.memory[self._get_val(a)] = self._get_val(b)

    def call(self, a):
        self.push(self.instr_ptr)
        self.instr_ptr = self._get_val(a)

    def ret(self):
        if self.stack:
            self.instr_ptr = self.stack.pop()
        else:
            self.status = Status.HALT

    def out(self, a):
        sys.stdout.write(chr(self._get_val(a)))

    def in_(self, a):
        self.registers[a] = ord(sys.stdin.read(1))

    def noop(self):
        pass


def main():
    c = Computer()
    c.run("challenge.bin")


if __name__ == "__main__":
    main()
