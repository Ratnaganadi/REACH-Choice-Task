import pandas as pd
import numpy as np
from scipy import mean, std
import matplotlib.pyplot as plt

dir = '/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/data/'
fns = ['03_2014_Mar_10_1132.xls', '02_2014_Mar_07_1209.xls', 'test_erik_2014_Feb_26_1018.xls',
    '01_2014_Feb_20_1000.xls', '04_2014_Mar_11_1058.xls', #'05_2014_Mar_11_1417.xls', 
    '07_2014_Mar_11_1440.xls', '08_2014_Mar_12_1459.xls', '09_2014_Mar_12_1601.xls',
    '10_2014_Mar_13_1228.xls', '11_2014_Mar_13_1328.xls', '12_2014_Mar_27_1521.xls']
fns = [dir+fn for fn in fns]

math_diffs = []
dots_diffs = []
music_diffs = []
spatial_diffs = []

math_scores = []
dots_scores = []
music_scores = []
spatial_scores = []

for fn in fns:
    main = pd.read_excel(fn, 'Main')
    
    for task_name, scores, diffs in [('Math',math_scores,math_diffs),('Dots',dots_scores,dots_diffs),('Spatial',spatial_scores,spatial_diffs),('Music',music_scores,music_diffs)]:
        tn = main[main.Game==task_name]['Trial Number'].values
        for i,val in enumerate(tn):
            if i==0: continue
            elif val!=tn[i-1]+1:
                choice_tn = val
                break
        scores.append( main[(main.Game==task_name) & (main['Trial Number']<choice_tn)].Score.values )
        diffs.append( main[(main.Game==task_name) & (main['Trial Number']<choice_tn)].Difficulty.values )
        

#plt.figure(figsize=(8,6), dpi=100)
#fig = plt.subplot(111)
p=1
for task_name, score_set, diff_set in [('Math',math_scores,math_diffs),('Dots',dots_scores,dots_diffs),('Spatial',spatial_scores,spatial_diffs),('Music',music_scores,music_diffs)]:
    fig = plt.subplot(2,2,p)
    for subj, scores, diffs in zip(range(len(score_set)), score_set, diff_set):
        correct = [(i,diff) for i,diff in enumerate(diffs) if scores[i]]
        incorrect = [(i,diff) for i,diff in enumerate(diffs) if not scores[i]]
        fig.plot([x[0] for x in correct], [x[1] for x in correct], 'go')
        fig.plot([x[0] for x in incorrect], [x[1] for x in incorrect], 'ro')
        fig.plot(range(len(diffs)), diffs,  '-')
        plt.xlabel('Trial Number')
        plt.ylabel('Difficulty')
        plt.title(task_name)
    p+=1
#plt.tight_layout()
plt.show()