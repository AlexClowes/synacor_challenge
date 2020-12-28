from enum import Enum
import sys


OPS = [
    "_halt",
    "_set",
    "_push",
    "_pop",
    "_eq",
    "_gt",
    "_jmp",
    "_jt",
    "_jf",
    "_add",
    "_mult",
    "_mod",
    "_and",
    "_or",
    "_not",
    "_rmem",
    "_wmem",
    "_call",
    "_ret",
    "_out",
    "_in",
    "_noop",
]
N_ARGS = [0, 2, 1, 1, 3, 3, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 1, 0, 1, 1, 0]


class Status(Enum):
    OK = 0
    HALT = 1


class Registers(dict):
    def __getitem__(self, key):
        if 2 ** 15 <= key < 2 ** 15 + 8:
            return super().__getitem__(key)
        raise ValueError(f"Invalid register {key}")

    def __setitem__(self, key, val):
        if 2 ** 15 <= key < 2 ** 15 + 8:
            super().__setitem__(key, val)
        else:
            raise ValueError(f"Invalid register {key}")


class Computer:
    def __init__(self, file_in=sys.stdin):
        self.registers = Registers({k: 0 for k in range(2 ** 15, 2 ** 15 + 8)})
        self.memory = [0] * 2 ** 15
        self.instr_ptr = 0
        self.stack = []
        self.status = Status.OK

        self.file_in = file_in

    def load_prog(self, prog_loc):
        mem_ptr = 0
        with open(prog_loc, mode="br") as f:
            while prog_word := f.read(2):
                self.memory[mem_ptr] = int.from_bytes(prog_word, "little")
                mem_ptr += 1

    def run(self, prog_loc, extra_actions):
        self.load_prog(prog_loc)
        while self.status == Status.OK:
            if self.instr_ptr in extra_actions:
                extra_actions[self.instr_ptr](self)
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

    def _halt(self):
        self.status = Status.HALT

    def _set(self, a, b):
        self.registers[a] = self._get_val(b)

    def _push(self, a):
        self.stack.append(self._get_val(a))

    def _pop(self, a):
        self.registers[a] = self.stack.pop()

    def _eq(self, a, b, c):
        self.registers[a] = int(self._get_val(b) == self._get_val(c))

    def _gt(self, a, b, c):
        self.registers[a] = int(self._get_val(b) > self._get_val(c))

    def _jmp(self, a):
        self.instr_ptr = self._get_val(a)

    def _jt(self, a, b):
        if self._get_val(a) != 0:
            self.instr_ptr = self._get_val(b)

    def _jf(self, a, b):
        if self._get_val(a) == 0:
            self.instr_ptr = self._get_val(b)

    def _add(self, a, b, c):
        self.registers[a] = (self._get_val(b) + self._get_val(c)) % (2 ** 15)

    def _mult(self, a, b, c):
        self.registers[a] = (self._get_val(b) * self._get_val(c)) % (2 ** 15)

    def _mod(self, a, b, c):
        self.registers[a] = self._get_val(b) % self._get_val(c)

    def _and(self, a, b, c):
        self.registers[a] = self._get_val(b) & self._get_val(c)

    def _or(self, a, b, c):
        self.registers[a] = self._get_val(b) | self._get_val(c)

    def _not(self, a, b):
        self.registers[a] = 2 ** 15 - 1 - self._get_val(b)

    def _rmem(self, a, b):
        self.registers[a] = self.memory[self._get_val(b)]

    def _wmem(self, a, b):
        self.memory[self._get_val(a)] = self._get_val(b)

    def _call(self, a):
        self.stack.append(self.instr_ptr)
        self.instr_ptr = self._get_val(a)

    def _ret(self):
        if self.stack:
            self.instr_ptr = self.stack.pop()
        else:
            self.status = Status.HALT

    def _out(self, a):
        sys.stdout.write(chr(self._get_val(a)))

    def _in(self, a):
        if self.file_in is not sys.stdin and not self.file_in.peek(1):
            self.file_in = sys.stdin
        self.registers[a] = ord(self.file_in.read(1))

    def _noop(self):
        pass


def main():
    file_in = open(sys.argv[1], mode="br") if len(sys.argv) > 1 else sys.stdin
    c = Computer(file_in)

    def change_reg(reg, val):
        def setter(self):
            self.registers[2 ** 15 + reg] = val

        return setter

    def jump_to(address):
        def setter(self):
            self.memory[self.instr_ptr] = 6  # jmp
            self.memory[self.instr_ptr + 1] = address

        return setter

    extra_actions = {
        5451: change_reg(7, 25734),  # Change high register to correct value
        5489: jump_to(5491),  # Skip call to 6027
        5491: change_reg(0, 6),  # Register 0 would be 6 if call to 6027 had taken place
    }
    c.run("challenge.bin", extra_actions)


if __name__ == "__main__":
    main()
