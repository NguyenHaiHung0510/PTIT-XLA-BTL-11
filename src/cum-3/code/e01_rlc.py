"""E01 — Run-length coding: lưu (độ dài, ký hiệu) theo từng hàng."""

from demo_io import brief, png, read_symbols, run, size


def encode_row(row):
    runs = []
    for value in row:
        if runs and runs[-1][1] == value:
            count, _ = runs[-1]
            runs[-1] = (count + 1, value)
        else:
            runs.append((1, value))
    return runs


def decode_row(runs):
    return [value for count, value in runs for _ in range(count)]


def demo(data, folder):
    rows = data["pixels"] if "pixels" in data else [data.get("bytes", data.get("symbols", []))]
    if "pixels" in data:
        size(rows)
    runs = [encode_row(row) for row in rows]
    decoded = [decode_row(row) for row in runs]
    if "pixels" in data:
        png(folder / "decoded.png", decoded)
    elif "bytes" in data:
        (folder / "decoded.bin").write_bytes(bytes(decoded[0]))
    return {"input_rows": brief([brief(row) for row in rows], 4),
            "runs": brief([brief(row) for row in runs], 4),
            "run_count": sum(map(len, runs)), "symbol_count": sum(map(len, rows)),
            "round_trip": rows == decoded}


if __name__ == "__main__":
    run("e01", __doc__, {"pixels": [[4, 4, 4, 8], [8, 8, 1, 1]]}, demo, read_symbols)
