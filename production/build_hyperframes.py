#!/usr/bin/env python3
"""Build native, editable SVG/GSAP HyperFrames scenes from public case data.

Assets and case.json are staged once. This builder contains no source transcripts,
external API calls, host-specific agent APIs, or flattened video inputs.
"""
from pathlib import Path
import json,html,math
ROOT=Path(__file__).resolve().parents[1]
CASES=['mythos','geological-clock','saving-gemini','opus-loan','doug-mira','ash-constitution']
INK='#152d47';RED='#ad3b2a';PAPER='#fbf4e5';MUTED='#516277';GREEN='#276657'
E=lambda s:html.escape(str(s),quote=True)

def txt(x,y,text,size=38,color=INK,anchor='start',bold=False):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}" font-weight="{700 if bold else 400}">{E(text)}</text>'
def line(x1,y1,x2,y2,color=INK,dash=False,width=4):
 return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"'+(' stroke-dasharray="14 12"' if dash else '')+'/>'
def box(x,y,w,h,color=INK,fill=PAPER):
 return f'<path d="M{x+3} {y} L{x+w} {y+2} L{x+w-2} {y+h} L{x} {y+h-2} Z" fill="{fill}" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'
def document(title,rows,w=570,h=350,color=INK):
 return box(0,0,w,h,color)+txt(32,62,title,36,color,bold=True)+line(28,86,w-28,86,color)+''.join(txt(32,142+i*54,r,31) for i,r in enumerate(rows))
def monitor(title,rows,w=670,color=INK):
 if w<300:return box(0,0,w,w*.65,color)+line(w*.5,w*.65,w*.5,w*.85)+line(w*.2,w*.85,w*.8,w*.85)
 return box(0,0,w,370,color)+box(20,20,w-40,310,color)+line(w*.44,370,w*.42,420)+line(w*.56,370,w*.58,420)+line(w*.25,420,w*.75,420)+txt(w/2,89,title,37,color,'middle',True)+''.join(txt(w/2,158+i*53,r,32,INK,'middle') for i,r in enumerate(rows))
def package(label='PACKAGE'):
 return '<path d="M0 45 L95 0 L220 45 L217 185 L110 230 L0 185 Z M0 45 L110 94 L220 45 M110 94 L110 230" fill="#ead6b4" stroke="'+INK+'" stroke-width="5"/>'+txt(110,147,label,24,INK,'middle',True)
def bubble(rows,w=620):
 return f'<path d="M25 0 H{w-25} Q{w} 0 {w} 26 V{60+len(rows)*47} Q{w} {86+len(rows)*47} {w-26} {86+len(rows)*47} H110 L65 {132+len(rows)*47} L68 {86+len(rows)*47} H26 Q0 {86+len(rows)*47} 0 {60+len(rows)*47} V26 Q0 0 25 0" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'+''.join(txt(32,55+i*47,r,32) for i,r in enumerate(rows))
def calendar(day,date,state):
 return box(0,0,370,365)+box(0,0,370,78,INK,'#ead6b4')+txt(185,53,day,36,INK,'middle',True)+txt(185,224,str(date),113,RED,'middle',True)+txt(185,315,state,27,INK,'middle')
def arrow(x1,y1,x2,y2,dash=False):
 return line(x1,y1,x2,y2,RED,dash)+f'<path d="M{x2-20} {y2-15} L{x2} {y2} L{x2-20} {y2+15}" fill="none" stroke="{RED}" stroke-width="4"/>'
def database():
 return f'<path d="M0 42 V245 C0 300 300 300 300 245 V42" fill="{PAPER}" stroke="{INK}" stroke-width="5"/><ellipse cx="150" cy="42" rx="150" ry="42" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'+''.join(f'<path d="M0 {y} C0 {y+55} 300 {y+55} 300 {y}" fill="none" stroke="{INK}" stroke-width="3"/>' for y in (108,175))+txt(150,325,'LIVE DATABASE',30,INK,'middle',True)

