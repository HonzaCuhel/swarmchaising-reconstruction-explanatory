#!/usr/bin/env python3
"""Static composition contract checks; this is not a browser or quality review."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,subprocess,tempfile,hashlib
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.scripts=[];self.script=None;self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.nodes.append((tag,d))
  if tag=='script' and 'src' not in d:self.script=''
 def handle_data(self,t):
  if self.script is not None:self.script+=t
 def handle_endtag(self,tag):
  if tag=='script' and self.script is not None:self.scripts.append(self.script);self.script=None

def verify_evidence(project,data):
 index=json.loads((project/'evidence-index.json').read_text())
 evidence={e['id']:e for e in index['evidence']}
 assert len(evidence)==len(index['evidence']),'Duplicate evidence IDs'
 sources={s['id']:s for s in index['sources']}
 used={eid for line in data['lines'] for eid in line['evidence_ids']}
 assert used<=evidence.keys(),f'Unresolved evidence IDs: {used-evidence.keys()}'
 for eid in used:
  e=evidence[eid]
  assert e['source_id'] in sources,(eid,'Missing source')
  assert e['source_url'].startswith('https://'),(eid,'Missing public source URL')
  assert any(e.get(k) for k in ['line','locator','unit_id','unit_ids']),(eid,'Missing record locator')
 return len(used)

def main():
 reports=[]
 for p in sorted((ROOT/'hyperframes').iterdir()):
  if not p.is_dir():continue
  data=json.loads((p/'case.json').read_text());evidence_checked=verify_evidence(p,data);parent=Page((p/'index.html').read_text());ids=[];count=0;caption_checks=0
  slots=[d for tag,d in parent.nodes if 'data-composition-src' in d]
  assert len(slots)==6
  assert not any(tag=='video' for tag,d in parent.nodes)
  previous=0
  for slot in slots:
   start=float(slot['data-start']);duration=float(slot['data-duration']);assert abs(start-previous)<1e-6;previous=start+duration
   file=p/slot['data-composition-src'];raw=file.read_text();page=Page(raw)
   roots=[d for tag,d in page.nodes if 'data-composition-id' in d];assert len(roots)==1
   assert roots[0]['data-composition-id']==slot['data-composition-id']
   assert abs(float(roots[0]['data-duration'])-duration)<1e-6
   expected=[q for q in data['caption_cues'] if q['end_seconds']>start and q['start_seconds']<previous]
   scripts='\n'.join(page.scripts)
   for n,q in enumerate(expected):
    cue_id=f"{slot['data-composition-id']}-caption-{n}"
    assert any(d.get('id')==cue_id for _,d in page.nodes)
    for t,opacity in [(max(0,q['start_seconds']-start),1),(min(duration,q['end_seconds']-start),0)]:
     needle=f'tl.set("#{cue_id}",{{opacity:{opacity}}},{t:.6f});';assert needle in scripts,(file.name,needle)
    caption_checks+=1
   assert '<video' not in raw and '.mp4' not in raw
   for tag,d in page.nodes:
    if 'id' in d:ids.append(d['id'])
    for key in ['href','src']:
     path=d.get(key,'')
     if path and not path.startswith(('http:','https:','#')):assert (p/path).exists(),(file.name,path)
   for script in page.scripts:
    with tempfile.NamedTemporaryFile('w',suffix='.js') as f:
     f.write(script);f.flush();subprocess.run(['node','--check',f.name],check=True)
   count+=1
  assert abs(previous-data['duration_seconds'])<1e-6
  assert len(ids)==len(set(ids)),'Duplicate assembled IDs'
  assert not re.search(r'lesson|moral|takeaway',json.dumps(data['lines']),re.I)
  reports.append(dict(case=p.name,scenes=count,caption_cues_checked=caption_checks,evidence_ids_resolved=evidence_checked,static_contract='passed',browser_and_render='pending',narration_sha256=hashlib.sha256((p/'assets/narration.m4a').read_bytes()).hexdigest()))
 dest=ROOT/'production/source-verification.json';dest.write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
