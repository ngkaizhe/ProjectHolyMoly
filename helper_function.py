from math import log2


def getLargestNumberOfLog2(max_number: int) -> int:
    # base case
    if max_number <= 0:
        return 0

    if log2(max_number) == int(log2(max_number)):
        return max_number

    return pow(2, int(log2(max_number)))
