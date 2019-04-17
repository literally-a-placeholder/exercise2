import numpy as np
from Featurize import featurize

def DTWDistance(features1, features2, sakoe_chiba_bandwidth = 40):
    n = features1.shape[1]
    m = features2.shape[1]

    dtw = np.full((n+1,m+1), np.inf)
    dtw[0,0] = 0

    for a in range(n):
        i = a + 1
        for b in range(m):
            j = b + 1
            if (max(i-j, j-i) > sakoe_chiba_bandwidth/2):
                continue
            cost = np.linalg.norm(features1[:,a] - features2[:,b])
            dtw[i,j] = cost + min(dtw[i-1,j], dtw[i-1,j-1], dtw[i,j-1])

    return dtw[n,m]