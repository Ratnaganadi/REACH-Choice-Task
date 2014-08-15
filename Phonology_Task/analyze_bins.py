import os
from os.path import join, isfile
import pandas as pd
from numpy import mean


d = pd.read_csv('/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/Phonology_Task/phonology_stims.csv')
ab = pd.read_csv('/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/Phonology_Task/phonology_stims_abbrev.csv')

dd = d[d.distance.notnull()]
abd = ab[ab.distance.notnull()]

sdict = {}
sdict['bin_number']=[]
sdict['number_phonemes']=[]
sdict['distance']=[]
sdict['position']=[]
sdict['total_stims']=[]
sdict['abbrev_stims']=[]
bnum = 0

for np in range(1,4):
    for dis in range(1,4):
        for dpos in range(1,np+1):
            bnum+=1
            sdict['bin_number'].append(bnum)
            sdict['number_phonemes'].append(np)
            sdict['distance'].append(dis)
            sdict['position'].append(dpos)
            sdict['total_stims'].append(len(dd[(dd.number_phonemes==np)&(dd.distance==dis)&(dd.difference_position==dpos)]))
            sdict['abbrev_stims'].append(len(abd[(abd.number_phonemes==np)&(abd.distance==dis)&(abd.difference_position==dpos)]))

s = pd.DataFrame(sdict)
s = s[['bin_number','number_phonemes','distance','position','total_stims','abbrev_stims']]

dir = '/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/Phonology_Task/lab_data_synth_phonemes'
full_fns = [join(dir,fn) for fn in os.listdir(dir) if isfile(join(dir,fn)) and fn[:2].isdigit()]


score_lists = [[] for x in range(18)]
rt_lists = [[] for x in range(18)]
for full_fn in full_fns:
    scores = pd.read_csv(full_fn)
    if len(scores)<50: continue
    print 'processing %s...'%full_fn
    data = abd.merge(scores, how='left')
    
    bnum=0
    for np in range(1,4):
        for dis in range(1,4):
            for dpos in range(1,np+1):
                bnum+=1
                bin_data=data[(data.number_phonemes==np)&(data.distance==dis)&(data.difference_position==dpos)]
                if bin_data: 
                    score_lists[bnum-1].append(bin_data.score.mean())
                    rt_lists[bnum-1].append(bin_data.rt.mean())
    
    
scores_mean = [mean(score_list) for score_list in score_lists]
rts_mean = [mean(rt_list) for rt_list in rt_lists]

s['mean_score'] = scores_mean
s['mean_rt'] = rts_mean

s.to_csv('/Users/Nolan/Dropbox/LDRH Tasks/Ratna/LDRH_Choice_Paradigm/Phonology_Task/bin_analysis.csv', index=False)