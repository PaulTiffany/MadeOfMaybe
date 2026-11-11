"""One-shot authorized owner's Suno MP3 transfer for film mux.

The temporary signed download URL is stored in an unreferenced private
GitHub git blob rather than in any tracked source, configuration, CI
logs, artifacts or source commits. Only a blob SHA appears in workflow.
Once the signed link expires it cannot authorize new reads. No credit
confirmation is executed by this script.
"""
from __future__ import annotations
import base64,json,os,sys,urllib.request
from pathlib import Path

def fetch(destination):
    blob_sha=os.environ['SUNO_URL_BLOB_SHA']
    token=os.environ['GH_TOKEN']
    if len(blob_sha)!=40 or not all(ch in '0123456789abcdef' for ch in blob_sha):
        raise ValueError('malformed ephemeral private blob SHA')
    uri=f'https://api.github.com/repos/PaulTiffany/MadeOfMaybe/git/blobs/{blob_sha}'
    request=urllib.request.Request(uri,headers={
      'Authorization':'Bearer '+token,
      'Accept':'application/vnd.github+json',
      'X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(request,timeout=30) as f:
        meta=json.load(f)
    url=base64.b64decode(meta['content']).decode().strip()
    if not url.startswith('https://suno-data-uploads.s3.amazonaws.com/'):
        raise ValueError('authorized user-owned Suno export unexpected host')
    dest=Path(destination);dest.parent.mkdir(parents=True,exist_ok=True)
    with urllib.request.urlopen(url,timeout=60) as f, dest.open('wb') as o:
        while buf:=f.read(1024*1024):
            o.write(buf)
    if dest.stat().st_size<1_000_000:
        dest.unlink(missing_ok=True)
        raise ValueError('authorized Suno master transfer is unexpectedly small')
    print('Successfully transferred original user-owned Suno master bytes:',
          dest.stat().st_size,'(signed URL was not logged)')

if __name__=='__main__':
    fetch(sys.argv[1])
