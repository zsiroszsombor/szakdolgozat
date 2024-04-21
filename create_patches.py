from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

OPENSLIDE_PATH = r'C:/Users/Zsombi/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages/openslide/openslide-bin-4.0.0.2-windows-x64/bin'

import os
if hasattr(os, 'add_dll_directory'):
    # Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        from openslide import open_slide
        import openslide
        from openslide.deepzoom import DeepZoomGenerator
else:
    from openslide import open_slide
    import openslide
    from openslide.deepzoom import DeepZoomGenerator
Image.MAX_IMAGE_PIXELS = 2823777528
slide = open_slide("masks/MSB-01771-01-02.tif")
tiles = DeepZoomGenerator(slide, tile_size=256, overlap=0, limit_bounds=False)

tile_dir = "C:/git/szakdolgozat/train/mask"
cols, rows = tiles.level_tiles[16]
for row in range(rows):
    for col in range(cols):
        tile_name = os.path.join(tile_dir, '%d_%d' % (col, row))
        print("Now saving tile with title: ", tile_name)
        temp_tile = tiles.get_tile(16, (col, row))
        temp_tile_RGB = temp_tile.convert('RGB')
        temp_tile.save(tile_name + ".tif")
        