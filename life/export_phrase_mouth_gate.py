"""Export source-linked phrase START / alternating mouth / CLOSE score."""
import argparse,json
from pathlib import Path
from .full_song_karaoke import ALIGNMENT_FILE
from .phrase_mouth_gate import audit,DEFAULT_SWITCH_G

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--alignment',type=Path,default=ALIGNMENT_FILE)
    parser.add_argument('--out',type=Path,default=Path('output/full_song_phrase_mouth_gate.json'))
    parser.add_argument('--min-switch',type=int,default=DEFAULT_SWITCH_G)
    args=parser.parse_args()
    report=audit(args.alignment,min_switch_g=args.min_switch)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print({k:v for k,v in report.items() if k!='events'})

if __name__=='__main__':main()
