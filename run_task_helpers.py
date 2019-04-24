import glob
from tqdm import tqdm
import numpy as np
from Featurize import featurize


def get_train_valid_page_nrs():
    with open('task/train.txt', 'r') as f:
        train_pages = []
        for line in f:
            train_pages.append(line.rstrip('\n'))

    with open('task/valid.txt', 'r') as f:
        valid_pages = []
        for line in f:
            valid_pages.append(line.rstrip('\n'))

    return train_pages, valid_pages


def get_img_paths(train_pages, valid_pages):
    train_img_paths = []
    for page_nr in train_pages:
        train_img_paths += glob.glob('binarized/' + page_nr + '*')

    valid_img_paths = []
    for page_nr in valid_pages:
        valid_img_paths += glob.glob('binarized/' + page_nr + '*')

    return train_img_paths, valid_img_paths


def get_keywords():
    with open('task/keywords.txt') as f:
        keywords = []
        for line in f:
            keywords.append(line.rstrip('\n'))

    return keywords


def featurize_list(img_paths):
    featurized_list = np.zeros((len(img_paths), 4, 100))

    print('Featurize multiple images...')
    for i, path in tqdm(enumerate(img_paths)):
        featurized_list[i] = featurize(path, minmax=True)

    return featurized_list


def compare_all(keyword, featurized_keyword_samples, featurized_valid):
    pass
