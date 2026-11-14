"""E07 — DPCM: lưu độ chênh DC so với block trước."""

from demo_io import brief, run


def encode(values):
    previous = 0
    differences = []
    for dc in values:
        differences.append(dc - previous)
        previous = dc
    return differences


def decode(differences):
    previous = 0
    values = []
    for difference in differences:
        previous += difference
        values.append(previous)
    return values


def demo(values, folder):
    differences = encode(values)
    restored = decode(differences)
    return {"dc": brief(values), "differences": brief(differences),
            "restored": brief(restored), "round_trip": values == restored}


if __name__ == "__main__":
    run("e07", __doc__, [45, 54, 48], demo)
