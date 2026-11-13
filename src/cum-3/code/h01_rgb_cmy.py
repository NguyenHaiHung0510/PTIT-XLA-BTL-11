"""H01 — RGB ↔ CMY lý tưởng, mỗi kênh từ 0 đến 255."""

from demo_io import png, read_image, read_json, run


def complement(pixels):
    return [[[255 - channel for channel in pixel] for pixel in row] for row in pixels]


def read_rgb(path):
    return read_json(path) if path.suffix.lower() == ".json" else read_image(path, "RGB")


def demo(pixels, folder):
    cmy = complement(pixels)
    restored = complement(cmy)
    for index, name in enumerate(("cyan", "magenta", "yellow")):
        # Trắng trong ảnh kênh = giá trị lượng mực cao; không phải màu giấy thật.
        png(folder / f"{name}.png", [[pixel[index] for pixel in row] for row in cmy])
    png(folder / "restored_rgb.png", restored, rgb=True)
    return {"first_rgb": pixels[0][0], "first_cmy": cmy[0][0],
            "restored_rgb": restored[0][0], "round_trip": restored == [[list(pixel) for pixel in row] for row in pixels]}


if __name__ == "__main__":
    run("h01", __doc__, [[[240, 60, 20], [255, 255, 255], [0, 0, 0]]], demo, read_rgb)
