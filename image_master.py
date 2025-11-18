# Tutaj jest skrypt na przetwarzanie obrazów

from PIL import Image
import os

# To zmieniamy ewentualnie
filename = 'example.png'

img = Image.open(filename)
img = img.convert("RGB")

source_size = img.size
source_size_max = max(source_size)
source_size_min = min(source_size)

source_proportions:float = float(source_size_max) / source_size_min

resolutions = [1920, 1280, 640]
sizes = []

print(source_size)
print(source_proportions)

for r in resolutions:
    crop_ratio = source_size_max / r
    new_size = (int(source_size[0] * crop_ratio), int(source_size[1] * crop_ratio))

    print(new_size)    

    new_w = new_size[0]
    new_h = new_size[1]
    new_filename = f"{os.path.splitext(os.path.basename('/path/to/file.txt'))[0]}_{new_w}_{new_h}.webp"

    new_img = img.copy()
    new_img = new_img.resize(new_size, Image.Resampling.LANCZOS)
    new_img.save(new_filename, 'webp')