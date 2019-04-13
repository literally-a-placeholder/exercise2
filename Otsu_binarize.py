import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_uint
from skimage.color import rgba2rgb, rgb2gray
from skimage.filters import threshold_otsu


# low bin counts results in finer lines but also fragmentation of originally already fine lines
# high bin counts result in bolder lines but also sometimes filling of the counter (the 'hole') of a letter
NBINS = 42

def main():
    if not os.path.isdir('otsu_sample'):
        os.mkdir('otsu_sample')

    sample_list = ['270-01-01.png', '270-01-02.png', '270-01-03.png',
                   '270-01-04.png', '270-01-05.png', '270-01-06.png', '270-01-07.png']
    for i, img in enumerate(sample_list):
        filepath = 'cropped\\' + img
        image = io.imread(filepath)

        binary_global = otsu_binarize(image)

        fig, axes = plt.subplots(nrows=2, figsize=(7, 8))
        ax = axes.ravel()
        plt.gray()

        ax[0].imshow(image)
        ax[0].set_title('Original')

        ax[1].imshow(binary_global)
        ax[1].set_title('Global thresholding')

        for a in ax:
            a.axis('off')

        io.imsave('otsu_sample\\otsu_' + img, binary_global)
        io.imsave('otsu_sample\\' + img, image)

    plt.show()


def otsu_binarize(img):
    img = rgba2rgb(img)
    img = rgb2gray(img)
    global_thresh = threshold_otsu(img, nbins=NBINS)
    binary_global = img > global_thresh
    # convert to uint8 array and use numpy's fancy indexing to get rid of the empty channels
    binary_global = np.uint8(binary_global * 255)
    return binary_global


if __name__ == '__main__':
    main()
