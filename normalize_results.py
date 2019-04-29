import os
import numpy as np


def main():
    for file in os.listdir('results'):
        f = np.loadtxt('results/'+file, dtype=str)
        normalize_values(f)

        if not os.path.isdir('norm_results/'):
            os.mkdir('norm_results/')
        np.savetxt('norm_results/'+file, f, fmt='%s %s')

    # to manually get the min and max of all the values!  'tmp = []' in front of the loop, tmp.append(f) inside
    # min(np.asarray(list(chain.from_iterable(f))[1::2]).astype(float))  :  8.53885310048419
    # max(np.asarray(list(chain.from_iterable(f))[1::2]).astype(float))  :  11.058616415666572


def normalize_values(results_arr):
    """Normalize the score values to sum up to 1, then transform with abs(log(x)) to get rid of small values."""
    scores = results_arr[:, 1].astype(float)
    scores = abs(np.log2(scores / np.sum(scores)))
    results_arr[:, 1] = scores


if __name__ == '__main__':
    main()
