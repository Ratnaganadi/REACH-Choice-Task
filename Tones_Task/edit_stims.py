from psychopy import data
import csv
import sys
import numpy

trialList=data.importConditions('stim_final2.csv')

out_file = open('stim_final2_edit.csv', 'w')
writer = csv.writer(out_file)
fieldnames=['Natural_Order','soundA','soundB','Details','Contour','Notes_Different','diff1','diff2','root','Answer','Random_Order']
headers = dict((n,n) for n in fieldnames)
myWriter = csv.DictWriter(out_file,fieldnames=fieldnames, lineterminator= '\n')
myWriter.writerow(headers)
for n, row in enumerate(trialList):
    soundA,soundB=(row['soundA'],row['soundB'])
    contour=''
    diff1,diff2=(None,None)
    for n in range(4):
        if soundA[n]>soundA[n+1]: contour+='D'
        elif soundA[n]<soundA[n+1]: contour+='U'
        else: contour+='X'
    for n in range(5):
        if soundA[n]!=soundB[n]: 
            diff1=n
            for m in range(n+1,5):
                if soundA[m]!=soundB[m]: diff2=m
            break
    row['Contour']=contour
    row['diff1']=diff1
    row['diff2']=diff2
    myWriter.writerow(row)
out_file.close()