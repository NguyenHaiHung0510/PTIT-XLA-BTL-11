"""Đọc mẫu, ghi kết quả; thuật toán nằm trong từng bài."""

import argparse
import json
from pathlib import Path
import re
from struct import pack
import zlib


def run(code, title, tiny, demo, read=None):
    parser = argparse.ArgumentParser(description=title)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("input", nargs="?", type=Path, help="Đường dẫn input")
    source.add_argument("--tiny", action="store_true", help="Chạy mẫu có sẵn")
    args = parser.parse_args()
    try:
        data = tiny if args.tiny else (read or read_json)(args.input)
        sample = "tiny" if args.tiny else args.input.stem
        folder = result_folder(code, sample)
        report = demo(data, folder)
        (folder / "result.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(2, f"Lỗi: {exc}\n")
    print(f"Kết quả: {folder}")


def result_folder(code, sample):
    root = Path(__file__).resolve().parents[1] / "output" / code
    root.mkdir(parents=True, exist_ok=True)
    sample = re.sub(r"[^\w-]+", "-", sample).strip("-") or "input"
    number = 1
    while True:
        path = root / f"{sample}-{number:02}"
        try:
            path.mkdir()
            return path
        except FileExistsError:
            number += 1


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_image(path, mode="L"):
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError("Đọc ảnh: cài Pillow bằng python -m pip install Pillow") from exc
    with Image.open(path) as source:
        img = source.convert(mode)
        values = list(img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata())
        return [values[i:i + img.width] for i in range(0, len(values), img.width)]


def read_gray(path):
    return read_json(path) if path.suffix.lower() == ".json" else read_image(path)


def size(rows):
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("Cần ma trận chữ nhật không rỗng")
    return len(rows[0]), len(rows)


def flat(rows):
    return [value for row in rows for value in row]


def brief(values, limit=64):
    if len(values) <= limit:
        return values
    return {"length": len(values), "first": values[:limit]}


def png(path, pixels, rgb=False):
    # PNG 8 bit, filter 0; chỉ để ghi ảnh demo mà không cần cài thư viện.
    width, height = size(pixels)

    def chunk(kind, data):
        return pack(">I", len(data)) + kind + data + pack(">I", zlib.crc32(kind + data))

    raw = b"".join(b"\0" + bytes(flat(row) if rgb else row) for row in pixels)
    header = pack(">2I5B", width, height, 8, 2 if rgb else 0, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def blocked_symbols(rows, block):
    width, height = size(rows)
    bh, bw = block
    if bh < 1 or bw < 1 or height % bh or width % bw:
        raise ValueError("Kích thước ảnh phải chia hết cho kích thước block")
    return [tuple(rows[y + r][x + c] for r in range(bh) for c in range(bw))
            for y in range(0, height, bh) for x in range(0, width, bw)]


def restore_blocks(symbols, width, height, block):
    bh, bw = block
    rows = [[0] * width for _ in range(height)]
    blocks = iter(symbols)
    for y in range(0, height, bh):
        for x in range(0, width, bw):
            pixels = next(blocks)
            for r in range(bh):
                rows[y + r][x:x + bw] = pixels[r * bw:(r + 1) * bw]
    return rows


def read_symbols(path):
    if path.suffix.lower() == ".json":
        return read_json(path)
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".pgm", ".tif", ".tiff", ".webp", ".gif", ".ppm"}:
        return {"pixels": read_image(path), "block": [1, 1]}
    return {"bytes": list(path.read_bytes())}


def get_symbols(data):
    if "pixels" in data:
        rows = data["pixels"]
        block = data.get("block", [1, 1])
        return blocked_symbols(rows, block)
    return list(data.get("bytes", data.get("symbols", [])))


def restore_symbols(folder, data, symbols):
    if "pixels" in data:
        width, height = size(data["pixels"])
        pixels = restore_blocks(symbols, width, height, data.get("block", [1, 1]))
        png(folder / "decoded.png", pixels)
        if max(flat(pixels)) <= 1:
            png(folder / "binary-preview.png", [[v * 255 for v in row] for row in pixels])
    elif "bytes" in data:
        (folder / "decoded.bin").write_bytes(bytes(symbols))


def symbol_label(symbol):
    if isinstance(symbol, tuple):
        if all(value in (0, 1) for value in symbol):
            return "".join(map(str, symbol))
        return ",".join(map(str, symbol))
    return symbol
