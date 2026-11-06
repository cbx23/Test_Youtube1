from PIL import Image, ImageDraw, ImageFont
import math, subprocess, wave, struct, pathlib

OUT = pathlib.Path('output'); OUT.mkdir(exist_ok=True)
W,H,FPS,DURATION=1280,720,30,30
BG='#0b1022'; WHITE='#f1f5ff'; MUTED='#9eacc8'; CYAN='#5ce5dd'; GOLD='#ffd38b'
def font(n,bold=False): return ImageFont.truetype('C:/Windows/Fonts/'+('seguisb.ttf' if bold else 'segoeui.ttf'),n)
fonts={n:font(n) for n in (19,22,26,30,36)}
fonts[54]=font(54,True); fonts[42]=font(42,True)
base=Image.new('RGB',(W,H)); pix=base.load()
for y in range(H):
 for x in range(W):
  glow=max(0,1-math.hypot((x-980)/1100,(y-210)/650))
  pix[x,y]=(int(10+9*glow),int(15+15*glow),int(32+29*glow))
scenes=[
 ('Cum funcționează un agent AI?','De la un obiectiv la un rezultat, pas cu pas.','UN EXEMPLU ÎN 30 DE SECUNDE'),
 ('1. Primește un obiectiv','Tu spui ce vrei și stabilești limitele.','OBIECTIV'),
 ('2. Împarte sarcina în pași','Agentul propune un plan pentru a atinge obiectivul.','PLANIFICARE'),
 ('3. Folosește instrumente','Caută informații și lucrează cu datele găsite.','ACȚIUNE'),
 ('4. Verifică și ajustează','Dacă informațiile nu sunt suficiente, caută din nou.','VERIFICARE'),
 ('5. Îți prezintă rezultatul','Tu verifici propunerea și decizi ce folosești.','REZULTAT')]
