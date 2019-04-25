import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
import glob


################################################
path = 'results/*.txt'
files = glob.glob(path)
auc = []
score = []

transcr = np.loadtxt('ground-truth/transcription.txt', dtype=str)

# take only pages 300-304
transcr = transcr[2433:, :]

for name in files:

    # create array with sorted ids from result file
    file = np.loadtxt(name, dtype=str)

    ################################################
    #find true IDs

    #find indeces in array with the same word in transcription: split the path into the keyword.
    arr_index = np.where(transcr == name.split("\\")[-1].split(".")[0])

    #create list with true IDs:
    true_ids = []
    for idx in arr_index[0]:
        true_ids.append(transcr[idx,0])

    #calculate auc only for the words with at least 1 solution.
    if len(true_ids) != 0:

        #############################################
        #find correct ids:

        tp = 0
        tn = 0
        fp = 0
        all_positive = len(true_ids)
        until_now_ids = []
        recall_all = []
        precision_all = []
        quality = []

        #go through all result test IDs (from highest score to lowest)
        for test_id in file[:,0]:

            until_now_ids.append(test_id)

            # calculate true positives:
            if test_id in true_ids:
                tp += 1

                score.extend(list(file[np.where(file[:,0] == test_id),1][0]))

            # calculate false positives (result id not in true_ids):
            fp_ids = [x for x in until_now_ids if x not in true_ids]
            fp = len(fp_ids)

            # if the word hasn't been found yet:
            if tp == 0:
                recall = 0
                precision = 0

            else:
                recall = tp / all_positive
                precision = tp / (tp + fp)

            recall_all.append(recall)
            precision_all.append(precision)

        wordauc = metrics.auc(recall_all, precision_all)
        if wordauc != 0:
            auc.append(metrics.auc(recall_all, precision_all))
        #explaination: it isn't possible that the auc is 0, because there is at least one solution
        #metrics.auc isn't able to recognize that and would give a auc of 0 insteat of 1.
        else:
            auc.append(1)

        #plot the auc graph with axis= precision and recall
        '''
        plt.plot(recall_all, precision_all)
        plt.xlabel('recall')
        plt.ylabel('precision')
        plt.show()
        '''


print('mean auc = ', np.mean(auc))

#calculation of tp mean score:
'''
intscore = []
for ele in score:
    intscore.append(float(ele))
print(intscore)
print(np.mean(intscore))
'''
