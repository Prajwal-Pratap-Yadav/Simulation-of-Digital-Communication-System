"""Check repository-relative Markdown links and tracked artifact sizes."""

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
errors = []
paths = (
    subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
)
for name in paths:
    if not name:
        continue
    path = root / name
    if not path.is_file():
        continue
    if path.stat().st_size > 5 * 1024 * 1024:
        errors.append(f"Oversized tracked file: {name}")
    if path.suffix != ".md" or "legacy/original" in name:
        continue
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        target = target.split("#")[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        if not (path.parent / unquote(target)).exists():
            errors.append(f"Broken link in {name}: {target}")
if errors:
    raise SystemExit("\n".join(errors))
print("Tracked Markdown links and artifact sizes pass")
