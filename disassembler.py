from computer import OPS, N_ARGS


def get_args(prog_file, n_args):
    for _ in range(n_args):
        val = int.from_bytes(prog_file.read(2), "little")
        if 0 <= val < 2 ** 15:
            yield str(val)
        elif 2 ** 15 <= val < 2 ** 15 + 8:
            yield f"R[{val - 2 ** 15}]"
        else:
            raise ValueError(f"Invalid arg {val}")


def gen_assembly(prog_file):
    mem_loc = 0
    while word := prog_file.read(2):
        opcode = int.from_bytes(word, "little")
        if 0 <= opcode < len(OPS):
            opname = OPS[opcode][1:]
            args = get_args(prog_file, N_ARGS[opcode])
            yield f"{mem_loc}\t{opname}\t" + ", ".join(args)
            mem_loc += N_ARGS[opcode] + 1
        else:
            yield f"{mem_loc}\t{opcode}"
            mem_loc += 1


def main():
    with open("challenge.bin", "br") as f:
        for line in gen_assembly(f):
            print(line)


if __name__ == "__main__":
    main()
