from PIL import Image, ImageDraw, ImageFont
import os

# build_video.py — renders the six episode frames (f1..f6, 1920x1080) + thumbnail.png (1280x720).
# Narration + assembly live in build_v2.py (the proven pipeline), which reads these f*.png files.
# Adapt the text/numbers each month; keep the layout. Run this first, then build_v2.py, then stage_kit.py.

PAPER=(247,245,239); INK=(24,32,25); HEDGE=(47,107,79); WHEAT=(217,164,65); SOFT=(90,97,87); LINE=(220,216,204)
W,H=1920,1080

# Resolve fonts relative to THIS script (runs from any cwd) with a cross-platform mono fallback.
# The bundled serif/sans travel with the skill; mono is a system font that differs per OS.
HERE=os.path.dirname(os.path.abspath(__file__))
OUTDIR=os.environ.get('RENDER_OUT', os.getcwd())   # thumbnail lands here; frames stay in cwd for build_v2.py
def _font(paths, size):
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except Exception: continue
    return ImageFont.load_default()
serif=lambda s: _font([os.path.join(HERE,'playfair.ttf')], s)
sans =lambda s: _font([os.path.join(HERE,'instrument.ttf')], s)
mono =lambda s: _font([
    os.path.join(HERE,'mono.ttf'),                                   # optional bundled mono
    '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',           # linux
    'C:\\Windows\\Fonts\\consola.ttf', 'C:\\Windows\\Fonts\\cour.ttf',  # windows
    '/System/Library/Fonts/Menlo.ttc', '/System/Library/Fonts/Monaco.ttf',  # macOS
    os.path.join(HERE,'instrument.ttf'),                             # last resort: never crash
], s)

def base(kicker):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,8], fill=HEDGE)
    d.text((80,50), "WEST FW LIVING", font=mono(30), fill=HEDGE)
    d.text((80,95), kicker, font=mono(24), fill=SOFT)
    d.text((W-560,58), "westfwliving.com", font=mono(28), fill=SOFT)
    return im,d

