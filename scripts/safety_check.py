#!/usr/bin/env python3
"""Conservative local safety check for tracked/public files.

Usage:
    python3 scripts/safety_check.py

Scans files tracked by git (falls back to a plain directory walk if git is
unavailable) and prints warnings about:

  * files under directories that should be private
    (private/, targets/, reports/, pocs/, evidence/, studio/, screenshots-private/)
  * .env-style files, *.key, *.pem, secrets.* files
  * confidentiality markers (CONFIDENTIAL, DO NOT PUBLISH, ACTIVE FINDING)
  * strings that look like private keys or seed phrases
  * a few other patterns worth a manual look

This check is intentionally simple and conservative. It does NOT delete or
modify anything, and it CANNOT guarantee that nothing sensitive is present.
It is a fast first pass, not a substitute for manual review.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

import _lib

PRIVATE_DIR_PREFIXES = (
    "private/",
    "targets/",
    "reports/",
    "pocs/",
    "evidence/",
    "studio/",
    "screenshots-private/",
)

SECRET_FILENAME_PATTERNS = (
    re.compile(r"(^|/)\.env(\..*)?$"),
    re.compile(r"\.key$"),
    re.compile(r"\.pem$"),
    re.compile(r"(^|/)secrets\..*$"),
)

CONFIDENTIAL_MARKERS = ("CONFIDENTIAL", "DO NOT PUBLISH", "ACTIVE FINDING")

CONTENT_PATTERNS = [
    ("possible private key (0x + 64 hex chars)", re.compile(r"\b0x[a-fA-F0-9]{64}\b")),
    ("PEM private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("possible seed phrase / mnemonic reference", re.compile(r"\b(seed phrase|mnemonic|recovery phrase)\b", re.IGNORECASE)),
]

TEXT_EXTENSIONS = {
    ".md", ".py", ".yaml", ".yml", ".csv", ".txt", ".json", ".sh", ".cfg", ".toml", "",
}

# Files that legitimately document the marker words/patterns themselves and would
# otherwise always trigger false positives in content_check.
CONTENT_CHECK_EXCLUDE = {
    "SECURITY_AND_DISCLOSURE.md",
    "scripts/safety_check.py",
}


def list_tracked_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=_lib.REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return [line for line in result.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        files = []
        for root, dirs, names in os.walk(_lib.REPO_ROOT):
            dirs[:] = [d for d in dirs if d != ".git"]
            for name in names:
                rel = os.path.relpath(os.path.join(root, name), _lib.REPO_ROOT)
                files.append(rel.replace(os.sep, "/"))
        return files


def check_path(path: str) -> list[str]:
    warnings = []
    for prefix in PRIVATE_DIR_PREFIXES:
        if path == prefix.rstrip("/") or path.startswith(prefix):
            warnings.append(f"{path}: located in a directory that should be private ({prefix})")
    for pattern in SECRET_FILENAME_PATTERNS:
        if pattern.search(path):
            warnings.append(f"{path}: filename matches a secret-file pattern")
    return warnings


def check_content(path: str) -> list[str]:
    warnings = []
    if path in CONTENT_CHECK_EXCLUDE:
        return warnings
    full_path = os.path.join(_lib.REPO_ROOT, path)
    _, ext = os.path.splitext(path)
    if ext.lower() not in TEXT_EXTENSIONS:
        return warnings
    try:
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                for marker in CONFIDENTIAL_MARKERS:
                    if marker in line:
                        warnings.append(f"{path}:{lineno}: contains marker '{marker}'")
                for label, pattern in CONTENT_PATTERNS:
                    if pattern.search(line):
                        warnings.append(f"{path}:{lineno}: {label}")
    except OSError:
        pass
    return warnings


def main(argv: list[str] | None = None) -> int:
    files = list_tracked_files()
    all_warnings: list[str] = []

    for path in files:
        all_warnings.extend(check_path(path))
        all_warnings.extend(check_content(path))

    if not all_warnings:
        print(f"safety-check: scanned {len(files)} tracked files, no issues found.")
        print("Note: this check is conservative and cannot guarantee nothing sensitive is present.")
        return 0

    print(f"safety-check: scanned {len(files)} tracked files, {len(all_warnings)} warning(s):\n")
    for warning in all_warnings:
        print(f"  - {warning}")
    print("\nThis check is conservative and cannot guarantee nothing sensitive is present.")
    print("Review each warning manually before publishing.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
