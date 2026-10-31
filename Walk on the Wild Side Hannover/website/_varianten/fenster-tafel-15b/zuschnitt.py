import sys, os, json
from PIL import Image, ImageOps
C=os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/_quelle/vom-kunden/')
OUT=sys.argv[1]; BAND=sys.argv[2]; os.makedirs(OUT,exist_ok=True); os.makedirs(BAND,exist_ok=True)
L=[
 ('tafel-gedeckt','drive/4972.jpg',.55),
 ('runde-von-oben','drive/3901.jpg',.55),
 ('tafel-im-raum','drive/4004.jpg',.58),
 ('blick-durch-die-tuer','drive/3859.jpg',.62),
 ('momo-am-tisch','3986.jpg',.45),
 ('applaus-kerzen','5022.jpg',.3),
 ('platz-gedeckt','drive/4075.jpg',.5),
 ('durch-die-wand','drive/4029.jpg',.55),
 ('fenster-nacht','drive/3998.jpg',.5),
 ('fenster-aussen','drive/4951.jpg',.45),
 ('kerzen-koch','drive/4894.jpg',.5),
 ('koch-erzaehlt-hell','drive/4365.jpg',.28),
 ('gaeste-am-fenster','drive/4398.jpg',.3),
 ('rote-drinks','4024.jpg',.3),
 ('koch-am-tisch-warm','drive/36913.jpg',.4),
 ('tafel-kerzen-frau','drive/3916.jpg',.45),
 ('koch-kerzentisch','drive/36543.jpg',.5),
]
info=[]
for name,q,my in L:
    im=ImageOps.exif_transpose(Image.open(C+q)).convert('RGB'); w,h=im.size
    cw=w; ch=round(w/1.6)
    y=min(max(0,round(my*h-ch/2)),h-ch)
    c=im.crop((0,y,cw,y+ch)); c.save(os.path.join(OUT,name+'.jpg'),quality=92)
    s=max(1000/c.width,650/c.height); v=c.resize((round(c.width*s),round(c.height*s)),Image.LANCZOS)
    x=(v.width-1000)//2; yy=(v.height-650)//2; v=v.crop((x,yy,x+1000,yy+650)).crop((0,107,1000,543))
    v.save(os.path.join(BAND,name+'.jpg'),quality=88)
    info.append((name,c.width,c.height,'Culinarium Hannover/_quelle/vom-kunden/'+q))
json.dump(info,open(os.path.join(OUT,'herkunft.json'),'w'),ensure_ascii=False,indent=1)
print(len(info))
