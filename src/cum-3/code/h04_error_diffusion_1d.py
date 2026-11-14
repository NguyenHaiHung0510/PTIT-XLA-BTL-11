"""H04 — Khuếch tán lỗi 1D: chuyển lỗi sang pixel tiếp theo cùng hàng."""

from demo_io import flat, png, read_gray, read_json, run, size


def threshold(value, cutoff):
    return 0 if value < cutoff else 255


def diffuse_row(row, cutoff):
    error = 0
    output, trace = [], []
    for value in row:
        corrected = value + error
        chosen = threshold(corrected, cutoff)
        error = corrected - chosen
        output.append(chosen)
        if len(trace) < 12:
            trace.append([value, corrected, chosen, error])
    # Hàm kết thúc ở cuối hàng; sai số không chuyển sang hàng sau.
    return output, trace


def read(path):
    if path.suffix.lower() != ".json":
        return {"pixels": read_gray(path)}
    data = read_json(path)
    return data if isinstance(data, dict) else {"pixels": data}


def demo(data, folder):
    pixels, cutoff = data["pixels"], data.get("threshold", 127)
    pairs = [diffuse_row(row, cutoff) for row in pixels]
    result = [pair[0] for pair in pairs]
    baseline = [[threshold(value, cutoff) for value in row] for row in pixels]
    png(folder / "threshold.png", baseline)
    png(folder / "diffused.png", result)
    return {"size": size(result), "threshold": cutoff, "levels": sorted(set(flat(result))),
            "preview": [row[:12] for row in result[:8]],
            "trace_columns": ["original", "corrected", "output", "error"],
            "trace": [pair[1] for pair in pairs[:8]]}


if __name__ == "__main__":
    run("h04", __doc__, {"pixels": [[100] * 4, [100] * 4]}, demo, read)
