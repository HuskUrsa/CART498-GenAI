#!/usr/bin/env python3
"""Generate a seeded Z-Image Turbo storyboard batch with one model load."""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "filipstrand/Z-Image-Turbo-mflux-4bit"
DEFAULT_CLI = PROJECT_ROOT / ".venv-mflux/bin/mflux-generate-z-image-turbo"
DEFAULT_CACHE = PROJECT_ROOT / "model_cache/huggingface"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "outputs/mflux_storyboards"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate several Z-Image Turbo frames in one MFLUX process, then "
            "assemble a labeled contact sheet."
        )
    )
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Prompt text to send to Z-Image Turbo.")
    prompt_group.add_argument("--prompt-file", type=Path, help="UTF-8 prompt file.")
    parser.add_argument("--count", type=int, default=4, help="Number of frames (default: 4).")
    parser.add_argument("--seed", type=int, nargs="*", help="Explicit seeds; overrides --count.")
    parser.add_argument("--width", type=int, default=768, help="Output width (default: 768).")
    parser.add_argument("--height", type=int, default=576, help="Output height (default: 576).")
    parser.add_argument("--steps", type=int, default=9, help="Scheduler steps (default: 9).")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Hugging Face repo or local model path.")
    parser.add_argument("--output-dir", type=Path, help="Exact run directory; timestamped by default.")
    parser.add_argument("--label", default="storyboard", help="Short filename/run label.")
    parser.add_argument("--no-contact-sheet", action="store_true", help="Skip contact-sheet assembly.")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not DEFAULT_CLI.exists():
        raise SystemExit(f"Missing MFLUX CLI: {DEFAULT_CLI}")
    if args.prompt_file and not args.prompt_file.is_file():
        raise SystemExit(f"Prompt file does not exist: {args.prompt_file}")
    if args.count < 1:
        raise SystemExit("--count must be at least 1")
    if args.width < 256 or args.height < 256:
        raise SystemExit("Width and height must each be at least 256 pixels")
    if args.width % 16 or args.height % 16:
        raise SystemExit("Width and height must be divisible by 16")
    if args.steps < 1:
        raise SystemExit("--steps must be at least 1")


def make_run_dir(args: argparse.Namespace) -> Path:
    if args.output_dir:
        run_dir = args.output_dir.expanduser().resolve()
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_label = "".join(c if c.isalnum() or c in "-_" else "_" for c in args.label)
        run_dir = DEFAULT_OUTPUT_ROOT / f"{stamp}_{safe_label}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def choose_seeds(args: argparse.Namespace) -> list[int]:
    if args.seed:
        return args.seed
    random_source = random.SystemRandom()
    return [random_source.randrange(0, 1_000_000_000) for _ in range(args.count)]


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        return args.prompt.strip()
    return args.prompt_file.read_text(encoding="utf-8").strip()


def build_contact_sheet(paths: list[Path], seeds: list[int], destination: Path) -> None:
    opened = [Image.open(path).convert("RGB") for path in paths]
    try:
        columns = 2 if len(opened) > 1 else 1
        rows = (len(opened) + columns - 1) // columns
        thumb_width = 640
        label_height = 38
        spacing = 18
        thumbs: list[Image.Image] = []
        for image in opened:
            ratio = thumb_width / image.width
            thumbs.append(image.resize((thumb_width, round(image.height * ratio)), Image.Resampling.LANCZOS))
        cell_height = max(image.height for image in thumbs) + label_height
        sheet_width = columns * thumb_width + (columns + 1) * spacing
        sheet_height = rows * cell_height + (rows + 1) * spacing
        sheet = Image.new("RGB", (sheet_width, sheet_height), "#202020")
        draw = ImageDraw.Draw(sheet)
        for index, (image, seed) in enumerate(zip(thumbs, seeds, strict=True)):
            column = index % columns
            row = index // columns
            x = spacing + column * (thumb_width + spacing)
            y = spacing + row * (cell_height + spacing)
            sheet.paste(image, (x, y))
            draw.text((x, y + image.height + 9), f"seed {seed}", fill="#f0f0f0")
        sheet.save(destination)
    finally:
        for image in opened:
            image.close()


def normalize_frame_paths(run_dir: Path, seeds: list[int]) -> list[Path]:
    """Normalize MFLUX's single- and multi-seed filename conventions."""
    normalized: list[Path] = []
    for seed in seeds:
        destination = run_dir / f"frame_{seed}.png"
        if destination.is_file():
            normalized.append(destination)
            continue
        candidates = sorted(run_dir.glob(f"*seed_{seed}.png"))
        if len(candidates) != 1:
            raise SystemExit(
                f"Could not resolve the output for seed {seed}; found {len(candidates)} candidates"
            )
        candidates[0].rename(destination)
        normalized.append(destination)
    return normalized


def main() -> int:
    args = parse_args()
    validate_args(args)
    prompt = read_prompt(args)
    if not prompt:
        raise SystemExit("Prompt is empty")

    seeds = choose_seeds(args)
    run_dir = make_run_dir(args)
    output_pattern = run_dir / "frame_{seed}.png"
    DEFAULT_CACHE.mkdir(parents=True, exist_ok=True)

    command = [
        str(DEFAULT_CLI),
        "--model",
        args.model,
        "--width",
        str(args.width),
        "--height",
        str(args.height),
        "--steps",
        str(args.steps),
        "--seed",
        *[str(seed) for seed in seeds],
        "--output",
        str(output_pattern),
    ]
    if args.prompt_file:
        command.extend(["--prompt-file", str(args.prompt_file.resolve())])
    else:
        command.extend(["--prompt", prompt])

    environment = os.environ.copy()
    environment["HF_HOME"] = str(DEFAULT_CACHE)
    environment["HF_XET_HIGH_PERFORMANCE"] = "1"

    print(f"Run directory: {run_dir}", flush=True)
    print(f"Model: {args.model}", flush=True)
    print(f"Seeds: {', '.join(map(str, seeds))}", flush=True)
    started = time.perf_counter()
    completed = subprocess.run(command, env=environment, check=False)
    elapsed = time.perf_counter() - started
    if completed.returncode:
        print(f"MFLUX exited with code {completed.returncode}", file=sys.stderr)
        return completed.returncode

    frame_paths = normalize_frame_paths(run_dir, seeds)

    contact_sheet = None
    if not args.no_contact_sheet:
        contact_sheet = run_dir / "contact_sheet.png"
        build_contact_sheet(frame_paths, seeds, contact_sheet)

    manifest = {
        "created_at": datetime.now().astimezone().isoformat(),
        "model": args.model,
        "prompt": prompt,
        "width": args.width,
        "height": args.height,
        "steps": args.steps,
        "seeds": seeds,
        "elapsed_seconds": round(elapsed, 3),
        "frames": [path.name for path in frame_paths],
        "contact_sheet": contact_sheet.name if contact_sheet else None,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Completed {len(frame_paths)} frame(s) in {elapsed:.1f}s", flush=True)
    if contact_sheet:
        print(f"Contact sheet: {contact_sheet}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