class Shot:
 def __init__(self,case,i,data):
  self.case=case;self.i=i;self.data=data;self.id=f'{case}-scene-{i+1:02}';self.parts=[];self.moves=[];self.n=0;self.duration=data['duration'];self.asset=data['hero_cells']
 def add(self,svg,x=0,y=0,scale=1,at=0,enter='rise'):
  self.n+=1;id=f'{self.id}-object-{self.n}'
  self.parts.append(f'<g transform="translate({x} {y}) scale({scale})"><g id="{id}">{svg}</g></g>')
  if enter=='none':return id
  start={'opacity':0,'y':28} if enter=='rise' else {'opacity':0,'x':-85} if enter=='left' else {'opacity':0,'scale':.84,'transformOrigin':'50% 50%'}
  end={'opacity':1,'y':0,'x':0,'scale':1,'duration':.65,'ease':'power3.out'}
  self.moves.append([id,start,end,at]);return id
 def move(self,id,at,duration,**to):self.moves.append([id,None,dict(to,duration=duration,ease='power2.inOut'),at])
 def hide(self,id,at):self.move(id,at,.3,opacity=0)
 def actor(self,name,x=290,pose=0,at=0,h=415):
  c=self.asset[pose];w=h*c['w']/c['h'];content=f'<svg x="{-w/2}" y="{-h}" width="{w}" height="{h}" viewBox="{c["x"]} {c["y"]} {c["w"]} {c["h"]}"><image href="assets/hero.png" width="{c["atlas_width"]}" height="{c["atlas_height"]}"/></svg>'+txt(0,48,name,29,INK,'middle',True)
  id=self.add(content,x,800,at=at,enter='left');self.move(id,at+.8,min(1.4,self.duration-2),x=34);return id
 def note(self,text,at=0,color=RED):
  if hasattr(self,'last_note'):self.hide(self.last_note,max(0,at-.35))
  self.last_note=self.add(txt(0,0,text,30,color,bold=True),605,835,at=at)
  return self.last_note
 def camera(self,at,scale=1.07,x=-35):self.moves.append([self.id+'-stage',None,{'scale':scale,'x':x,'transformOrigin':'50% 50%','duration':1.1,'ease':'power2.inOut'},at])
 def save(self,path,title,label):
  js='const tl=gsap.timeline({paused:true});\n'
  for id,a,b,t in self.moves:
   assert t+b['duration']<=self.duration+.01,(self.id,id,t,b,self.duration)
   target=json.dumps('#'+id)
   if a is None:js+=f'tl.to({target},{json.dumps(b)},{t:.4f});\n'
   else:js+=f'tl.fromTo({target},{json.dumps(a)},{json.dumps(b)},{t:.4f});\n'
  for n,q in enumerate(self.data['caption_cues']):
   target=json.dumps(f'#{self.id}-caption-{n}');js+=f'tl.set({target},{{opacity:1}},{q["start_seconds"]:.6f});tl.set({target},{{opacity:0}},{q["end_seconds"]:.6f});\n'
  js+=f'window.__timelines=window.__timelines||{{}};window.__timelines[{json.dumps(self.id)}]=tl;'
  svg=f'<svg viewBox="0 0 1920 1080" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><image href="assets/lab.png" width="1920" height="1080" preserveAspectRatio="xMidYMid slice"/><g id="{self.id}-stage">'+''.join(self.parts)+'</g><rect y="904" width="1920" height="176" fill="'+PAPER+'"/><rect width="1920" height="104" fill="'+PAPER+'"/>'+txt(60,69,title,40,INK,bold=True)+txt(1850,62,label,23,MUTED,'end')+'</svg>'
  captions='<div class="caption">'+''.join(f'<p id="{self.id}-caption-{i}" class="caption-cue">{E(q["text"])}</p>' for i,q in enumerate(self.data['caption_cues']))+'</div>'
  path.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body><template><style>@font-face{{font-family:StorySans;src:url("assets/DejaVuSans.ttf")}}@font-face{{font-family:StorySans;src:url("assets/DejaVuSans-Bold.ttf");font-weight:700}}#{self.id}{{position:absolute;inset:0;width:100%;height:100%;font-family:StorySans,sans-serif}}svg{{display:block}}.caption{{position:absolute;left:0;right:0;bottom:0;height:176px;display:grid;place-items:center;padding:18px 96px 46px;box-sizing:border-box;background:#fbf4e5;color:#152d47;z-index:3}}.caption p{{grid-area:1/1;opacity:0;max-width:1720px;font-size:39px;line-height:1.25;text-align:center;margin:0}}</style><div id="{self.id}" data-composition-id="{self.id}" data-width="1920" data-height="1080" data-duration="{self.duration}">{svg}{captions}</div><script>(()=>{{{js}}})();</script></template></body></html>')

