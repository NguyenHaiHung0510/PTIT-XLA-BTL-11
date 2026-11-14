"""H03 — Ordered dithering: so mức xám với ngưỡng lặp theo vị trí."""

from demo_io import flat, png, read_gray, read_json, run, size

THRESHOLDS = [[32, 160], [224, 96]]


def dither(pixels, thresholds=THRESHOLDS):
    width, height = size(thresholds)
    return [[255 if value > thresholds[y % height][x % width] else 0
             for x, value in enumerate(row)] for y, row in enumerate(pixels)]


def read(path):
    if path.suffix.lower() != ".json":
        return {"pixels": read_gray(path)}
    data = read_json(path)
    return data if isinstance(data, dict) else {"pixels": data}


def demo(data, folder):
    pixels = data["pixels"]
    thresholds = data.get("thresholds", THRESHOLDS)
    result = dither(pixels, thresholds)
    png(folder / "ordered.png", result)
    return {"size": size(result), "thresholds": thresholds, "levels": sorted(set(flat(result))),
            "preview": [row[:12] for row in result[:8]]}


if __name__ == "__main__":
    run("h03", __doc__, {"pixels": [[100, 100], [100, 100]]}, demo, read)
