import os
import glob
import numpy as np
import matplotlib.pyplot as plt

from tifffile import imread, imsave
from csbdeep.utils import Path, normalize
from csbdeep.utils.tf import keras_import
from csbdeep.data import Normalizer, normalize_mi_ma
keras = keras_import()

from stardist import export_imagej_rois, random_label_cmap
from stardist.models import StarDist2D


class Scale_Norm(Normalizer):
    def __init__(self, mi, ma):
        self.mi, self.ma = mi, ma
    def before(self, x, axes):
        return normalize_mi_ma(x, self.mi, self.ma, dtype=np.float32)
    def after(*args, **kwargs):
        assert False
    @property
    def do_after(self):
        return False


mi, ma = 0, 255
normalizer = Scale_Norm(mi,ma)
np.random.seed(0)
cmap = random_label_cmap()
model = StarDist2D.from_pretrained("2D_versatile_he")

data_dir = "data"
mask_dir = "masks"
svs_files = glob.glob(os.path.join(data_dir, "*.svs"))

for svs_file in svs_files:
    img = imread(svs_file)
    labels, palys = model.predict_instances_big(img, axes='YXC', block_size=4096, min_overlap=128, context=128, normalizer=normalizer, n_tiles=(4,4,1))
    output_file = os.path.splitext(os.path.basename(svs_file))[0] + ".tif"
    output_path = os.path.join(mask_dir, output_file)
    imsave(output_path, labels)