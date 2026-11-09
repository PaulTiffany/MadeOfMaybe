"""Compile Suno word alignment to deterministic Life-generations and bubble pages.

This module describes *timing and native-Life caption assets*, not phonemes.
Neither its cue files nor SRT cause runtime cell insertion: the final Life
performance must implement every desired event using generation-zero cells.

Caveats: Suno sometimes aligns punctuation as separate tokens, splits words
across syllables, and assigns zero duration to a few tokens. We retain exact
source token indices and flag anomalies rather than fabricate precision.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import re
from typing import Iterable

AUDIO_ID = "53610991-7381-4749-96e1-79b8e3b1c28b"
GENERATIONS_PER_SECOND = 24
MAX_BUBBLE_CHARS = 8
MAX_BUBBLE_LINES = 2
_HEADER = re.compile(r"\[[^\]]*\]")
_PAREN = re.compile(r"\([^)]*\)")
_PUNCT_NEW_WORD = re.compile(r"^[,;:]\s+(.*)$", re.DOTALL)
_GLYPH_CHAR = re.compile(r"[^A-Z0-9'!? .-]")


@dataclass(frozen=True)
class LyricWord:
    text: str
    start_s: float
    end_s: float
    line: int
    section: str
    source_tokens: tuple[int, ...]
    flagged: bool = False


@dataclass(frozen=True)
class CaptionPage:
    lines: tuple[str, ...]
    words: tuple[LyricWord, ...]
    start_s: float
    end_s: float
    section: str
    line: int


def generation(seconds: float, gps: int = GENERATIONS_PER_SECOND) -> int:
    """Nearest generation, with decimal half-up rounding."""
    if gps <= 0 or seconds < 0:
        raise ValueError("time must be nonnegative and gps positive")
    return int((Decimal(str(seconds)) * gps).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def make_generation(seconds: float, gps: int = GENERATIONS_PER_SECOND) -> int:
    """Nearest permitted two-glider block MAKE generation (4 mod 4)."""
    desired = generation(seconds, gps)
    return max(4, 4 * int((Decimal(desired) / 4).quantize(Decimal("1"), rounding=ROUND_HALF_UP)))


def read_alignment(path: str | Path) -> dict:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if value.get("audio_id") != AUDIO_ID or value.get("status") != "complete":
        raise ValueError("Not the completed alignment for the selected Made of Maybe song")
    if not isinstance(value.get("words"), list) or not value["words"]:
        raise ValueError("No lyrics-alignment words")
    last = 0.0
    for i, entry in enumerate(value["words"]):
        if not isinstance(entry.get("word"), str):
            raise ValueError(f"bad word entry at token {i}")
        start = float(entry["start_s"])
        end = float(entry["end_s"])
        if start < 0 or end < start or start < last - .15:
            raise ValueError(f"invalid/nonmonotone alignment at token {i}")
        last = max(last, end)
    return value


def aligned_words(raw: dict) -> tuple[LyricWord, ...]:
    """Join detached punctuation and syllable fragments, retaining provenance."""
    out: list[LyricWord] = []
    section = "Unlabeled"
    line = -1
    for i, token in enumerate(raw["words"]):
        original = token["word"]
        headers = _HEADER.findall(original)
        # Only headers preceding the token surface describe its section.
        # A trailing [End] annotation must not relabel the final sung word.
        if headers and original.lstrip().startswith("["):
            section = headers[-1][1:-1].strip()
        cleaned = _PAREN.sub("", _HEADER.sub("", original))
        match = re.match(r"\s*", cleaned)
        prefix = match.group(0) if match else ""
        has_break = "\n" in prefix  # trailing newlines belong to the NEXT word
        begins_with_whitespace = bool(prefix)
        surface = cleaned.strip()
        if not surface:
            continue
        punct = _PUNCT_NEW_WORD.match(surface)
        if punct:
            surface = punct.group(1)
            begins_with_whitespace = True
        surface = _GLYPH_CHAR.sub("", surface.upper()).strip()
        if not surface:
            continue
        start = float(token["start_s"])
        end = float(token["end_s"])
        flagged = end <= start or not bool(token.get("success", True))
        if has_break:
            line += 1
        elif line < 0:
            line = 0
        attach = (out and not has_break and not begins_with_whitespace and not punct
                  and out[-1].line == line)
        if attach:
            previous = out[-1]
            out[-1] = LyricWord(previous.text + surface,
                               previous.start_s, max(previous.end_s, end),
                               line, previous.section, previous.source_tokens + (i,),
                               previous.flagged or flagged)
        else:
            out.append(LyricWord(surface, start, end, line, section, (i,), flagged))
    return tuple(out)


def _fragments(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks = []
    while len(text) > max_chars:
        chunks.append(text[:max_chars-1] + "-")
        text = text[max_chars-1:]
    chunks.append(text)
    return chunks


def caption_pages(words: Iterable[LyricWord], max_chars: int = MAX_BUBBLE_CHARS,
                  max_lines: int = MAX_BUBBLE_LINES) -> tuple[CaptionPage, ...]:
    """Wrap semantic lyric lines without trimming or dropping any displayed word."""
    if max_chars < 2 or max_lines < 1:
        raise ValueError("unusable bubble layout dimensions")
    words = tuple(words)
    if not words:
        return ()
    pages: list[CaptionPage] = []
    groups: list[list[LyricWord]] = []
    for word in words:
        if not groups or word.line != groups[-1][-1].line:
            groups.append([])
        groups[-1].append(word)
    for group in groups:
        lines: list[str] = []
        selected: list[LyricWord] = []

        def emit():
            if lines:
                unique = tuple(dict.fromkeys(selected))
                pages.append(CaptionPage(tuple(lines), unique,
                                         unique[0].start_s, max(w.end_s for w in unique),
                                         unique[0].section, unique[0].line))

        for word in group:
            pieces = _fragments(word.text, max_chars)
            for part in pieces:
                if lines and len(pieces) == 1 and len(lines[-1])+1+len(part) <= max_chars:
                    lines[-1] += " " + part
                elif len(lines) >= max_lines:
                    emit()
                    lines = [part]
                    selected = []
                else:
                    lines.append(part)
                selected.append(word)
        emit()
    return tuple(pages)


def cue_rows(raw: dict, gps: int = GENERATIONS_PER_SECOND) -> list[dict]:
    out = []
    for i, w in enumerate(aligned_words(raw)):
        out.append({
            "word_index": i,
            "word": w.text,
            "section": w.section,
            "source_line": w.line,
            "start_s": round(w.start_s, 3),
            "end_s": round(w.end_s, 3),
            "generation_on": generation(w.start_s, gps),
            "generation_off": generation(w.end_s, gps),
            "make_generation": make_generation(w.start_s, gps),
            "source_token_indices": ";".join(str(x) for x in w.source_tokens),
            "flagged": int(w.flagged),
        })
    return out


def page_rows(raw: dict, gps: int = GENERATIONS_PER_SECOND) -> list[dict]:
    out = []
    for i, p in enumerate(caption_pages(aligned_words(raw))):
        out.append({
            "page": i,
            "start_s": round(p.start_s, 3),
            "end_s": round(p.end_s, 3),
            "start_generation": generation(p.start_s, gps),
            "end_generation": generation(p.end_s, gps),
            "line1": p.lines[0],
            "line2": p.lines[1] if len(p.lines)>1 else "",
            "section": p.section,
            "source_line": p.line,
            "source_tokens": ";".join(str(t) for w in p.words for t in w.source_tokens),
            "has_flagged_tokens": int(any(w.flagged for w in p.words)),
        })
    return out


def export_cue_csv(raw: dict, path: str | Path, gps: int = GENERATIONS_PER_SECOND):
    rows = cue_rows(raw, gps)
    with Path(path).open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def export_pages_csv(raw: dict, path: str | Path, gps: int = GENERATIONS_PER_SECOND):
    rows = page_rows(raw, gps)
    with Path(path).open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def _srt_clock(seconds: float) -> str:
    milliseconds = int((Decimal(str(seconds)) * 1000).quantize(Decimal("1"),rounding=ROUND_HALF_UP))
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    sec, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{sec:02d},{ms:03d}"


def export_pages_srt(raw: dict, path: str | Path):
    """Reference subtitle timing, NOT a rendered/native-Life caption switch."""
    pages = caption_pages(aligned_words(raw))
    lines = []
    for i, p in enumerate(pages):
        next_start = pages[i+1].start_s if i+1 < len(pages) else None
        ending = p.end_s + .22
        if next_start is not None:
            ending = min(ending, next_start-.02)
        # A long word split across pages can create equal timestamps. For
        # those, choose a small reference time span and flag page data.
        ending = max(ending, p.start_s + .042)
        lines += [str(i+1), f"{_srt_clock(p.start_s)} --> {_srt_clock(ending)}",
                  *p.lines, ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def export_pages_json(raw: dict, path: str | Path, gps: int = GENERATIONS_PER_SECOND):
    pages=page_rows(raw,gps)
    out={"audio_id":AUDIO_ID,"gps":gps,"source":"Suno word-level lyric alignment",
         "native_life_switching":"NOT IMPLEMENTED FOR CAPTION PAGES",
         "note":"Source of truth for preloaded glider controller planning; not phoneme data.",
         "pages":pages}
    Path(path).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")


def compile_files(raw: dict, prefix: str | Path, gps: int = GENERATIONS_PER_SECOND):
    prefix=Path(prefix)
    prefix.parent.mkdir(exist_ok=True,parents=True)
    stem=prefix.name
    export_cue_csv(raw,prefix.with_name(stem+"_words.csv"),gps)
    export_pages_csv(raw,prefix.with_name(stem+"_pages.csv"),gps)
    export_pages_srt(raw,prefix.with_name(stem+"_pages.srt"))
    export_pages_json(raw,prefix.with_name(stem+"_pages.json"),gps)


if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser(description="Compile Suno Made of Maybe lyric events to Life timing")
    parser.add_argument("--alignment",default="data/made_of_maybe_suno_alignment.json")
    parser.add_argument("--out",default="output/lyric_cues")
    parser.add_argument("--gps",type=int,default=GENERATIONS_PER_SECOND)
    args=parser.parse_args()
    value=read_alignment(args.alignment)
    compile_files(value,args.out,args.gps)
    words=aligned_words(value);pages=caption_pages(words)
    print(f"Compiled {len(value['words'])} Suno tokens into {len(words)} displayed words and {len(pages)} caption pages, at {args.gps} B3/S23 generations/sec")
