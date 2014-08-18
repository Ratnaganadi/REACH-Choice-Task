import pandas as pd
import numpy as np
from scipy import mean, std
import matplotlib.pyplot as plt
from math import cos, sin, pi

dir = '/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/data/'
fns = ['03_2014_Mar_10_1132.xls', '02_2014_Mar_07_1209.xls', 'test_erik_2014_Feb_26_1018.xls',
    '01_2014_Feb_20_1000.xls', '04_2014_Mar_11_1058.xls', #'05_2014_Mar_11_1417.xls', 
    '07_2014_Mar_11_1440.xls', '08_2014_Mar_12_1459.xls', '09_2014_Mar_12_1601.xls',
    '10_2014_Mar_13_1228.xls', '11_2014_Mar_13_1328.xls', '12_2014_Mar_27_1521.xls']
spatial_set_to_1 = ['02_2014_Mar_07_1209.xls', 'test_erik_2014_Feb_26_1018.xls',
    '01_2014_Feb_20_1000.xls']
spatial_set_to_1 = [dir+fn for fn in spatial_set_to_1]
fns = [dir+fn for fn in fns]

math_rts = []
dots_rts = []
music_rts = []
spatial_rts1 = []
spatial_rts2 = []

math_score = []
dots_score = []
music_score = []
spatial_score_three = []
spatial_score_one = []
spatial_score = []

math_threshold = []
dots_threshold = []
music_threshold = []
spatial_threshold = []

for fn in fns:
    main = pd.read_excel(fn, 'Main')
    math = pd.read_excel(fn, 'Math')
    dots = pd.read_excel(fn, 'Dots')
    reading = pd.read_excel(fn, 'Reading')
    phonology = pd.read_excel(fn, 'Phonology')
    spatial = pd.read_excel(fn, 'Spatial')
    music = pd.read_excel(fn, 'Music')
    
    math_rts.extend(list(math['Resp Time'].values))
    while 'timed out' in math_rts: math_rts.remove('timed out')
    dots_rts.extend(list(dots['Resp Time'].values))
    while 'timed out' in dots_rts: dots_rts.remove('timed out')
    music_rts.extend(list(music['Resp Time'].values))
    while 'timed out' in music_rts: music_rts.remove('timed out')
    spatial_rts1.extend(list(spatial.First_Click_Time.values))
    while 'timed out' in spatial_rts1: spatial_rts1.remove('timed out')
    spatial_rts2.extend(list(spatial.dropna().Second_Click_Time.values))
    while 'timed out' in spatial_rts2: spatial_rts2.remove('timed out')
    
    for task_name, score, threshold in [('Math',math_score,math_threshold),('Dots',dots_score,dots_threshold),('Spatial',None,spatial_threshold),('Music',music_score,music_threshold)]:
        tn = main[main.Game==task_name]['Trial Number'].values
        for i,val in enumerate(tn):
            if i==0: continue
            elif val!=tn[i-1]+1:
                choice_tn = val
                break
        vals = mean(main[(main.Game==task_name) & (main['Trial Number']>=choice_tn)].Score.values)
        N = len(main[(main.Game==task_name) & (main['Trial Number']>=choice_tn)].Score.values)
        if task_name=='Spatial' and fn in spatial_set_to_1: 
            spatial_score_one.append((vals,N))
            spatial_score.append((vals,N))
        elif task_name=='Spatial' and fn not in spatial_set_to_1: 
            spatial_score_three.append((vals,N))
            spatial_score.append((vals,N))
        else: score.append((vals,N))
        threshold.append(main[main.Game==task_name].Difficulty.values[-1])
        
print 'Math\t\tMean_RT: %f\tStd_RT: %f\tTotal time: %f\tChoice_Mean_Score: %f\tChoice_Std_Score: %f' %(mean(math_rts), std(math_rts), mean(math_rts), mean([d[0] for d in math_score]), std([d[0] for d in math_score]))
print 'Dots\t\tMean_RT: %f\tStd_RT: %f\tTotal time: %f\tChoice_Mean_Score: %f\tChoice_Std_Score: %f' %(mean(dots_rts), std(dots_rts), 2. + mean(dots_rts), mean([d[0] for d in dots_score]), std([d[0] for d in dots_score]))
print 'Music\t\tMean_RT: %f\tStd_RT: %f\tTotal time: %f\tChoice_Mean_Score: %f\tChoice_Std_Score: %f' %(mean(music_rts), std(music_rts), 5.5 + mean(music_rts), mean([d[0] for d in music_score]), std([d[0] for d in music_score]))
print 'Spatial\t\tMean_RT: %f\tStd_RT: %f\tTotal time: %f\tChoice_Mean_Score: %f\tChoice_Std_Score: %f' %(mean(spatial_rts2), std(spatial_rts2), 5. + mean(spatial_rts2), mean([d[0] for d in spatial_score]), std([d[0] for d in spatial_score]))

plt.figure(figsize=(8,6), dpi=100)
fig = plt.subplot(111)
fig.plot([1]*len(math_score), [s[0] for s in math_score], 'bo', label='Math Scores')
fig.plot([2]*len(dots_score), [s[0] for s in dots_score], 'go', label='Dots Scores')
fig.plot([3]*len(music_score), [s[0] for s in music_score], 'ro', label='Music Scores')
fig.plot([4]*len(spatial_score_three), [s[0] for s in spatial_score_three], 'yo', label='Spatial Scores')
fig.plot([4]*len(spatial_score_one), [s[0] for s in spatial_score_one], 'yD')

for x, score, threshold in [(1,math_score,math_threshold),(2,dots_score,dots_threshold),(3,music_score,music_threshold),(4,spatial_score,spatial_threshold)]:
    ns = [s[1] for s in score]
    score = [s[0] for s in score]
    ys=[]
    for i,txt in enumerate(threshold):
        # normalizes score to an angle of -pi/3 to pi/3
        angle = ((score[i]-min(score))*((3*pi/4)/(max(score)-min(score))))-(3*pi/8)
        if [y for y in ys if y+0.02 > score[i] > y-0.02]: 
            xtext=60*-cos(angle)
        else: xtext=20*cos(angle)
        ytext=30*sin(angle)
        fig.annotate('Diff: {:.0f} N: {}'.format(txt,ns[i]), xy=(x,score[i]), xycoords='data', size='small',
                xytext=(xtext, ytext), textcoords='offset points',
                arrowprops=dict(arrowstyle="->")) #(xtext,score[i]), xytext=(this_xtext,score[i]))
        ys.append(score[i])

handles, labels = fig.get_legend_handles_labels()
display = range(len(labels))
#box = fig.get_position()
#fig.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#fig.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
plt.xticks([1,2,3,4],labels)
plt.xlim([0,5])
plt.yticks([0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
fig.yaxis.grid()
plt.ylim([min([s[0] for s in math_score]+[s[0] for s in dots_score]+[s[0] for s in music_score]+[s[0] for s in spatial_score])-0.15, max([s[0] for s in math_score]+[s[0] for s in dots_score]+[s[0] for s in music_score]+[s[0] for s in spatial_score])+0.15])
plt.ylabel('Accuracy')
#plt.xlabel('Scores')
plt.title('Choice Task Pilot Scores')
plt.show()

pd.DataFrame(dots_rts).to_csv('/Users/Nolan/Desktop/dots_rts.csv')