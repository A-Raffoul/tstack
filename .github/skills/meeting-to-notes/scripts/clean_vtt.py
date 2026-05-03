#!/usr/bin/env python3
"""
clean_vtt.py — Pre-process a Teams .vtt transcript before passing to Claude.

Usage:
    python clean_vtt.py input.vtt                  # prints cleaned transcript to stdout
    python clean_vtt.py input.vtt -o output.txt    # writes to file
    python clean_vtt.py input.vtt --stats          # also prints token savings estimate

Output format (one line per speaker turn):
    Speaker Name: text of what they said

Unknown speakers are labelled [Unknown].
"""

import re
import sys
import argparse
from pathlib import Path


def _is_cue_id(line: str) -> bool:
    """True if line is a cue identifier — plain integer or Teams UUID format."""
    if re.match(r"^\d+$", line):
        return True
    # Teams format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/N-N
    if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}[/\-]\d", line, re.IGNORECASE):
        return True
    return False


def _is_timestamp(line: str) -> bool:
    return bool(re.match(r"^\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->", line))


_META_MARKERS = {
    "[Recording started]", "[Recording stopped]",
    "[Recording Started]", "[Recording Stopped]",
}


def _normalize_speaker(name: str) -> str:
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
    if name.isupper():
        name = name.title()
    return name


def _strip_inline_tags(text: str) -> str:
    """Remove residual HTML/VTT inline tags like <c>, <b>, </v>."""
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _extract_speaker_text(cue_text: str) -> tuple[str, str]:
    """
    Extract (speaker, text) from a full cue text string.
    Handles both <v Speaker>text</v> and "Speaker: text" formats.
    cue_text may span multiple original lines (joined with space).
    """
    # Pattern 1: <v Speaker Name>text</v>  — closing tag optional
    match = re.match(r"<v\s+([^>]+)>(.*?)(?:</v>)?$", cue_text, re.IGNORECASE | re.DOTALL)
    if match:
        speaker = _normalize_speaker(match.group(1).strip())
        text = _strip_inline_tags(match.group(2).strip())
        return speaker, text

    # Pattern 2: "Speaker Name: text" — at least 2 words before colon
    match = re.match(r"^([A-Z][^\:]{2,50}):\s+(.+)$", cue_text)
    if match:
        speaker = _normalize_speaker(match.group(1).strip())
        text = _strip_inline_tags(match.group(2).strip())
        return speaker, text

    text = _strip_inline_tags(cue_text.strip())
    return "", text


def clean_vtt(content: str) -> tuple[list[tuple[str, str]], dict]:
    """
    Parse and clean a VTT file, treating each cue as an atomic block.

    VTT cues are separated by blank lines. Processing per line (as the naive
    approach does) breaks on multi-line cue text and UUID cue identifiers.
    """
    lines = content.splitlines()
    stats = {"raw_lines": len(lines), "unknown_count": 0}

    # ── Split into cue blocks (blank-line separated) ──
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            current.append(stripped)
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)

    # ── Extract one (speaker, text) per cue block ──
    raw_segments: list[tuple[str, str]] = []

    for block in blocks:
        if not block:
            continue

        # Skip WEBVTT header and NOTE blocks
        if block[0].startswith("WEBVTT") or block[0].startswith("NOTE"):
            continue

        # Collect only the cue text lines (discard ID, timestamp, meta markers)
        text_lines = [
            line for line in block
            if not _is_cue_id(line)
            and not _is_timestamp(line)
            and line not in _META_MARKERS
        ]

        if not text_lines:
            continue

        # Join multi-line cue text before parsing — this preserves speaker attribution
        full_cue = " ".join(text_lines)
        speaker, text = _extract_speaker_text(full_cue)

        if not text:
            continue

        if not speaker:
            stats["unknown_count"] += 1
            speaker = "[Unknown]"

        raw_segments.append((speaker, text))

    # ── Merge consecutive turns from the same speaker ──
    merged: list[tuple[str, str]] = []
    for speaker, text in raw_segments:
        if merged and merged[-1][0] == speaker:
            prev_text = merged[-1][1]
            if not prev_text.endswith(text):
                merged[-1] = (speaker, prev_text + " " + text)
        else:
            merged.append((speaker, text))

    # ── Deduplicate exact consecutive turns ──
    deduped: list[tuple[str, str]] = []
    for turn in merged:
        if not deduped or deduped[-1] != turn:
            deduped.append(turn)

    stats["cleaned_turns"] = len(deduped)
    return deduped, stats


def format_output(turns: list[tuple[str, str]]) -> str:
    return "\n".join(f"{speaker}: {text}" for speaker, text in turns)


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def main():
    parser = argparse.ArgumentParser(description="Clean a Teams .vtt transcript for Claude.")
    parser.add_argument("input", help="Path to input .vtt file")
    parser.add_argument("-o", "--output", help="Path to output .txt file (default: stdout)")
    parser.add_argument("--stats", action="store_true", help="Print token savings stats to stderr")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw_content = input_path.read_text(encoding="utf-8", errors="replace")
    turns, stats = clean_vtt(raw_content)
    cleaned_text = format_output(turns)

    if args.output:
        Path(args.output).write_text(cleaned_text, encoding="utf-8")
    else:
        print(cleaned_text)

    raw_tokens = estimate_tokens(raw_content)
    clean_tokens = estimate_tokens(cleaned_text)
    saving_pct = round((1 - clean_tokens / max(raw_tokens, 1)) * 100)

    if args.stats or args.output:
        print(f"\n── VTT Cleaning Stats ──", file=sys.stderr)
        print(f"  Raw lines       : {stats['raw_lines']}", file=sys.stderr)
        print(f"  Speaker turns   : {stats['cleaned_turns']}", file=sys.stderr)
        print(f"  Unknown speakers: {stats['unknown_count']}", file=sys.stderr)
        print(f"  Est. tokens raw : ~{raw_tokens}", file=sys.stderr)
        print(f"  Est. tokens out : ~{clean_tokens}", file=sys.stderr)
        print(f"  Token reduction : ~{saving_pct}%", file=sys.stderr)
        if stats["unknown_count"] > 0:
            print(f"\n  ⚠️  {stats['unknown_count']} line(s) had no speaker — labelled [Unknown]", file=sys.stderr)


if __name__ == "__main__":
    main()
