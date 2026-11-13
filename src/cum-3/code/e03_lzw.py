"""E03 — LZW: dựng từ điển cụm ký hiệu trong lúc đọc."""

from demo_io import brief, get_symbols, read_symbols, restore_symbols, run, symbol_label


def encode(symbols, alphabet):
    dictionary = {(symbol,): i for i, symbol in enumerate(alphabet)}
    codes, added = [], []
    current = ()
    for symbol in symbols:
        extended = current + (symbol,)
        if extended in dictionary:
            current = extended
        else:
            codes.append(dictionary[current])
            dictionary[extended] = len(dictionary)
            added.append(extended)
            current = (symbol,)
    if current:
        codes.append(dictionary[current])
    return codes, added


def decode(codes, alphabet):
    if not codes:
        return []
    dictionary = [(symbol,) for symbol in alphabet]
    if not 0 <= codes[0] < len(dictionary):
        raise ValueError("Mã đầu phải có trong từ điển gốc")
    previous = dictionary[codes[0]]
    output = list(previous)
    for code in codes[1:]:
        if 0 <= code < len(dictionary):
            entry = dictionary[code]
        elif code == len(dictionary):
            entry = previous + previous[:1]
        else:
            raise ValueError("Mã LZW ngoài phạm vi từ điển")
        output.extend(entry)
        dictionary.append(previous + entry[:1])
        previous = entry
    return output


def demo(data, folder):
    symbols = get_symbols(data)
    if "alphabet" in data:
        alphabet = [tuple(x) if isinstance(x, list) else x for x in data["alphabet"]]
    elif "bytes" in data:
        alphabet = list(range(256))
    else:
        alphabet = sorted(set(symbols))
    if len(set(alphabet)) != len(alphabet) or not set(symbols).issubset(alphabet):
        raise ValueError("Từ điển gốc phải chứa đủ các ký hiệu và không trùng")
    codes, added = encode(symbols, alphabet)
    decoded = decode(codes, alphabet)
    restore_symbols(folder, data, decoded)
    return {"symbols": brief([symbol_label(s) for s in symbols]),
            "alphabet": brief([symbol_label(s) for s in alphabet]),
            "added": brief([{"code": i + len(alphabet), "entry": [symbol_label(s) for s in entry]}
                            for i, entry in enumerate(added)]),
            "codes": brief(codes), "code_count": len(codes),
            "decoded": brief([symbol_label(s) for s in decoded]),
            "round_trip": symbols == decoded}


if __name__ == "__main__":
    run("e03", __doc__, {"symbols": list("ABABABA"), "alphabet": ["A", "B"]}, demo, read_symbols)
