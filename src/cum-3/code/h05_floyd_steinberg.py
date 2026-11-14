"""H05 — Floyd–Steinberg: chia lỗi cho bốn điểm chưa duyệt."""

from demo_io import flat, png, run, size
from h04_error_diffusion_1d import read, threshold

NEIGHBORS = [(0, 1, 7), (1, -1, 3), (1, 0, 5), (1, 1, 1)]


def diffuse(pixels, cutoff):
    width, height = size(pixels)
    work = [list(row) for row in pixels]
    result = [[0] * width for _ in range(height)]
    trace = []
    for y in range(height):
        for x in range(width):
            value = work[y][x]
            chosen = threshold(value, cutoff)
            error = value - chosen
            result[y][x] = chosen
            updates = []
            for dy, dx, weight in NEIGHBORS:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width:
                    delta = error * weight / 16
                    work[ny][nx] += delta
                    if len(trace) < 8:
                        updates.append([ny, nx, delta])
            if len(trace) < 8:
                trace.append({"row": y, "col": x, "corrected": value,
                              "output": chosen, "error": error, "updates": updates})
    return result, trace


def demo(data, folder):
    cutoff = data.get("threshold", 127)
    result, trace = diffuse(data["pixels"], cutoff)
    png(folder / "diffused.png", result)
    return {"size": size(result), "threshold": cutoff, "levels": sorted(set(flat(result))),
            "preview": [row[:12] for row in result[:8]], "trace": trace}


if __name__ == "__main__":
    run("h05", __doc__, {"pixels": [[100, 100], [100, 100]]}, demo, read)
