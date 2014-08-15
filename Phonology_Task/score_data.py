import pandas as pd
import os.path
import matplotlib.pyplot as plt

dir = '/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/Phonology_Task/lab_data_synth_phonemes'
fns = ['101_Feb_19_1447.csv', '102_Feb_28_1103.csv', '103_Feb_28_1203.csv',
    '104_Mar_04_1216.csv', '105_Mar_04_1319.csv', '07_Apr_15_1551.csv',
    '106_May_06_1528.csv', '109_May_13_1445.csv', '110_May_30_1548.csv',
    '111_Jun_05_1520.csv', '112_Jun_06_1057.csv', '114_Jun_06_1153.csv','115_Jun_11_1045.csv',
    '116_Jun_12_0817.csv']



scores = pd.DataFrame({fns[0]: pd.read_csv(os.path.join(dir,fns[0])).score})
for fn in fns[1:]:
    scores[fn] = pd.read_csv(os.path.join(dir,fn)).score

scores.index = pd.Index(pd.read_csv(os.path.join(dir,fn)).trial_number, name='trial_number')


rts = pd.DataFrame({fns[0]: pd.read_csv(os.path.join(dir,fns[0])).rt})
for fn in fns[1:]:
    rts[fn] = pd.read_csv(os.path.join(dir,fn)).rt
rts.index = pd.Index(pd.read_csv(os.path.join(dir,fn)).trial_number, name='trial_number')


output = pd.read_csv(os.path.join(dir,fn), index_col = 'trial_number')
output = output.drop(['score','rt'], axis=1)
output['scores']=scores.T.mean()
output['rts']=rts.T.mean()

phon_dict = {
    'b': {'d':1, 'g':2, 'k':3, 'p':4, 't':5},
    'd': {'g':6, 'k':7, 'p':8, 't':9},
    'g': {'k':10, 'p':11, 't':12},
    'k': {'p':13, 't':14},
    'p': {'t':15}
    }

rev_dict = {
    1: 'b-d', 2: 'b-g', 3: 'b-k', 4: 'b-p',
    5: 'b-t', 6: 'd-g', 7: 'd-k', 8: 'd-p',
    9: 'd-t', 10: 'g-k', 11: 'g-p', 12: 'g-t',
    13: 'k-p', 14: 'k-t', 15: 'p-t'
    }

def diff_code(stim1,stim2):
    s1 = stim1.split('a')[:-1]
    s2 = stim2.split('a')[:-1]
    for p1,p2 in zip(s1,s2):
        if p1==p2: continue
        else: break
    if p1!=p2:
        ps = [p1,p2]
        ps.sort()
        return phon_dict[ps[0]][ps[1]]

def vot_steps(diff_score):
    if diff_score in [1,2,6,13,14,15]: return 0
    elif diff_score in [3,4,5,7,8,9,10,11,12]: return 1
    else: return None

def poa_steps(diff_score):
    if diff_score in [4,9,10]: return 0
    elif diff_score in [1,5,6,7,8,12,14,15]: return 1
    elif diff_score in [2,3,11,13]: return 2
    else: return None

def votorpoa(vot,poa):
    if vot and not poa: return 'VOT'
    elif poa and not vot: return 'POA'
    elif poa not in [0,1,2]: return None
    elif poa and vot: return 'Both'

output['diff_code'] = [diff_code(p1,p2) for p1,p2 in zip(output.stim1.values,output.stim2.values)]
output['VOT_steps'] = [vot_steps(code) for code in output.diff_code.values]
output['POA_steps'] = [poa_steps(code) for code in output.diff_code.values]
output['VOTorPOA'] = [votorpoa(vot,poa) for vot,poa in zip(output.VOT_steps.values, output.POA_steps.values)]
output.to_csv(os.path.join(dir,'scored_phonology_data_06_18_14_new.csv'))

df = pd.DataFrame({'diff_code':range(1,16)})
df['N'] = [len(output[output.diff_code==i]) for i in range(1,16)]
df['Mean'] = [output[output.diff_code==i].scores.mean() for i in range(1,16)]
df['Std'] = [output[output.diff_code==i].scores.std() for i in range(1,16)]
df['difficulty'] = [output[output.diff_code==i].difficulty.values[0] for i in range(1,16)]
df['phonemes'] = [rev_dict[i] for i in range(1,16)]
df_sorted = df.sort('difficulty')
df.to_csv(os.path.join(dir,'phonology_summary.csv'), index=False)


def autolabel(rects,dif):
    for i,rect in enumerate(rects):
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 0.1+height, '%.2f'%height,
            ha='center', va='bottom')
        ax.text(rect.get_x()+rect.get_width()/2., 0.05, int(df_sorted[df_sorted.difficulty==dif].N.values[i]),
            ha='center', va='bottom')

fig,ax = plt.subplots()
rects1 = ax.bar([1,2], df_sorted[df_sorted.difficulty==1].Mean.values, width=0.8, color='g', yerr=df_sorted[df_sorted.difficulty==1].Std.values, error_kw=dict(ecolor='blue'))
rects2 = ax.bar([3,4,5,6,7,8], df_sorted[df_sorted.difficulty==2].Mean.values, width=0.8, color='y', yerr=df_sorted[df_sorted.difficulty==2].Std.values, error_kw=dict(ecolor='blue'))
rects3 = ax.bar([9,10,11,12,13,14,15], df_sorted[df_sorted.difficulty==3].Mean.values, width=0.8, color='r', yerr=df_sorted[df_sorted.difficulty==3].Std.values, error_kw=dict(ecolor='blue'))
ax.set_title('Mean Scores by Phoneme Difference')
ax.set_ylabel('Mean Score')
#ax.set_xlabel('Phonemes Difference')
ax.set_xticks([x+0.4 for x in range(1,16)])
ax.set_xticklabels(df_sorted.phonemes.values)
ax.text(0.5, 0.05, 'N = ', ha='center',va='bottom')
autolabel(rects1,1)
autolabel(rects2,2)
autolabel(rects3,3)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.legend( (rects1[0], rects2[0], rects3[0]), ('Difficulty = 1', 'Difficulty = 2', 'Difficulty = 3'), loc='upper center', 
        bbox_to_anchor=(0.5,-0.05), fancybox=True, ncol=3)
plt.show()