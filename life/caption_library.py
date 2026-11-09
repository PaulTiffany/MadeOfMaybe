"""Native-Life caption page assets sized for the unchanged singer bubble.

Each page is a valid static Life pattern ready for a future glider-activated
caption sequencer. Exporting several RLEs does NOT mean the running simulation
can switch between them yet. This module NEVER inserts cells during playback.
"""
from __future__ import annotations
from pathlib import Path
from .core import evolve,place
from .composition import bubble_parts
from .export_operational import compact_rle
from .lyric_font import line_cells,width_of
from .lyric_cues import CaptionPage,caption_pages,aligned_words,read_alignment

BUBBLE_CENTER_X = 378
MIN_FIRST_GLYPH_X = 291  # bubble tail intrudes at the lower-left edge
ROW_Y = (-149,-91)
SINGLE_ROW_Y = -118
MAX_LINE_WIDTH = 190


def bubble_frame():
    original,_ = bubble_parts()
    return place(original,160,-90)


def word_rows(lines: tuple[str,...]):
    """Life-block mosaic centered within the already qualified bubble."""
    if not 1<=len(lines)<=2:
        raise ValueError('one or two caption rows required')
    out=set()
    ys=ROW_Y if len(lines)==2 else (SINGLE_ROW_Y,)
    for line,y in zip(lines,ys):
        width=width_of(line)
        if width>MAX_LINE_WIDTH:
            raise ValueError(f'caption too wide for native Life bubble: {line}')
        out.update(line_cells(line,(max(MIN_FIRST_GLYPH_X,BUBBLE_CENTER_X-width//2),y)))
    return out


def native_page(page:CaptionPage):
    """Bubble outline plus one completely native and stable Life caption."""
    frame=bubble_frame()
    caption=word_rows(page.lines)
    if frame&caption or evolve(frame|caption)!=frame|caption:
        raise ValueError(f'caption conflicts with bubble: {page.lines}')
    return frame|caption


def export_page_rles(raw, directory: str|Path):
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    pages=caption_pages(aligned_words(raw))
    for i,p in enumerate(pages):
        out=path/f'page_{i:03d}.rle'
        out.write_text(compact_rle(native_page(p),(
            f'MadeOfMaybe page {i}, {p.start_s:.3f}-{p.end_s:.3f}s',
            f'Lines: {" / ".join(p.lines)}',
            'STATIC Life-stable caption page asset; NOT runtime text switching.',
        )),encoding='utf-8')
    return len(pages)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Export qualified native Life caption-page asset RLEs')
    parser.add_argument('--alignment',default='data/made_of_maybe_suno_alignment.json')
    parser.add_argument('--out',default='output/lyric_cues/native_page_rles')
    args=parser.parse_args()
    raw=read_alignment(args.alignment)
    count=export_page_rles(raw,args.out)
    print(f'Exported {count} independently stable Golly RLE pages; not a switched Life video')
