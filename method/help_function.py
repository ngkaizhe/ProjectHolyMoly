from math import log2, ceil, floor


def isPowerOf2(n: int) -> bool:
    if n == 0:
        return False

    return ceil(log2(n)) == floor(log2(n))
