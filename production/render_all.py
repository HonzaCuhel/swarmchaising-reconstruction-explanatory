#!/usr/bin/env python3
"""Run real HyperFrames checks/renders; publish outputs only after decode checks."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
CASES=['mythos','geological-clock','saving-gemini','opus-loan','doug-mira','ash-constitution']

def cli_command():
 override=os.environ.get('HYPERFRAMES_CLI')
 if override:return ['node',override]
 installed=ROOT/'node_modules/.bin/hyperframes'
 if installed.exists():return [str(installed)]
 return ['npx','--yes','hyperframes@0.7.10']

def execute(command,log):
 print('RUN '+' '.join(command),flush=True)
 env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY='1')
 with log.open('w') as f:
  p=subprocess.Popen(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=env)
  for line in p.stdout:print(line,end='',flush=True);f.write(line)
  code=p.wait()
 if code:raise RuntimeError(f'Command failed ({code}); see {log.relative_to(ROOT)}')

def probe_and_decode(path,expected):
 p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
 v=next(s for s in p['streams'] if s['codec_type']=='video');audio=[s for s in p['streams'] if s['codec_type']=='audio']
 assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1'),v
 assert audio,'Narration stream missing'
 actual=float(p['format']['duration']);assert abs(actual-expected)<.15,(actual,expected)
 subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
 return dict(duration_seconds=actual,width=v['width'],height=v['height'],fps=30,full_decode='passed',audio_stream_present=True)

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--case',choices=CASES);parser.add_argument('--lint-only',action='store_true');args=parser.parse_args()
 cli=cli_command();version=subprocess.check_output(cli+['--version'],text=True,env=dict(os.environ,HYPERFRAMES_NO_TELEMETRY='1')).strip()
 match=re.search(r'(\d+)\.(\d+)\.(\d+)',version)
 if not match:raise RuntimeError('Cannot establish the installed HyperFrames version: '+version)
 legacy=tuple(map(int,match.groups()))<(0,8,0)
 manifest_path=ROOT/'videos/manifest.json';manifest=json.loads(manifest_path.read_text())
 state_path=ROOT/'production/render-status.json';states=json.loads(state_path.read_text()) if state_path.exists() else {}
 for case in ([args.case] if args.case else CASES):
  p=ROOT/'hyperframes'/case;logs=p/'verification';logs.mkdir(exist_ok=True)
  data=json.loads((p/'case.json').read_text());project=str(p.relative_to(ROOT))
  try:
   if args.lint_only:
    execute(cli+['lint',project,'--json'],logs/'lint.json');continue
   if legacy:
    for gate in ['lint','validate','inspect']:execute(cli+[gate,project,'--json'],logs/(gate+'.json'))
   else:execute(cli+['check',project,'--json'],logs/'check.json')
   pending=ROOT/'videos'/f'.{case}.rendering.mp4'
   execute(cli+['render',project,'--quality','high' if legacy else 'delivery','--fps','30','--workers','2','--output',str(pending)],logs/'render.log')
   facts=probe_and_decode(pending,data['duration_seconds'])
   target=ROOT/'videos'/f'{case}.en-en.hyperframes.mp4';pending.replace(target)
   samples=p/'verification/encoded';samples.mkdir(exist_ok=True)
   scenes=json.loads((p/'scene-manifest.json').read_text())['scenes']
   for i,s in enumerate(scenes):
    for phase,fraction in [('early',.2),('middle',.5),('late',.8)]:
     t=s['start']+s['duration']*fraction
     subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(target),'-frames:v','1',str(samples/f'{i+1:02}-{phase}.png')],check=True)
   record=dict(case=case,path=str(target.relative_to(ROOT)),bytes=target.stat().st_size,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),production='Native HyperFrames HTML/SVG/GSAP',hyperframes_version=version,**facts)
   old=next((x for x in manifest if x['case']==case),None)
   manifest=[record if x['case']==case else x for x in manifest]
   if old is None:manifest.append(record)
   manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
   states[case]=dict(status='rendered_and_decoded_pending_visual_and_listening_review',**record,visual_review='pending',audio_listening='pending',caption_pixel_review='pending',sampled_frames=18)
   state_path.write_text(json.dumps(states,indent=2)+'\n')
   # Keep prior exports until the new picture/audio is reviewed; no silent deletions.
   print('RENDERED '+str(target),flush=True)
  except Exception as exc:
   states[case]={'status':'failed','reason':str(exc),'hyperframes_version':version};state_path.write_text(json.dumps(states,indent=2)+'\n');raise
if __name__=='__main__':main()
