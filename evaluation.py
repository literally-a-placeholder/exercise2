import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
import glob
from tqdm import tqdm


def main():
    ################################################
    path = 'norm_results/*.txt'
    files = glob.glob(path)
    auc = []
    auc_sum = []
    score = []
    zero_true_ids = False

    recall_mean = []
    precision_mean = []

    # find true IDs

    transcr = np.loadtxt('ground-truth/transcription.txt', dtype=str)

    # take only pages 300-304
    transcr = transcr[2433:, :]

    # range limit from manual evaluation of our results (see comments in 'normalize_results.py)
    # norm_res: (8.5, 11.1, 0.1) ; res: (5, 25, 1) AND CHANGE > TO < for checking the threshold on line ~64
    for i in tqdm(np.arange(8.5, 11.1, 0.1)):

        recall_all = []
        precision_all = []
        for name in files:

            # create array with sorted ids from result file
            file = np.loadtxt(name, dtype=str)

            ################################################

            #find indeces in array with the same word in transcription: split the path into the keyword.
            arr_index = np.where(transcr == name.split("\\")[-1].split(".")[0])

            #create list with true IDs:
            true_ids = []
            for idx in arr_index[0]:
                true_ids.append(transcr[idx,0])

            #keywords which are not present in the test pages
            if len(true_ids) == 0:
                zero_true_ids = True
            else:
                zero_true_ids = False

            #############################################
            #find correct ids:

            tp = 0
            tn = 0
            fp = 0

            all_positive = len(true_ids)


            #create new array with only IDs over the threshold
            file = file[np.where(np.array([float(x) for x in file[:,1]]) > i)] #todo: write >threshold

            #go through all result test IDs (from highest score to lowest)
            for test_id in file[:,0]:

                # calculate true positives:
                if test_id in true_ids:
                    tp += 1
                    score.extend(list(file[np.where(file[:, 0] == test_id), 1][0]))
                else:
                    fp += 1

            if zero_true_ids == False:
                recall = tp / all_positive
                precision = tp / (tp + fp+0.0000000001)

                recall_all.append(recall)
                precision_all.append(precision)

            #if there are zero words in the transcription file
            else:
                if tp == 0:
                    recall, precision = 1, 1
                else:
                    recall, precision = 0, 0


        recall_mean.append(np.mean(recall_all))
        precision_mean.append(np.mean(precision_all))




    print(np.mean(recall_mean), np.mean(precision_mean))

    auc = metrics.auc(recall_mean, precision_mean)
    plt.plot(recall_mean, precision_mean)
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title(auc)
    plt.show()


    #calculation of tp mean score:
    '''
    intscore = []
    for ele in score:
        intscore.append(float(ele))
    print(intscore)
    print(np.mean(intscore))
    '''


if __name__ == '__main__':
    main()