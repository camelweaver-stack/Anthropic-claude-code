import subprocess, wave, os, struct, math

# Output goes into the current work dir (or RENDER_OUT) as <slug>.mp4 — stage_kit.py then moves it
# into <queue>/READY_<slug>/. Set RENDER_SLUG to the episode slug so the filename matches the kit.
SLUG=os.environ.get('RENDER_SLUG','west-fw-rent-report-august-2026')
OUTDIR=os.environ.get('RENDER_OUT', os.getcwd())
OUT=os.path.join(OUTDIR, SLUG + '.mp4')

# sentence-level synthesis with engineered pauses
# (pause seconds after each sentence; longer at section transitions and before key numbers)
script = [
 # (text, pause_after)
 ("The West Fort Worth Rent Report.", 0.45),
 ("August, twenty twenty six.", 0.7),
 ("From West F W Living \u2014 the west side's independent field guide.", 0.6),
 ("Ninety seconds. Four numbers. One move to make this month.", 1.1),
 ("First \u2014 the Concession Index.", 0.65),
 ("Across the tracked communities of the Willow Park corridor, the average advertised move-in special now stands at\u2026 seven point five weeks free.", 0.8),
 ("Olympus, and Willow Crossing \u2014 eight weeks.", 0.45),
 ("Gates \u2014 seven.", 0.45),
 ("Canvas \u2014 six to eight, depending on the plan, and the lease length.", 0.7),
 ("When properties pay this much to fill units\u2026 renters hold the leverage.", 1.2),
 ("Second \u2014 what a one bedroom actually costs, pocket by pocket.", 0.75),
 ("White Settlement \u2014 roughly nine hundred, to twelve hundred dollars.", 0.5),
 ("And one major platform now tracks rents there down thirteen percent, year over year.", 0.75),
 ("The I-thirty corridor \u2014 eleven hundred to fourteen fifty.", 0.45),
 ("Benbrook \u2014 eleven hundred to fourteen hundred.", 0.45),
 ("Willow Park and Hudson Oaks \u2014 eleven fifty to fifteen hundred\u2026 before the free weeks.", 1.2),
 ("Third \u2014 the number that matters more than any sticker price.", 0.55),
 ("Effective rent.", 0.7),
 ("Take the total cost of the lease\u2026 and divide by the months.", 0.6),
 ("Fourteen fifty a month, with eight weeks free\u2026 is really twelve twenty seven.", 0.8),
 ("That gap \u2014 over two hundred dollars a month \u2014 is the difference between shopping the way the office wants\u2026 and shopping the way the market allows.", 1.2),
 ("The move this month.", 0.6),
 ("Get every quote in writing. For your unit. Your dates. And a twelve month term.", 0.7),
 ("Then compare properties on effective rent \u2014 and only effective rent.", 0.7),
 ("In a market giving away six to eight weeks\u2026 the sticker price is an opening offer.", 1.2),
 ("The full tables, the fine print decoder, and the calculator, are free \u2014 at west F W living, dot com.", 0.6),
 ("Updated monthly. Nobody will call you.", 0.55),
 ("See you in September.", 0.4),
]
# section boundaries by sentence index (frame changes): f1 ends after idx3, f2 after idx9, f3 after idx15, f4 after idx20, f5 after idx24, f6 to end
bounds=[3,9,15,20,24,27]

RATE=22050
def silence_wav(path, secs):
    n=int(RATE*secs)
    with wave.open(path,'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(b'\x00\x00'*n)

parts=[]; durs=[]
for i,(txt,pause) in enumerate(script):
    fn=f'p{i:02d}.wav'
    subprocess.run(['piper','-m','en_US-ryan-high.onnx','--length-scale','1.06','-f',fn], input=txt.encode(), check=True, capture_output=True)
    with wave.open(fn) as wv:
        d=wv.getnframes()/wv.getframerate()
        if wv.getframerate()!=RATE:
            subprocess.run(['ffmpeg','-y','-i',fn,'-ar',str(RATE),f'r{fn}'],check=True,capture_output=True); os.replace(f'r{fn}',fn)
            with wave.open(fn) as wv2: d=wv2.getnframes()/wv2.getframerate()
    sn=f'q{i:02d}.wav'; silence_wav(sn, pause)
    parts += [fn, sn]; durs.append(d+pause)
with open('alist2.txt','w') as f:
    for p_ in parts: f.write(f"file '{p_}'\n")
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','alist2.txt','-af','loudnorm=I=-17:TP=-1.5,highpass=f=70,equalizer=f=220:t=q:w=1.2:g=1.5,equalizer=f=4200:t=q:w=1.5:g=1.2','narration2.wav'], check=True, capture_output=True)
# frame durations from sentence groups
fd=[]; prev=0
for b in bounds:
    fd.append(sum(durs[prev:b+1])); prev=b+1
with open('vlist2.txt','w') as f:
    for i,dur in enumerate(fd,1): f.write(f"file 'f{i}.png'\nduration {dur:.3f}\n")
    f.write("file 'f6.png'\n")
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','vlist2.txt','-i','narration2.wav','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','medium','-crf','20','-c:a','aac','-b:a','160k','-shortest',OUT], check=True, capture_output=True)
print("v2 assembled:", round(sum(fd),1), "s |", os.path.getsize(OUT)//1024//1024, "MB | frames:", [round(x,1) for x in fd], "->", OUT)
