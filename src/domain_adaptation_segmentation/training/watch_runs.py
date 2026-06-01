"""Watch experiment progress from status files and stdout logs."""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - watcher should not crash on partial writes.
        return {"_error": str(exc)}


def find_status_files(runs_root: Path) -> list[Path]:
    return sorted(runs_root.glob("experiments/*/status.json"))


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def latest_status(status_files: list[Path]) -> tuple[Path, dict] | None:
    if not status_files:
        return None
    statuses = [(path, read_json(path)) for path in status_files]

    def sort_key(item: tuple[Path, dict]) -> tuple[int, datetime]:
        _path, status = item
        running_rank = 1 if status.get("status") == "running" else 0
        heartbeat = parse_time(status.get("last_heartbeat_utc")) or parse_time(
            status.get("started_at_utc")
        )
        return running_rank, heartbeat or datetime.min.replace(tzinfo=timezone.utc)

    return max(statuses, key=sort_key)


def tail_lines(path: Path, lines: int) -> list[str]:
    if not path.exists():
        return [f"[missing] {path}"]
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return [f"[read-error] {path}: {exc}"]
    return text.splitlines()[-lines:]


def read_latest_metrics(run_dir: Path) -> list[str]:
    results = run_dir / "results.csv"
    if not results.exists():
        return ["results.csv: not written yet"]
    lines = tail_lines(results, 2)
    if len(lines) == 1:
        return lines
    return ["results.csv latest:", lines[0], lines[-1]]


def print_summary(runs_root: Path, active_path: Path, active_status: dict, tail: int) -> None:
    run_dir = active_path.parent
    status_files = find_status_files(runs_root)
    statuses = [(path.parent.name, read_json(path).get("status", "unknown")) for path in status_files]

    print("Domain Adaptation Segmentation - Live Watch")
    print("=" * 72)
    print(f"Time UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"Runs root: {runs_root}")
    print()
    print("Experiment statuses:")
    for name, status in statuses:
        marker = "->" if name == run_dir.name else "  "
        print(f"{marker} {name:35s} {status}")

    print()
    print("Active/latest experiment:")
    print(f"  {run_dir.name}")
    for key in [
        "experiment_id",
        "name",
        "status",
        "started_at_utc",
        "last_heartbeat_utc",
        "finished_at_utc",
        "elapsed_seconds",
        "device",
        "return_code",
    ]:
        if key in active_status:
            print(f"  {key}: {active_status[key]}")

    print()
    print("Latest metrics:")
    for line in read_latest_metrics(run_dir):
        print(f"  {line}")

    print()
    print(f"stdout.log tail ({tail} lines):")
    print("-" * 72)
    for line in tail_lines(run_dir / "stdout.log", tail):
        print(line)


def watch(runs_root: Path, interval: float, tail: int, once: bool, no_clear: bool) -> None:
    while True:
        status_files = find_status_files(runs_root)
        latest = latest_status(status_files)
        if not no_clear:
            clear_screen()
        if latest is None:
            print(f"No status files found under {runs_root}/experiments")
        else:
            active_path, active_status = latest
            print_summary(runs_root, active_path, active_status, tail)

        if once:
            return
        time.sleep(interval)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--interval", type=float, default=10.0)
    parser.add_argument("--tail", type=int, default=30)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--no-clear", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    watch(args.runs_root, args.interval, args.tail, args.once, args.no_clear)


if __name__ == "__main__":
    main()