def bar(d,x,y,w,h,color,label,val,lf,vf):
    d.text((x,y+h//2-16), label, font=lf, fill=INK)
    d.rounded_rectangle([x+430,y,x+430+w,y+h], 10, fill=color)
    d.text((x+450+w,y+h//2-16), val, font=vf, fill=INK)

# S1 title
im,d=base("MONTHLY MARKET BRIEFING")
d.text((80,330),"The West Fort Worth", font=serif(110), fill=INK)
d.text((80,460),"Rent Report", font=serif(110), fill=HEDGE)
d.text((80,640),"August 2026", font=sans(56), fill=SOFT)
d.text((80,850),"90 seconds \u00b7 four numbers \u00b7 one move to make this month", font=sans(40), fill=INK)
im.save('f1.png')

# S2 concession index
im,d=base("THE CONCESSION INDEX \u00b7 AUGUST")
d.text((80,180),"7.5", font=serif(300), fill=HEDGE)
d.text((560,320),"average advertised weeks free,\ntracked west-side communities", font=sans(48), fill=INK)
y=620
for label,wd,val,col in [("Olympus Willow Park",760,"8 wks",HEDGE),("Willow Crossing",760,"8 wks*",HEDGE),("Gates at Meadow Place",660,"7 wks",(61,122,93)),("Canvas at Willow Park",610,"6\u20138 wks*",WHEAT)]:
    bar(d,80,y,wd,54,col,label,val,sans(38),mono(38)); y+=88
d.text((80,H-90),"*conditional \u2014 varies by unit, plan, and lease length", font=sans(30), fill=SOFT)
im.save('f2.png')

# S3 rent bands
im,d=base("1BR ASKING RENTS \u00b7 BY POCKET")
d.text((80,160),"What a one-bedroom costs,", font=serif(72), fill=INK)
d.text((80,255),"pocket by pocket", font=serif(72), fill=HEDGE)
y=420
for label,wd,val,col in [("White Settlement",520,"$900\u2013$1,200",HEDGE),("West FW \u00b7 I-30 corridor",640,"$1,100\u2013$1,450",(61,122,93)),("Benbrook",620,"$1,100\u2013$1,400",(74,138,107)),("Willow Park / Hudson Oaks",700,"$1,150\u2013$1,500",WHEAT)]:
    bar(d,80,y,wd,58,col,label,val,sans(38),mono(40)); y+=100
d.text((80,H-160),"White Settlement: one major platform tracks rents DOWN ~13% year-over-year", font=sans(36), fill=INK)
d.text((80,H-100),"bands compiled from public listings \u00b7 before concessions", font=sans(28), fill=SOFT)
im.save('f3.png')

# S4 effective rent receipt
im,d=base("THE NUMBER THAT MATTERS \u00b7 EFFECTIVE RENT")
d.rounded_rectangle([80,200,1100,820],18, outline=LINE, width=3, fill=(255,255,255))
d.text((140,260),"Advertised rent", font=sans(44), fill=INK); d.text((760,260),"$1,450 /mo", font=mono(44), fill=INK)
d.text((140,370),"8 weeks free", font=sans(44), fill=INK); d.text((760,370),"\u2212 $2,677", font=mono(44), fill=HEDGE)
d.line([140,480,1040,480], fill=LINE, width=3)
d.text((140,540),"Effective rent", font=sans(52), fill=INK); d.text((700,530),"$1,227 /mo", font=mono(56), fill=HEDGE)
d.text((140,700),"\u2014 total lease cost \u00f7 months. always. \u2014", font=mono(34), fill=SOFT)
d.text((1200,380),"The $223/mo gap is\nthe difference between\nshopping like the office wants\u2026", font=sans(46), fill=INK)
d.text((1200,650),"\u2026and shopping like\nthe market allows.", font=serif(54), fill=HEDGE)
im.save('f4.png')

# S5 the move
im,d=base("THE MOVE THIS MONTH")
d.text((80,220),"Get every quote in writing \u2014", font=serif(84), fill=INK)
d.text((80,330),"your unit, your dates, 12 months.", font=serif(84), fill=INK)
d.text((80,520),"Then compare on effective rent only.", font=serif(84), fill=HEDGE)
d.text((80,780),"In a market giving away 6\u20138 weeks,", font=sans(48), fill=INK)
d.text((80,850),"the sticker price is an opening offer.", font=sans(48), fill=INK)
im.save('f5.png')

# S6 outro
im,d=base("FREE \u00b7 INDEPENDENT \u00b7 UPDATED MONTHLY")
d.text((80,300),"The full tables. The fine-print", font=serif(80), fill=INK)
d.text((80,405),"decoder. The calculator.", font=serif(80), fill=INK)
d.text((80,600),"westfwliving.com", font=mono(84), fill=HEDGE)
d.text((80,800),"Nobody will call you. See you in September.", font=sans(46), fill=SOFT)
im.save('f6.png')

# THUMBNAIL (1280x720, big-number style) — youtube-publish picks this up as thumbnail.png.
# Adapt the hero number + captions each month, same as the frames.
TW,TH=1280,720
tim=Image.new('RGB',(TW,TH),PAPER); td=ImageDraw.Draw(tim)
td.rectangle([0,0,TW,10], fill=HEDGE)
td.text((60,50),"WEST FW LIVING", font=mono(30), fill=HEDGE)
td.text((60,92),"THE CONCESSION INDEX", font=mono(24), fill=SOFT)
td.text((55,150),"7.5", font=serif(340), fill=HEDGE)
td.text((60,560),"weeks free, west-side average", font=sans(46), fill=INK)
td.text((640,220),"The West Fort Worth", font=serif(64), fill=INK)
td.text((640,300),"Rent Report", font=serif(64), fill=HEDGE)
td.text((640,410),"August 2026", font=sans(40), fill=SOFT)
td.text((640,470),"90 seconds \u00b7 four numbers", font=sans(36), fill=INK)
tim.save(os.path.join(OUTDIR,'thumbnail.png'))
print("frames + thumbnail rendered ->", OUTDIR)
