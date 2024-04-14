import os
vipsbin = r'c:\vips-dev-8.15\bin'
add_dll_dir = getattr(os, 'add_dll_directory', None)
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ['PATH'] = os.pathsep.join((vipsbin, os.environ['PATH']))

import wsi_preprocessing as pp

# if, for instance, CMU-1.svs is in your current directory:
slides = pp.list_slides(r"C:\Users\Zsombi\Downloads\PKG - Biobank_CMB-CRC_v3\CMB-CRC")

pp.save_slides_mpp_otsu(slides, "slides_mpp_otsu.csv")

# this may take some minutes, depending on your local machine
pp.run_tiling("slides_mpp_otsu.csv", "tiles.csv")

pp.calculate_filters("slides_mpp_otsu.csv", "", "tiles_filters.csv")