import os
from PIL import Image
from classes.getClasses import Resolution

def resizeBgs(bg_dir):
    if Resolution.if_720:
        bg_dir = os.path.join(os.path.dirname(bg_dir), "bg")
        for filename in os.listdir(bg_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                with Image.open(os.path.join(bg_dir, filename)) as img:
                    width, height = img.size
                    if width > 1270 and height > 950 and width != height:
                        img = img.resize((1280, 960), Image.LANCZOS)
                        img = img.convert("RGB")
                        new_filename = os.path.splitext(filename)[0] + ".jpg"
                        img.save(os.path.join(bg_dir, new_filename), "JPEG", quality=100)
            if filename.endswith('.png'):
                os.remove(os.path.join(bg_dir, filename))
    
    if Resolution.if_1080:
        hi_res = os.path.join(bg_dir, "1080")
        os.makedirs(hi_res, exist_ok=True)
        
        for filename in os.listdir(bg_dir):
            if filename.endswith('.jpg'):
                with Image.open(os.path.join(bg_dir, filename)) as img:
                    img = img.resize((1920, 1440), Image.LANCZOS)
                    img = img.convert("RGB")
                    new_filename = "1080_" + os.path.splitext(filename)[0] + ".jpg"
                    img.save(os.path.join(hi_res, new_filename), "JPEG", quality=100)