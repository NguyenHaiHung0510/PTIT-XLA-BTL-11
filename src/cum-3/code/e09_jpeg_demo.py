"""E09 — Demo JPEG ảnh xám: DCT, lượng tử, zig-zag, DPCM/RLE, Huffman."""

from math import sqrt

from demo_io import flat, png, read_gray, run, size
from e02_huffman import build_tree, code_table, decode as huffman_decode, encode as huffman_encode
from e04_dct import dct, idct, display
from e05_quantize import LUMA, dequantize, nearest, quantize
from e06_zigzag import restore, scan
from e07_dpcm import decode as dc_decode, encode as dc_encode
from e08_ac_rle import decode as ac_decode, encode as ac_encode

BLOCK = 8


def blocks_from(pixels):
    width, height = size(pixels)
    positions, blocks = [], []
    for y in range(0, height, BLOCK):
        for x in range(0, width, BLOCK):
            positions.append((x, y))
            # Lặp pixel sát biên để đủ 8x8; cắt phần đệm khi ghép lại.
            blocks.append([[pixels[min(y + r, height - 1)][min(x + c, width - 1)] - 128
                            for c in range(BLOCK)] for r in range(BLOCK)])
    return positions, blocks


def entropy_encode(vectors):
    dc_differences = dc_encode([vector[0] for vector in vectors])
    ac_pairs = [ac_encode(vector[1:]) for vector in vectors]
    # Ký hiệu 0 là DC. Ký hiệu 1 là một cặp AC; DC kế tiếp bắt đầu block mới.
    symbols = []
    for difference, pairs in zip(dc_differences, ac_pairs):
        symbols.append((0, difference))
        symbols.extend((1, skip, value) for skip, value in pairs)
    tree, _, _ = build_tree(symbols)
    bits = huffman_encode(symbols, code_table(tree))
    return tree, bits, dc_differences, ac_pairs


def entropy_decode(tree, bits):
    differences, pairs = [], []
    for kind, *payload in huffman_decode(bits, tree):
        if kind == 0:
            differences.append(payload[0])
            pairs.append([])
        else:
            pairs[-1].append(tuple(payload))
    return [[dc] + ac_decode(encoded, BLOCK * BLOCK - 1)
            for dc, encoded in zip(dc_decode(differences), pairs)]


def reconstruct(positions, vectors, width, height):
    pixels = [[0] * width for _ in range(height)]
    for (x, y), vector in zip(positions, vectors):
        coefficients = dequantize(restore(vector, BLOCK, BLOCK), LUMA)
        block = idct(coefficients)
        for r in range(min(BLOCK, height - y)):
            for c in range(min(BLOCK, width - x)):
                pixels[y + r][x + c] = max(0, min(255, nearest(block[r][c] + 128)))
    return pixels


def demo(pixels, folder):
    width, height = size(pixels)
    positions, blocks = blocks_from(pixels)
    coefficients = [dct(block) for block in blocks]
    quantized = [quantize(block, LUMA) for block in coefficients]
    vectors = [scan(block) for block in quantized]
    tree, bits, differences, pairs = entropy_encode(vectors)
    decoded = entropy_decode(tree, bits)
    reconstructed = reconstruct(positions, decoded, width, height)
    errors = [abs(a - b) for a, b in zip(flat(pixels), flat(reconstructed))]
    png(folder / "input.png", pixels)
    png(folder / "reconstructed.png", reconstructed)
    return {"size": [width, height],
            "padded_size": [((width + 7) // 8) * 8, ((height + 7) // 8) * 8],
            "blocks": len(blocks), "quantized_round_trip": decoded == vectors,
            "payload_bits": len(bits), "raw_pixel_bits": width * height * 8,
            "mae": sum(errors) / len(errors),
            "rmse": sqrt(sum(e * e for e in errors) / len(errors)), "max_error": max(errors),
            "first_block": {"level_shifted": blocks[0], "dct": display(coefficients[0]),
                            "quantized": quantized[0], "zigzag": vectors[0],
                            "dc_difference": differences[0], "ac_rle": pairs[0]}}


if __name__ == "__main__":
    tiny = [[48 + 12 * x + 3 * y for x in range(16)] for y in range(8)]
    run("e09", __doc__, tiny, demo, read_gray)
