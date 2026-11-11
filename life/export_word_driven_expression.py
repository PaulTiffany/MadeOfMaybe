"""Export auditable target states tied ONLY to actual Conway karaoke events."""
import argparse,json
from pathlib import Path
from .word_driven_expression import audit
from .full_song_karaoke import ALIGNMENT_FILE

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=Path('output/full_song_three_state_intent.json'))
    p.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    args=p.parse_args(); args.out.parent.mkdir(parents=True,exist_ok=True)
    if not args.alignment.exists(): raise FileNotFoundError(f'Source alignment required: {args.alignment}')
    result=audit(args.alignment);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(f"{result['word_events']} word cues; {result['line_clear_events']} line clears; {result['state_changes_requested']} three-state intentions; physically routed: {result['physical_full_lip_wiring_verified']}")

if __name__=='__main__':main()
