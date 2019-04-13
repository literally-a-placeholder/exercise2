import matplotlib.pyplot as plt
from skimage import io, img_as_uint
from skimage.filters import threshold_otsu


def main():
    sample_list = ['270-01-01.png', '270-01-02.png', '270-01-03.png',
                   '270-01-04.png', '270-01-05.png', '270-01-06.png', '270-01-07.png']
    for i, img in enumerate(sample_list):
        filepath = 'otsu_sample\\' + img
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
    global_thresh = threshold_otsu(img)
    binary_global = img > global_thresh

    return img_as_uint(binary_global)


if __name__ == '__main__':
    main()
