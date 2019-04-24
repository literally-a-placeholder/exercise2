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

    # the following is a proposal for the pipeline:
    # TODO: get id's of keywords from 'ground-truth/transcription.txt'

    # TODO: featurize ALL images from valid pages and store in memory -> valid_searchspace
    featurized_valid = featurize_list(valid_img_paths)

    # TODO: for each keyword do:

        # TODO: featurize images from the train pages for this keyword

        # TODO: compare these to the valid_searchspace with DTW

        # TODO: sort list of matches / choose threshold above which to keep matches

    # TODO: calculate precision/recall


if __name__ == '__main__':
    main()
