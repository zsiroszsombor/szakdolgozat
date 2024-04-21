import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from tifffile import imread, imsave
from csbdeep.utils import Path, normalize
from csbdeep.utils.tf import keras_import
from csbdeep.data import Normalizer, normalize_mi_ma
from keras.preprocessing import image
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

data_dir = "train/image"
mask_dir = "train/mask"
data_list = glob.glob(os.path.join(data_dir, "*.tif"))

for data in data_list:
    img = imread(data)
    labels, palys = model.predict_instances(img, axes='YXC')
    output_file = os.path.splitext(os.path.basename(data))[0] + ".tif"
    output_path = os.path.join(mask_dir, output_file)
    imsave(output_path, labels)