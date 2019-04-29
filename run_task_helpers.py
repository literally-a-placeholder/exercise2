import os
import glob
from math import log
from tqdm import tqdm
import numpy as np
from Featurize import featurize
from DTW import DTWDistance


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


def get_ids_of_keyword(keyword, only_train=False):
    ids = []
    with open('ground-truth/transcription.txt', 'r') as f:
        for line in f:
            if only_train:
                if keyword in line and line.startswith('2'):
                    ids.append(line.strip()[:9])
            else:
                if keyword in line:
                    ids.append(line.strip()[:9])

    return ids


def ids_to_paths(ids):
    paths = [None]*len(ids)
    for i, one_id in enumerate(ids):
        paths[i] = 'binarized/' + one_id + '.png'
    return paths


def featurize_list(img_paths):
    featurized_list = np.zeros((len(img_paths), 4, 100))

    for i, path in enumerate(img_paths):
        featurized_list[i] = featurize(path, minmax=True)

    return featurized_list


def compare_all(keyword, featurized_valid, valid_ids, save_as_txt=False, normalize=False):
    """Compare all found samples of the given keyword against all valid words with dynamic time warping (DTW).
    Output: <keyword>.txt containing all id's of the valid words and their scores, sorted from best to worst"""
    keyword_ids = get_ids_of_keyword(keyword, only_train=True)
    valid_ids = valid_ids
    keyword_paths = ids_to_paths(keyword_ids)
    featurized_keywords = featurize_list(keyword_paths)

    result = {}
    print('\nSearching all valid words for keyword \'{}\'...'.format(keyword))
    for valid_id, valid_word in enumerate(tqdm(featurized_valid, mininterval=3)):

        valid_word_distances = [np.inf] * len(keyword_ids)
        for i, keyword_word in enumerate(featurized_keywords):
            valid_word_distances[i] = DTWDistance(keyword_word, valid_word)

        lowest_dist = min(valid_word_distances)
        result[valid_ids[valid_id]] = lowest_dist

    if save_as_txt:
        target_dir = 'results'
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        sort_result_and_save_as_txt(result, keyword, target_dir)

    return result


def sort_result_and_save_as_txt(result, keyword, target_dir):
    with open('{}/{}.txt'.format(target_dir, keyword), 'w') as f:
        for key, value in sorted(result.items(), key=lambda item: item[1], reverse=True):
            f.write('{} {}\n'.format(key, value))


def multicore_compare(keyword, valid, valid_ids):
    compare_all(keyword, valid, valid_ids, save_as_txt=True)
    print('\nResults saved in \'{}.txt\'\n'.format(keyword))
