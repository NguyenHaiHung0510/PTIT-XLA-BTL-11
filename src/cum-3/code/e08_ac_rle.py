"""E08 — RLE cho AC: (số 0 trước đó, hệ số khác 0), (0,0) là EOB."""

from demo_io import run

EOB = (0, 0)


def encode(ac):
    pairs = []
    zeros = 0
    for value in ac:
        if value == 0:
            zeros += 1
        else:
            pairs.append((zeros, value))
            zeros = 0
    if zeros:
        pairs.append(EOB)
    return pairs


def decode(pairs, length):
    ac = []
    for index, pair in enumerate(pairs):
        skip, value = pair
        if (skip, value) == EOB:
            if index != len(pairs) - 1 or len(ac) >= length:
                raise ValueError("EOB phải kết thúc một đuôi khác rỗng toàn 0")
            ac.extend([0] * (length - len(ac)))
            break
        if value == 0 or skip < 0 or len(ac) + skip >= length:
            raise ValueError("Cặp RLE AC không hợp lệ")
        ac.extend([0] * skip)
        ac.append(value)
    if len(ac) != length:
        raise ValueError("Thiếu hệ số AC")
    return ac


def demo(ac, folder):
    pairs = encode(ac)
    restored = decode(pairs, len(ac))
    return {"ac": ac, "pairs": pairs, "restored": restored, "round_trip": ac == restored}


if __name__ == "__main__":
    run("e08", __doc__, [0, 0, 5, 0, -2, 0, 0], demo)
