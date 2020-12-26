from itertools import permutations


def main():
    vals = (2, 3, 5, 7, 9)
    func = lambda a, b, c, d, e: a + b * c ** 2 + d ** 3 - e == 399
    for perm in permutations(vals):
        if func(*perm):
            print(perm)


if __name__ == "__main__":
    main()
