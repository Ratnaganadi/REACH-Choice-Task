import sys
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

for fn in fns:
    math_diffs = {'staircase':[], 'choice':[]}
    dots_diffs = {'staircase':[], 'choice':[]}
    music_diffs = {'staircase':[], 'choice':[]}
    spatial_diffs = {'staircase':[], 'choice':[]}

    math_scores = {'staircase':[], 'choice':[]}
    dots_scores = {'staircase':[], 'choice':[]}
    music_scores = {'staircase':[], 'choice':[]}
    spatial_scores = {'staircase':[], 'choice':[]}
    
    main = pd.read_excel(fn, 'Main')
    
    for task_name, scores, diffs in [('Math',math_scores,math_diffs),('Dots',dots_scores,dots_diffs),('Spatial',spatial_scores,spatial_diffs),('Music',music_scores,music_diffs)]:
        tn = main[main.Game==task_name]['Trial Number'].values
        for i,val in enumerate(tn):
            if i==0: continue
            elif val!=tn[i-1]+1:
                choice_tn = val
                break
        scores['staircase'].append( main[(main.Game==task_name) & (main['Trial Number']<tn[i])].Score.values )
        diffs['staircase'].append( main[(main.Game==task_name) & (main['Trial Number']<tn[i])].Difficulty.values )
        scores['choice'].append( main[(main.Game==task_name) & (main['Trial Number']>=tn[i])].Score.values )
        diffs['choice'].append( main[(main.Game==task_name) & (main['Trial Number']>=tn[i])].Difficulty.values )
        #scores.append( main[(main.Game==task_name)].Score.values )
        #diffs.append( main[(main.Game==task_name)].Difficulty.values )
        

    plt.figure()
    p=1
    for task_name, score_set, diff_set in [('Math',math_scores,math_diffs),('Dots',dots_scores,dots_diffs),('Spatial',spatial_scores,spatial_diffs),('Music',music_scores,music_diffs)]:
        fig = plt.subplot(2,2,p)
        for subj, stair_scores, choice_scores, stair_diffs, choice_diffs in zip(range(len(score_set)), score_set['staircase'], score_set['choice'], diff_set['staircase'], diff_set['choice']):
            stair_correct = [(i,diff) for i,diff in enumerate(stair_diffs) if stair_scores[i]==1]
            stair_incorrect = [(i,diff) for i,diff in enumerate(stair_diffs) if stair_scores[i]==0]
            fig.plot([x[0] for x in stair_correct], [x[1] for x in stair_correct], 'go')
            fig.plot([x[0] for x in stair_incorrect], [x[1] for x in stair_incorrect], 'ro')
            #fig.plot(len(stair_diffs)-1, stair_diffs[-1], 'bo')
            fig.plot(range(len(stair_diffs)), stair_diffs,  'k-', color='0.5')
            plt.axvline(x=len(stair_diffs)-0.5, ls='-.', color='0.7')
        
            choice_correct = [(i+len(stair_diffs),diff) for i,diff in enumerate(choice_diffs) if choice_scores[i]==1]
            choice_incorrect = [(i+len(stair_diffs),diff) for i,diff in enumerate(choice_diffs) if choice_scores[i]==0]
            fig.plot([x[0] for x in choice_correct], [x[1] for x in choice_correct], 'go')
            fig.plot([x[0] for x in choice_incorrect], [x[1] for x in choice_incorrect], 'ro')
            fig.plot([x+len(stair_diffs) for x in range(len(choice_diffs))], choice_diffs,  'k-', color='0.5')
        
            plt.xlabel('Trial Number')
            plt.ylabel('Difficulty')
            plt.xlim([-0.5,len(stair_diffs)+len(choice_diffs)])
            yrange = max(stair_diffs)-min(stair_diffs)
            plt.ylim([min(stair_diffs)-(0.1*yrange), max(stair_diffs)+(0.1*yrange)])
            plt.title(task_name)
            
        p+=1
        plt.tight_layout()
plt.show()