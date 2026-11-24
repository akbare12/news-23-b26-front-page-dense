"""news-23 b26 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1024 * 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == repo_dir:
        print("refusing to write into the repo directory", file=sys.stderr)
        return 1
    # also refuse any output dir inside the repo tree (grader runs from a
    # read-only copy; writing there would fail or pollute the submission)
    try:
        inside = os.path.commonpath([os.path.abspath(out_dir), repo_dir]) == repo_dir
    except ValueError:
        inside = False
    if inside:
        print("refusing to write inside the repo tree", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        data = f.read()
    # PNG signature
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("bad PNG signature", file=sys.stderr)
        return 1
    # IHDR chunk: length 13, type IHDR, width/height, bit depth, colour type
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        print("bad IHDR chunk", file=sys.stderr)
        return 1
    width, height, bit_depth, colour_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        print(f"bad size {width}x{height}, want 1024x1024", file=sys.stderr)
        return 1
    if bit_depth != 8 or colour_type not in (2, 6):
        print(f"unexpected bit depth {bit_depth} / colour type {colour_type}", file=sys.stderr)
        return 1
    # IEND trailer: final 12 bytes must be a well-formed IEND chunk
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("bad IEND trailer", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png too big: {len(data)} bytes", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    # re-read to confirm byte-identical
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        print("output differs from source", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
