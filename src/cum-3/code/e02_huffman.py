"""E02 — Huffman: ghép hai nút có tần suất thấp nhất."""

from collections import Counter
from heapq import heapify, heappop, heappush

from demo_io import brief, get_symbols, read_symbols, restore_symbols, run, symbol_label


def build_tree(symbols):
    counts = Counter(symbols)
    queue = [(counts[symbol], order, (symbol, None, None))
             for order, symbol in enumerate(sorted(counts))]
    if not queue:
        return None, counts, []
    heapify(queue)
    order = len(queue)
    merges = []
    while len(queue) > 1:
        a, _, left = heappop(queue)
        b, _, right = heappop(queue)
        heappush(queue, (a + b, order, (None, left, right)))
        merges.append((a, b, a + b))
        order += 1
    return queue[0][2], counts, merges


def code_table(tree):
    table = {}

    def visit(node, prefix):
        symbol, left, right = node
        if left is None:
            table[symbol] = prefix or "0"
        else:
            visit(left, prefix + "0")
            visit(right, prefix + "1")

    if tree is not None:
        visit(tree, "")
    return table


def encode(symbols, table):
    return "".join(table[symbol] for symbol in symbols)


def decode(bits, tree):
    if tree is None or tree[1] is None:
        if not bits:
            return []
        if tree is None or any(bit != "0" for bit in bits):
            raise ValueError("Bitstream không khớp cây Huffman")
        return [tree[0]] * len(bits)
    node = tree
    symbols = []
    for bit in bits:
        if bit not in "01":
            raise ValueError("Mã Huffman chỉ chứa bit 0 và 1")
        node = node[1 if bit == "0" else 2]
        if node[1] is None:
            symbols.append(node[0])
            node = tree
    if node is not tree:
        raise ValueError("Bitstream kết thúc giữa một từ mã")
    return symbols


def demo(data, folder):
    symbols = get_symbols(data)
    tree, counts, merges = build_tree(symbols)
    table = code_table(tree)
    bits = encode(symbols, table)
    decoded = decode(bits, tree)
    restore_symbols(folder, data, decoded)
    return {"symbols": brief([symbol_label(s) for s in symbols]),
            "table": [{"symbol": symbol_label(s), "count": counts[s], "code": table[s]}
                      for s in sorted(counts)],
            "merges": brief(merges), "bits": brief(bits, 512),
            "payload_bits": len(bits), "round_trip": symbols == decoded}


if __name__ == "__main__":
    run("e02", __doc__, {"symbols": list("AAAAABBCD")}, demo, read_symbols)
