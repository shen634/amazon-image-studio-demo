from rembg import remove
from PIL import Image
import numpy as np
import os
import csv

def bbox_ratio(alpha):
    ys, xs = np.where(alpha > 10)
    if len(xs) == 0:
        return 0.0
    xmin, xmax = xs.min(), xs.max()
    ymin, ymax = ys.min(), ys.max()
    w = xmax - xmin + 1
    h = ymax - ymin + 1
    return (w * h) / (alpha.shape[0] * alpha.shape[1])

def process_image(in_path, out_dir, sku="sku"):
    # load and remove bg
    img = Image.open(in_path).convert("RGBA")
    rgba = remove(np.array(img))
    img_rgba = Image.fromarray(rgba).convert("RGBA")
    alpha = np.array(img_rgba.split()[-1])
    ratio = bbox_ratio(alpha)
    # resize rules
    w,h = img_rgba.size
    target = 2000
    min_side = 1000
    scale = target / max(w,h)
    if max(w,h) < min_side:
        scale = min_side / max(w,h)
    new_w = max(1, int(w*scale)); new_h = max(1, int(h*scale))
    img_resized = img_rgba.resize((new_w,new_h), Image.LANCZOS)
    # create white canvas
    canvas = Image.new("RGB", (target, target), (255,255,255))
    x = (target - new_w)//2; y = (target - new_h)//2
    canvas.paste(img_resized.convert("RGB"), (x,y), img_resized.split()[-1])
    out_name = f"{sku}_{os.path.basename(in_path).rsplit('.',1)[0]}.jpg"
    out_path = os.path.join(out_dir, out_name)
    canvas.save(out_path, format="JPEG", quality=90, optimize=True)
    report_name = f"{out_name}.report.csv"
    report_path = os.path.join(out_dir, report_name)
    with open(report_path,'w',newline='',encoding='utf-8') as f:
        wcsv = csv.writer(f)
        wcsv.writerow(['src','dst','foreground_ratio'])
        wcsv.writerow([in_path, out_path, ratio])
    return out_path, report_path
