import sys, json, os
from PIL import Image, ImageOps, ImageFilter, ImageStat
C=os.path.expanduser('~/Desktop/Website-Projekte/Culinarium Hannover/_quelle')
W=os.path.expanduser('~/Desktop/Website-Projekte/Walk on the Wild Side Hannover/_quelle')
OUT=sys.argv[1]
# (name, quelle, vertikale Mitte des 16:10-Ausschnitts 0..1, horizontale Mitte)
L=[
 ('anstossen-kerzen', C+'/vom-kunden/drive/5376.jpg', .4, .5),
 ('drink-kraeuter', C+'/vom-kunden/drive/5289.jpg', .4, .5),
 ('koch-kerzen', C+'/vom-kunden/drive/63990.jpg', .22, .5),
 ('runde-stoesst-an', C+'/vom-kunden/drive/4574.jpg', .4, .5),
 ('gast-am-teller', C+'/vom-kunden/drive/5041.jpg', .5, .5),
 ('dessert-tafel', C+'/ki/geschaerft/2025-06-15_highlight-6684-10-geschaerft.jpg', .5, .5),
 ('glaeser-tafel', W+'/google-maps/google-17.jpg', .5, .5),
 ('raum-abend', W+'/google-maps/google-07.jpg', .58, .5),
 ('momo-mixt-gast', C+'/vom-kunden/drive/4568.jpg', .34, .5),
 ('drink-nische', C+'/vom-kunden/drive/63741.jpg', .5, .5),
 ('rose-glas', C+'/vom-kunden/drive-arw-vorschau/5406.jpg', .5, .5),
 ('theke-gaeste', W+'/google-maps/google-28.jpg', .5, .5),
 ('drinks-tisch', W+'/google-maps/google-29.jpg', .4, .5),
 ('cocktail-flasche', C+'/vom-kunden/drive/4558.jpg', .5, .5),
 ('koch-am-tisch', C+'/vom-kunden/drive/5301.jpg', .22, .5),
]
info=[]
for name, q, my, mx in L:
    im=ImageOps.exif_transpose(Image.open(q)).convert('RGB'); w,h=im.size
    cw=w; ch=round(w/1.6)
    if ch>h: ch=h; cw=round(h*1.6)
    x=min(max(0,round(mx*w-cw/2)),w-cw); y=min(max(0,round(my*h-ch/2)),h-ch)
    c=im.crop((x,y,x+cw,y+ch))
    if c.width>3200: c=c.resize((3200,round(3200/1.6)),Image.LANCZOS)
    c.save(os.path.join(OUT,name+'.jpg'),quality=90)
    g=c.convert('L'); g.thumbnail((900,900)); sh=ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).var[0]
    info.append((name,c.width,c.height,round(sh),os.path.relpath(q,os.path.expanduser('~/Desktop/Website-Projekte'))))
json.dump(info,open(os.path.join(OUT,'herkunft.json'),'w'),ensure_ascii=False,indent=1)
for i in info: print(i)