def ease(v): v=max(0,min(1,v)); return 1-(1-v)**3
def render(t):
 im=base.copy(); d=ImageDraw.Draw(im); s=min(5,int(t/5)); u=t-s*5
 def txt(x,y,text,size=26,color=WHITE,center=False):
  f=fonts[size]
  if center: x-=d.textlength(text,font=f)/2
  d.text((x,y),text,font=f,fill=color)
 def box(x,y,w,h,label,accent=CYAN,small=None):
  d.rounded_rectangle((x,y,x+w,y+h),radius=20,fill='#17233b',outline=accent,width=2)
  txt(x+w/2,y+(h-40)/2-(15 if small else 0),label,30,WHITE,True)
  if small: txt(x+w/2,y+h/2+20,small,19,MUTED,True)
 def arrow(x1,y1,x2,y2):
  d.line((x1,y1,x2,y2),fill=CYAN,width=3)
  a=math.atan2(y2-y1,x2-x1)
  d.polygon([(x2,y2),(x2-12*math.cos(a-.5),y2-12*math.sin(a-.5)),(x2-12*math.cos(a+.5),y2-12*math.sin(a+.5))],fill=CYAN)
 def orb(x,y,r=60):
  rr=r+int(4*math.sin(t*3))
  d.ellipse((x-rr-10,y-rr-10,x+rr+10,y+rr+10),outline='#294e68',width=2)
  d.ellipse((x-r,y-r,x+r,y+r),fill='#194351',outline=CYAN,width=3)
  txt(x,y-25,'AI',36,CYAN,True)
 txt(64,38,'AGENT AI / DEMO',19,CYAN)
 txt(1215,38,f'{s+1:02d} / 06',19,MUTED,True)
 txt(64,108,scenes[s][2],19,CYAN)
 shift=int(25*(1-ease(u/.65)))
 txt(64,150+shift,scenes[s][0],54)
 txt(64,226+shift,scenes[s][1],26,MUTED)
 if s==0:
  labels=['Obiectiv','Plan','Acțiune','Verificare','Rezultat']
  for i,label in enumerate(labels):
   x=64+i*237; active=u>i*.55
   box(x,355,205,125,label,CYAN if active else '#34425f')
   if i<4: arrow(x+211,418,x+230,418)
  txt(640,527,'Un model AI + instrumente + o buclă de lucru',30,GOLD,True)
 elif s==1:
  box(80,335,770,185,'„Găsește 3 idei de clipuri despre spațiu.”',small='Public: începători  •  Include surse  •  Nu publica automat')
  arrow(875,428,990,428); orb(1090,428)
 elif s==2:
  items=[('01','Caută subiecte'),('02','Compară sursele'),('03','Alege 3 idei')]
  for i,(num,label) in enumerate(items):
   yy=315+i*88; xx=180+int(50*(1-ease((u-i*.45)/.6)))
   box(xx,yy,920,70,label,CYAN if u>i*.7 else '#34425f'); txt(xx+25,yy+18,num,26,CYAN)
 elif s==3:
  orb(230,427,74)
  for i,label in enumerate(['Căutare web','Citirea paginilor','Notițe + surse']):
   yy=310+i*100; arrow(330,427,680,yy+37); box(700,yy,420,75,label)
   p=(u*.65-i*.27)%1; x=330+350*p; y=427+(yy+37-427)*p
   d.ellipse((x-6,y-6,x+6,y+6),fill=GOLD)
  txt(230,542,'În limitele accesului acordat',19,MUTED,True)
 elif s==4:
  box(85,350,315,130,'Verifică sursele'); box(495,350,315,130,'Sunt suficiente?'); box(905,350,290,130,'Pregătește ideile')
  arrow(414,415,480,415); arrow(825,415,890,415); txt(850,380,'DA',19,CYAN,True)
  d.line((650,490,650,555,240,555,240,495),fill=GOLD,width=3)
  txt(448,567,'NU → repetă căutarea',22,GOLD,True)
 elif s==5:
  for i,(label,sub) in enumerate([('De ce strălucesc stelele?','Ideea 01'),('Cum apar eclipsele?','Ideea 02'),('Ce este o gaură neagră?','Ideea 03')]):
   x=64+i*393; box(x,330,365,165,sub)
   txt(x+182,426,label,22,WHITE,True)
  txt(640,535,'Agentul poate greși. Verifică informațiile și sursele.',26,GOLD,True)
 d.line((64,642,1216,642),fill='#29344c',width=3)
 d.line((64,642,64+1152*t/DURATION,642),fill=CYAN,width=4)
 txt(64,663,'OBIECTIV → PLAN → ACȚIUNE → VERIFICARE → REZULTAT',19,MUTED)
 txt(1185,663,f'{int(t):02d}s',19,MUTED,True)
 fade=min(1,u/.25,(5-u)/.25)
 if fade<1: im=Image.blend(base,im,max(0,fade))
 return im

rate=44100
with wave.open(str(OUT/'ambient.wav'),'w') as wav:
 wav.setparams((1,2,rate,0,'NONE','not compressed'))
 data=bytearray()
 for i in range(rate*DURATION):
  t=i/rate; chord=[(130.81,164.81,196),(110,130.81,164.81),(87.31,130.81,174.61)][int(t/5)%3]
  env=min(1,t/1.5,(DURATION-t)/2)
  v=sum(math.sin(2*math.pi*f*t) for f in chord)*.025
  beat=t%.5; v+=.035*math.exp(-beat*20)*math.sin(2*math.pi*523.25*t)
  data.extend(struct.pack('<h',int(32767*v*env)))
 wav.writeframes(data)
cmd=['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'ambient.wav'),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-shortest',str(OUT/'agent-ai-demo.mp4')]
with open(OUT/'render.log','w') as log:
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 for i in range(FPS*DURATION):
  p.stdin.write(render(i/FPS).tobytes())
 p.stdin.close()
 if p.wait(): raise RuntimeError('ffmpeg failed; see render.log')
render(3).save(OUT/'preview.jpg')
thumb=Image.new('RGB',(640*3,360*2))
for s in range(6): thumb.paste(render(s*5+2.5).resize((640,360)),((s%3)*640,(s//3)*360))
thumb.save(OUT/'storyboard.jpg')
print(OUT/'agent-ai-demo.mp4')
