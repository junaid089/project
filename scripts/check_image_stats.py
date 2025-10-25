from PIL import Image
import os

paths = [
    'media/generated/gen_aa170c0c.jpg',
    'media/generated/gen_80fda6d3.jpg',
]
for p in paths:
    if not os.path.exists(p):
        print(p, 'MISSING')
        continue
    im = Image.open(p).convert('RGB')
    w,h = im.size
    pixels = im.load()
    # sample pixels
    samples = [pixels[min(w-1, x), min(h-1,y)] for x,y in [(10,10),(50,50),(w//2,h//2),(w-10,h-10)]]
    avg = tuple(sum(c for c in comps)//len(samples) for comps in zip(*samples))
    print(p, 'size', im.size, 'sample_pixels', samples, 'avg', avg)
