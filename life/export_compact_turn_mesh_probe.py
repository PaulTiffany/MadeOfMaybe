"""Export measured native stagger micro-mesh and Golly RLE."""
import json
from pathlib import Path
from .core import encode_rle
from .compact_turn_mesh_probe import components,qualify

def main():
    cert=qualify()
    folder=Path('output/compact_turn_mesh')
    folder.mkdir(parents=True,exist_ok=True)
    cells=set().union(*components())
    (folder/'seven_row_stagger.rle').write_text(encode_rle(cells,(
        'Native B3/S23 diagonal seven-corner LWSS turn mesh',
        'All seven outputs aligned by g800; one-shot, debris not cleaned',
        'Global collision separation verified through generation 3200',
    )),encoding='utf-8')
    (folder/'seven_row_stagger_certificate.json').write_text(
        json.dumps(cert,indent=2)+'\n',encoding='utf-8')
    print('Exported',len(cells),'initial native cells and proof certificate.')

if __name__=='__main__':main()
