import os
import glob
import numpy as np
from skimage import io
from tqdm import tqdm
import crop
from Otsu_binarize import otsu_binarize


def main():
    # crop and resize
    if not os.path.isdir('cropped'):
        crop.main()

    # binarize
    if not os.path.isdir('binarized'):
        os.mkdir("binarized")
        print('Starting binarization...')
        for img in tqdm(os.listdir('cropped\\')):
            image = io.imread('cropped\\' + img)
            bin_img = otsu_binarize(image)
            io.imsave('binarized\\' + img, bin_img)
        print('Binarization done.')

    # list some paths
    train_pages, valid_pages = get_train_valid_page_nrs()
    train_img_paths, valid_img_paths = get_img_paths(train_pages, valid_pages)
    keywords = get_keywords()

    # the following is a proposal for the pipeline:
    # TODO: get id's of keywords from 'ground-truth/transcription.txt'

    # TODO: featurize ALL images from valid pages and store in memory -> valid_searchspace

    # TODO: for each keyword do:

        # TODO: featurize images from the train pages for this keyword

        # TODO: compare these to the valid_searchspace with DTW

        # TODO: sort list of matches / choose threshold above which to keep matches

    # TODO: calculate precision/recall


def get_train_valid_page_nrs():
    with open('task\\train.txt', 'r') as f:
        train_pages = []
        for line in f:
            train_pages.append(line)

    with open('task\\valid.txt', 'r') as f:
        valid_pages = []
        for line in f:
            valid_pages.append(line)

    return train_pages, valid_pages


def get_img_paths(train_pages, valid_pages):
    train_img_paths = []
    for page_nr in train_pages:
        train_img_paths.append(glob.glob('cropped\\' + page_nr + '*'))

    valid_img_paths = []
    for page_nr in valid_pages:
        valid_img_paths.append(glob.glob('cropped\\' + page_nr + '*'))

    return train_img_paths, valid_img_paths


def get_keywords():
    with open('task\\keywords.txt') as f:
        keywords = []
        for line in f:
            keywords.append(line)

    return keywords


if __name__ == '__main__':
    main()
