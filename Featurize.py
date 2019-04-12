import numpy as np
from PIL import Image


def featurize(img):
    # RETURN
    #   feature-matrix
    img = np.asarray(Image.open(img))

    # WORK IN PROGRESS
    np.apply_along_axis()



# __________ feature calculations __________
def lower_contour(slice):
    pass


def upper_contour(slice):
    pass


def bw_transitions(slice):
    pass


def fraction_of_bw_between_LCUC(slice):
    pass

# __________________________________________
