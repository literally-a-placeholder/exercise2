import numpy as np
from PIL import Image


def main():
    print(featurize("dummy270-19.png"))


def featurize(img):
    img = np.asarray(Image.open(img))

    feature_mat = np.zeros((4, 100))
    func_list = [lower_contour, upper_contour, bw_transitions, fraction_of_bw_between_uclc]

    for i, func in enumerate(func_list):
        feature_mat[i] = np.apply_along_axis(func, axis=1, arr=img)

    return feature_mat


# __________ feature calculations __________
def lower_contour(img_col):
    result = 0
    zeros_indices = np.where(img_col == 0)[0]
    if zeros_indices.size != 0:
        result = np.amax(zeros_indices)
    return result


def upper_contour(img_col):
    result = img_col.size
    zeros_indices = np.where(img_col == 0)[0]
    if zeros_indices.size != 0:
        result = np.amin(zeros_indices)
    return result


def bw_transitions(img_col):
    old_val = img_col[0]
    transitions = 0
    for val in img_col:
        if val != old_val:
            transitions += 1
        old_val = val
    return transitions


def fraction_of_bw_between_uclc(img_col):
    result = 0
    upp = upper_contour(img_col)
    low = lower_contour(img_col)
    between_uclc = img_col[upp:low+1]
    if between_uclc.size != 0:
        result = np.count_nonzero(between_uclc) / between_uclc.size
    return result
# __________________________________________


if __name__ == "__main__":
    main()
