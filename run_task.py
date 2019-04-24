import os
from skimage import io
from tqdm import tqdm
import crop
from Otsu_binarize import otsu_binarize
from run_task_helpers import *


def main():
    # crop and resize
    if not os.path.isdir('cropped'):
        crop.main()

    # binarize
    if not os.path.isdir('binarized'):
        os.mkdir("binarized")
        print('Starting binarization...')
        for img in tqdm(os.listdir('cropped/')):
            filepath = 'cropped/' + img
            bin_img = otsu_binarize(filepath)
            io.imsave('binarized/' + img, bin_img)
        print('Binarization done.')

    # list some paths
    train_pages, valid_pages = get_train_valid_page_nrs()
    train_img_paths, valid_img_paths = get_img_paths(train_pages, valid_pages)
    keywords = get_keywords()

    # featurize ALL images from valid pages and store to use for all keywords
    featurized_valid = featurize_list(valid_img_paths)

    # for each keyword compare to all valid words and save results in <keyword>.txt
    print('\nCompute all distances of each keyword to each word of the valid pages...\n')
    for keyword in tqdm(keywords):
        compare_all(keyword, featurized_valid, save_as_txt=True)
        print('\nResults saved in \'{}.txt\'\n'.format(keyword))

    # TODO: calculate precision/recall


if __name__ == '__main__':
    main()
