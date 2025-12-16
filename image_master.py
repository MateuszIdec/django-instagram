from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

def convertImage(image):
    print("\n\n Converting Image... \n\n")

    img = Image.open(image)
    img = img.convert("RGB")

    source_size = img.size
    source_size_max = max(source_size)
    source_size_min = min(source_size)
    source_proportions: float = float(source_size_max) / source_size_min

    resolutions = [1920, 1280, 640]
    imgs = []

    for r in resolutions:
        crop_ratio = source_size_max / r
        new_size = (int(source_size[0] * crop_ratio), int(source_size[1] * crop_ratio))

        new_img = img.copy()
        new_img = new_img.resize(new_size, Image.Resampling.LANCZOS)

        # zapisujemy do pamięci jako WebP
        temp_io = BytesIO()
        new_img.save(temp_io, format='WEBP')

        # generujemy nazwę pliku
        base_name = os.path.splitext(os.path.basename(getattr(image, 'name', 'image')))[0]
        new_name = f"{base_name}_{new_size[0]}x{new_size[1]}.webp"

        # tworzymy ContentFile, gotowy do zapisania w ImageField
        imgs.append(ContentFile(temp_io.getvalue(), name=new_name))
    
    # zwracamy dwa mniejsze obrazy (1280 i 640)
    return imgs[2], imgs[1], imgs[0]
