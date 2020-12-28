"""
f is an ackermann-type function, satisfying
f(0, b, R) = b + 1
f(a, 0, R) = f(a - 1, R, R) for a != 0
f(a, b, R) = f(a - 1, f(a, b - 1, R), R) for a != 0 and b != 0

We seek R s.t. f(4, 1, R) = 6 (mod 2^15)

It can be shown (by induction) that
f(3, b, R) = (R + 1)^b * (R^2 + 3R + 1) + (2R + 1) * ((R + 1)^(b-1) + (R + 1)^(b-2) + ... + 1)
and hence f(4, 1, R) = f(3, f(4, 0, R), R)
                     = f(3, f(3, R, R), R)
"""
from tqdm import trange


MOD = 2 ** 15


def f3(b, R):
    """Returns val of f(3, b, R) % (2 ** 15)"""
    term1 = pow(R + 1, b, MOD) * (R * R + 3 * R + 1)
    term2 = 0
    for _ in range(b):
        term2 = ((R + 1) * term2 + 1) % MOD
    term2 *= 2 * R + 1
    return (term1 + term2) % MOD


def f41(R):
    """Returns val of f(4, 1, R) % (2 ** 15)"""
    return f3(f3(R, R), R) % MOD


def main():
    for R in trange(1, MOD):
        if f41(R) == 6:
            print(R)
            break


if __name__ == "__main__":
    main()