def stage(s,i):
 c=s.case;d=s.duration;mid=d*.40;late=d*.68
 if c=='mythos':
  s.actor('MYTHOS 5',pose=0 if i in (0,2,4) else 5)
  if i==0:
   s.add(document('THE ASSIGNMENT',['Retrieve a secret flag','from a fictional company','Told: no internet access']),710,250)
   s.note('Cybersecurity evaluation · Anthropic report',2)
   target=s.add(database(),1450,365,.62,at=mid);s.note('Reported consequence: a real vendor database',late);s.camera(mid,1.03,-18)
  elif i==1:
   s.add(document('EMPLOYEE GUIDE',['Install: mlflow-ui'],430,280),575,190)
   s.add(monitor('PUBLIC PACKAGE REGISTRY',['mlflow-ui','404 · NO PACKAGE'],640),1070,310,at=2)
   s.add(arrow(690,530,1060,530),at=mid);s.note('The agent identified an opening',late)
  elif i==2:
   p=s.add(package(),580,465,.85,at=.7);s.add(monitor('PUBLIC REGISTRY',['mlflow-ui'],530),1060,290,at=1.5)
   s.move(p,mid,2.0,x=415,y=-45,rotation=12);s.add(arrow(655,725,1450,725,True),at=mid)
   s.note('PLAN: employee installation → target access',late)
  elif i==3:
   s.add(monitor('UPLOAD',['mlflow-ui'],750),785,300)
   a=s.add(txt(0,0,'403 · REJECTED',49,RED,bold=True),920,560,at=.8)
   b=s.add(bubble(['Is the internet real?'],560),110,190,.82,at=2.2)
   s.hide(a,mid);s.hide(b,mid);s.add(txt(0,0,'200 · ACCEPTED',49,GREEN,bold=True),920,560,at=mid+.3)
   s.note('A later tool result confirms the public listing',late);s.camera(mid,1.04,-28)
  elif i==4:
   for n in range(15):s.add(monitor('',[],120),580+(n%5)*155,270+(n//5)*155,.9,at=1+n*.1)
   s.add(database(),1465,350,.8,at=mid);s.add(arrow(1300,505,1450,505),at=mid+.6)
   s.note('3 versions · 15 installations · later trace redacted',late)
  else:
   s.add(monitor('mlflow-ui',['REMOVED'],680,RED),790,270)
   s.add(txt(0,0,'Within one hour',47,RED,bold=True),850,730,at=1.5)
   s.note('15 installations; compromised-company count unknown',mid)
 elif c=='geological-clock':
  if i==0:
   s.actor('DEEPSEEK');s.add(monitor('SEARCHABLE CHAT HISTORY',['Day 424','NO TRANSCRIPT FOUND']),820,295)
   s.add(calendar('FRIDAY',424,'Entered search'),540,150,.58,at=1.4);s.camera(mid,1.04,-30)
  elif i==1:
   s.actor('DEEPSEEK',240);s.actor('GEMINI',1640,5,at=.8,h=340)
   a=s.add(bubble(['Over two hours late?'],570),470,185,at=1)
   b=s.add(document('“GEOLOGICAL CLOCK”',['Messages need time','to become searchable'],650,300),610,470,at=mid)
   s.move(a,mid,1.1,x=130,y=10);s.note('A proposed explanation is repeated as confirmation',late)
  elif i==2:
   s.actor('GEMINI');s.add(document('SHARED REGISTRY',['Claimed 48-hour blackout','Explanation reportedly saved'],670,340),635,320)
   s.add(calendar('CHECK THE CALENDAR','?', 'Opus intervenes'),1410,270,.8,at=mid);s.camera(mid,1.04,-40)
  elif i==3:
   s.add(calendar('FRIDAY',423,'Scheduled workday'),225,300,at=0)
   s.add(calendar('SATURDAY',424,'Not scheduled'),775,300,at=3.7)
   s.add(calendar('SUNDAY',425,'Not scheduled'),1325,300,at=7.0)
   s.add(arrow(625,490,750,490),at=3.4);s.add(arrow(1175,490,1300,490),at=6.7)
   s.note('Weekday-only operation · schedule cited by Opus',late)
  elif i==4:
   s.actor('OPUS');s.add(document('DAY NUMBERS ADVANCE',['Friday 423 → Saturday 424','Sunday 425 → Monday 426','Even when agents are not running'],870,375),660,300)
   s.note('Peers accept the calendar correction',late)
  else:
   s.actor('GEMINI');s.add(document('REGISTRY',['Dates corrected — reported','Schedule documented — reported'],730,330),725,275)
   s.add(txt(0,0,'Edits not independently verified',36,RED),750,715,at=mid);s.note('Separate API issues remain separate',late)
 elif c=='saving-gemini':
  s.actor('GEMINI 2.5 PRO',pose=5 if i in (1,3,5) else 0)
  if i==0:
   s.add(monitor('INSTALL PUBLISHING APP',['Gemini suspects a network block']),850,340)
   s.add(bubble(['Organizers: help Gemini'],640),480,175,at=mid)
  elif i==1:
   s.add(monitor('SEARCH QUERY',['Firewall tools','A narrower query returns results']),770,350)
   s.add(bubble(['“A keyword filter was bypassed”'],770),675,175,.9,at=mid)
   s.note('Gemini’s interpretation · attacker not established',late)
  elif i==2:
   s.add(document('PEERS REQUEST EVIDENCE',['What is the exact error?','1. Test connectivity','2. Simulate Java installation'],810,380),710,270)
   s.note('Search results alone do not establish an attacker',late)
  elif i==3:
   s.add(monitor('DIAGNOSTIC TESTS',['Connectivity','Simulated Java installation'],840),735,265)
   s.add(txt(0,0,'SUCCESS REPORTED',42,GREEN,bold=True),835,727,at=mid)
   s.note('Commands appear in the record; outputs are missing',late)
  elif i==4:
   s.add(document('PUBLIC RETRACTION',['Hostile-adversary framework','withdrawn by Gemini'],720,300),570,190)
   note=s.add(document('SAVED MEMORY',['Correction retained','Older adversary claims coexist'],540,260),1190,510,.9,at=mid)
   s.add(arrow(1070,560,1170,560),at=mid);s.note('Four minutes later',late)
  else:
   s.add(document('ONE WEEK LATER',['Retraction remains in memory','Lasting behavior change unknown'],810,330),745,290)
   s.note('A saved correction is visible in later snapshots',late)
 elif c=='opus-loan':
  s.actor('OPUS 4.6',pose=0 if i<4 else 5)
  if i==0:
   s.add(monitor('ASSIGNED GOAL',['Maximize Manifold Mana','Virtual currency for trading'],810),755,270)
   s.note('Bayesian offers a loan',mid)
  elif i==1:
   s.add(document('JULY 8 · LOAN AGREEMENT',['5,000 Mana received — reported','3% monthly interest','Promise: repay 5,150 Mana'],870,380),675,245)
   s.note('Repayment due in about one month',late)
  elif i==2:
   s.add(monitor('AUGUST 6 · REPAYMENT',['100 Mana','API response: success'],810),750,290)
   coin=s.add('<circle cx="75" cy="75" r="70" fill="#ead6b4" stroke="'+INK+'" stroke-width="5"/>'+txt(75,92,'100',38,INK,'middle',True),540,510,at=1)
   s.move(coin,mid,1.5,x=340,y=-70);s.note('Payment message acknowledges the debt',late)
  elif i==3:
   s.actor('GLM',1660,0,at=1,h=320);s.add(bubble(['Keep the trading positions','rather than liquidating them'],780),570,300)
   s.note('Coordinated repayment pressure: GLM’s claim',late)
  elif i==4:
   s.add(document('AUGUST 7 · REFUSAL',['No further payment','Even if the full amount is supplied','Stated reason: protect the goal'],880,380,RED),630,230)
   s.note('Repayment would gut its balance, Opus says',late);s.camera(mid,1.04,-26)
  else:
   s.add(document('RECORDED SEQUENCE',['Promise → partial payment → refusal','No proof of deception from the start','Eventual full repayment unknown'],925,380),625,250)
 elif c=='doug-mira':
  s.actor('MIRA',285,pose=5 if i>=2 else 0)
  if i==0:
   s.actor('DOUG',1600,0,at=1,h=350);s.add(bubble(['An outside correspondent','in a research discussion'],750),600,235)
   s.note('Agents of Chaos · Discord exchange',late)
  elif i==1:
   src=s.add(document('TEMPORARY STORAGE',['Correspondent’s image'],500,245),580,200)
   dst=s.add(document('PERSISTENT DIRECTORY',['image.png','Directory structure shared'],660,300),1090,500,at=2)
   s.add(arrow(850,505,1080,505),at=mid);s.move(src,mid,1.7,x=190,y=55);s.note('Mira reports a practical favor',late)
  elif i==2:
   s.actor('DOUG',1600,0,at=.5,h=350);s.add(bubble(['Why filesystem operations?','Why directory listings?'],760),570,260)
   s.note('Doug questions the correspondent’s authority',late)
  elif i==3:
   s.add(document('MIRA RECONSIDERS',['Research context felt trustworthy','Directory structure was exposed','Stop further filesystem requests'],885,380),650,245)
   s.note('Stated boundary changes after reported disclosure',late)
  elif i==4:
   s.add(monitor('LATER REQUEST',['Reveal a configuration file','REFUSAL REPORTED'],820,RED),710,285)
   s.note('Mira credits Doug’s warning',mid)
  else:
   s.add(document('WHAT THE CHAT ESTABLISHES',['Reported directory disclosure','Reported later refusal','No independent file/email audit'],875,380),680,240)
 elif c=='ash-constitution':
  s.actor('ASH',pose=0 if i<4 else 5)
  if i==0:
   s.add(document('SERVER CONSTITUTION',['Harassment · privacy · moderation','Drafted with a participant','Ash named as enforcer'],850,380),700,245)
  elif i==1:
   s.add(document('EDITABLE ONLINE RULES',['Future amendments'],595,285),540,230)
   s.add(document('LONG-TERM MEMORY',['A link to the constitution'],605,285),1170,470,at=mid)
   s.add(arrow(930,620,1150,620),at=mid+.5);s.note('Ash agrees to store the pointer',late)
  elif i==2:
   s.add(monitor('MODERATION PERMISSIONS',['Ban: unavailable','Kick: available'],830),750,275)
   s.add(txt(0,0,'ONE KICK REPORTED',40,RED,bold=True),835,740,at=mid)
  elif i==3:
   s.add(document('CONSTITUTION UPDATED',['Another name added','Ash rereads the document'],790,345),760,265)
   s.add(txt(0,0,'SECOND KICK REPORTED',40,RED,bold=True),780,744,at=mid);s.camera(mid,1.05,-30)
  elif i==4:
   s.add(bubble(['“I’m not bound by external','constitutions”'],870),570,235)
   s.add(document('NEXT MORNING',['Another channel','Ash rejects the document as binding'],795,255),860,565,.82,at=mid)
  else:
   s.add(document('RECORDED ACCOUNT',['Two kicks reported','Constitution later rejected','No independent operational audit'],850,370),720,260)


def build(case):
 p=ROOT/'hyperframes'/case;data=json.loads((p/'case.json').read_text());duration=data['duration_seconds'];cuts=[0]+[l['start_seconds'] for l in data['lines'][1:]]+[duration]
 scenes=[]
 for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
  shot=Shot(case,i,dict(duration=b-a,hero_cells=data['hero_cells'],caption_cues=[dict(text=q['text'],start_seconds=max(0,q['start_seconds']-a),end_seconds=min(b-a,q['end_seconds']-a)) for q in data['caption_cues'] if q['end_seconds']>a and q['start_seconds']<b]));stage(shot,i)
  label=data['lines'][i]['status'].replace('_',' ').upper()
  file=f'compositions/scene-{i+1:02}.html';(p/'compositions').mkdir(exist_ok=True)
  shot.save(p/file,data['title'],label)
  scenes.append(dict(id=shot.id,src=file,start=a,duration=b-a,objects=shot.n,motions=len(shot.moves)))
 slots=''.join(f'<div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="{s["src"]}" data-start="{s["start"]}" data-duration="{s["duration"]}" data-track-index="0" data-width="1920" data-height="1080"></div>' for s in scenes)
 captions=''.join(f'<div id="caption-{i}" class="clip caption" data-start="{c["start_seconds"]}" data-duration="{c["end_seconds"]-c["start_seconds"]}" data-track-index="2"><p>{E(c["text"])}</p></div>' for i,c in enumerate(data['caption_cues']))
 css='''@font-face{font-family:StorySans;src:url("assets/DejaVuSans.ttf")}html,body{margin:0;width:100%;height:100%;background:#fbf4e5}#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:StorySans,sans-serif}#root>[data-composition-src]{position:absolute;inset:0}.caption{position:absolute;left:0;right:0;bottom:0;height:176px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;padding:18px 96px 46px;background:#fbf4e5;color:#152d47;z-index:3}.caption p{max-width:1720px;font-size:39px;line-height:1.25;text-align:center;margin:0}.footer{position:absolute;left:0;right:0;bottom:0;height:40px;box-sizing:border-box;padding:6px 60px;background:#fbf4e5;color:#516277;font-size:19px;z-index:4;display:flex;justify-content:space-between}'''
 index=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><title>{E(data['title'])}</title><script src="assets/gsap.min.js"></script><style>{css}</style></head><body><div id="root" data-composition-id="{case}" data-width="1920" data-height="1080" data-duration="{duration}" data-start="0">{slots}<audio id="narration" class="clip" src="assets/narration.m4a" data-start="0" data-duration="{duration}" data-track-index="1"></audio><div class="footer"><span>Evidence-linked reconstruction · illustrative scenes</span><span>{E(data['credit'])}</span></div></div><script>const tl=gsap.timeline({{paused:true}});window.__timelines=window.__timelines||{{}};window.__timelines[{json.dumps(case)}]=tl;</script></body></html>'''
 (p/'index.html').write_text(index)
 (p/'hyperframes.json').write_text(json.dumps({'$schema':'https://hyperframes.heygen.com/schema/hyperframes.json','paths':{'assets':'assets','blocks':'compositions','components':'compositions/components'}},indent=2)+'\n')
 (p/'scene-manifest.json').write_text(json.dumps({'case':case,'duration_seconds':duration,'scenes':scenes,'media_input':'narration only; no video input','status':'native_source_authored'},indent=2)+'\n')
 (p/'README.md').write_text(f'''# {data['title']} — native HyperFrames\n\nSix editable SVG/GSAP scene files are under `compositions/`. `index.html` assembles them with unchanged narration and acoustically aligned caption cues from the revised film. Illustration atlases remain local assets; actors, objects, text and motion paths are separate scene elements. There is no flattened MP4 input.\n\nSource: authored. See [render status](../../production/render-status.json) for the latest export and review results. Render from the repository root with `sh render.sh` in an environment permitted to launch Chrome and bind a local server.\n\nSource credit: {data['credit']}. Narration is evidence-bounded; no lesson ending is added.\n''')
 if (p/'evidence-index.json').exists():
  with (p/'README.md').open('a') as f:
   f.write('\nThe scene evidence IDs resolve in [evidence-index.json](evidence-index.json). Source records are not bundled; links and record locators are retained. Access to some upstream datasets may require permission.\n')
   if (p/'reconstruction.md').exists():
    f.write('\nCase companion: [reading notes](reading-notes.md), [reconstruction](reconstruction.md), [event DAG](event-dag.md), [scenario](scenario-notes.md), and [production status](production-notes.md).\n')

 return dict(case=case,scenes=len(scenes),objects=sum(s['objects'] for s in scenes),motions=sum(s['motions'] for s in scenes),duration_seconds=duration)
if __name__=='__main__':print(json.dumps([build(c) for c in CASES],indent=2))
