# VTT Cleaning Reference

The primary cleaning method is `scripts/clean_vtt.py`. This file documents what it does and serves as a manual fallback if the script cannot run.

---

## What the Script Does

### Input: Raw Teams VTT

```
WEBVTT

1
00:00:05.000 --> 00:00:08.000
<v John Smith>We need to</v>

2
00:00:08.200 --> 00:00:10.500
<v John Smith>review the budget before end of month</v>

3
00:00:11.000 --> 00:00:13.000
<v Sarah Lee (Contoso)>Agreed. I can have the numbers ready by Friday.</v>
```

### Output: Cleaned transcript

```
John Smith: We need to review the budget before end of month
Sarah Lee: Agreed. I can have the numbers ready by Friday.
```

---

## What Gets Stripped

| Pattern | Example | Action |
|---|---|---|
| WEBVTT header | `WEBVTT` | Remove |
| NOTE blocks | `NOTE ...` | Remove |
| Cue identifiers | `1`, `2`, `42` or `b20e633d-.../18-0` (Teams UUID) | Remove |
| Timestamp lines | `00:00:05.000 --> 00:00:08.000` | Remove |
| VTT voice tags | `<v Name>...</v>` | Strip tags, keep content |
| Inline HTML tags | `<c>`, `<b>`, etc. | Strip |
| Meta markers | `[Recording started]` | Remove |
| Blank lines | | Remove |

## What Gets Normalised

| Pattern | Before | After |
|---|---|---|
| Company suffix in name | `Sarah Lee (Contoso)` | `Sarah Lee` |
| All-caps name | `JOHN SMITH` | `John Smith` |
| Consecutive same-speaker lines | 3 separate lines | Merged into one turn |
| Duplicate consecutive turns | Same line repeated | Deduplicated |

---

## Manual Fallback

If the script cannot run (no Python, permission error, encoding issue), apply these rules manually in order:

1. Remove every line matching: `WEBVTT`, `NOTE *`, pure integers, Teams UUID cue IDs (format `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/N-N`), `HH:MM:SS --> HH:MM:SS`
2. For `<v Speaker Name>text</v>` lines → rewrite as `Speaker Name: text`
3. For `Speaker Name (Company): text` → rewrite as `Speaker Name: text`
4. Merge consecutive lines with the same speaker prefix into one line
5. Remove exact duplicate consecutive lines
6. Replace blank speaker with `[Unknown]`

---

## Edge Cases

### Encoding errors
Teams sometimes exports VTTs with mixed UTF-8/Latin-1. The script uses `errors="replace"` so it won't crash, but garbled characters may appear. If you see `?` or `â€™` in the output, tell the user their VTT has encoding issues.

### No speaker names at all
Some VTT exports omit speaker labels entirely. The script will label everything `[Unknown]`. Flag this to the moderator — the transcript is still usable but decisions/owners will need manual attribution.

### Very long monologues
If one speaker talks for >5 minutes without interruption, their merged turn can be very long. This is correct behaviour — don't split artificially.

### Overlapping timestamps (crosstalk)
Teams occasionally produces overlapping cues for crosstalk. The script processes them in file order. Crosstalk attribution may be imperfect — flag if `[Unknown]` count is high relative to total turns.