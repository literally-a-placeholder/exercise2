import os
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

from skimage import io


def main():
    if not os.path.isdir('otsu_sample'):
        os.mkdir('otsu_sample')

    sample_list = ['270-01-01.png', '270-01-02.png', '270-01-03.png',
                   '270-01-04.png', '270-01-05.png', '270-01-06.png', '270-01-07.png']
    for i, img in enumerate(sample_list):
        filepath = './otsu_sample/' + img
        image = io.imread(filepath)

        binarized_image = otsu_binarize(filepath)

        fig, axes = plt.subplots(nrows=2, figsize=(7, 8))
        ax = axes.ravel()
        plt.gray()

        ax[0].imshow(image)
        ax[0].set_title('Original')

        ax[1].imshow(binarized_image)
        ax[1].set_title('Global thresholding')

        for a in ax:
            a.axis('off')

        io.imsave('otsu_sample/otsu_' + img, binarized_image)
        io.imsave('otsu_sample/' + img, image)

    plt.show()


def otsu_binarize(filepath):
    img = cv.imread(filepath, cv.IMREAD_UNCHANGED)
    img = make_background_white(img)

    blur = cv.GaussianBlur(img, (5, 5), 0)  # apply gaussian filter to remove noise from the picture
    threshold, dst = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # apply otsu threshold
    binary_global = img > threshold
    binarized_image = np.uint8(binary_global * 255)

    return binarized_image


def make_background_white(img):
    alpha_channel = img[:, :, 3]
    _, mask = cv.threshold(alpha_channel, 254, 255, cv.THRESH_BINARY)  # binarize mask
    color = img[:, :, :3]
    new_img = cv.bitwise_not(cv.bitwise_not(color, mask=mask))
    img = cv.cvtColor(new_img, cv.COLOR_BGR2GRAY)
    return img

if __name__ == '__main__':
    main()
