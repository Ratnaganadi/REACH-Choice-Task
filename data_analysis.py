import os, math, csv, xlwt, glob
import numpy as np
import pandas as pd
import pprint as pp

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir+'/data/complete_data/')

#initialize list and variables
data_header = ['Type','Game','Difficulty','Score']
game_header = ['Type','Subject_ID','Difficulty','Total_Score','Total_Trial','Accuracy']
summary_header = ['Type','Subject_ID','Game','Total_Score','Total_Trial','Accuracy']
mean_byTask_header = ['Type','Game','Difficulty','Accuracy']
mean_perID_header = ['Type','Subject_ID','Accuracy']
games = ['Math','Dots','Reading','Phonology','Spatial','Music']
data={}; accuracy_thr={}; general_accuracy_thr={}
accuracy_byTask = {} 
mean_all=[] #a list of mean_perID

tab_names = ['Mean_perID','Mean_byTask','Summary'] + [game+'_all' for game in games]
#getting filenames
filenames = glob.glob('*.xls')

#create output structure
wb = xlwt.Workbook()
output={}
for tab in tab_names:
    if tab=='Mean_perID': head = mean_perID_header
    elif tab=='Mean_byTask': head = mean_byTask_header
    elif tab=='Summary': head = summary_header
    elif tab.split('_')[1]=='all': head = game_header

    #initialize each tab/sheet and its header
    output[tab] = dict(sheet = wb.add_sheet(tab), headers=head, row=1)
    for col, header in enumerate(output[tab]['headers']): output[tab]['sheet'].write(0,col,header)

#create a function for accuracy calculations and write_to_file
def accuracy_calculation(game_name):
    game_data = data['threshold'][game_name] #getting all the thresholding data of one game
    game_lvl = list(set([game_data[i][1] for i in range(0,len(game_data))])) #getting the list of levels
    accuracy_list = {}
    general_accuracy_list = [0,0,0]
    for x in game_lvl: accuracy_list[x]=[0,0,0]
    for i in range(0,len(game_data)):
        dif = game_data[i][1] #difficulty
        
        #calculate accuracy per level of difficulty
        accuracy_list[dif][0]+=game_data[i][2]
        accuracy_list[dif][1]+=1
        accuracy_list[dif][2] = float(accuracy_list[dif][0]/accuracy_list[dif][1])
        #calculate general score and number of trials per game
        general_accuracy_list[0]+=game_data[i][2]
        general_accuracy_list[1]+=1
    
    #calculate accuracy per game in 1 subject
    general_accuracy_list[2] = float(general_accuracy_list[0]/general_accuracy_list[1])
    return(accuracy_list,general_accuracy_list)

def write_to_file(tab,outrow,extra_row):
    if extra_row=='extra_row':
        for key in outrow.keys(): outrow[key]=''
        for col,header in enumerate(output[tab]['headers']):
            output[tab]['sheet'].write(output[tab]['row'],col,outrow[header])
        output[tab]['row']+=1
    else:
        for col,header in enumerate(output[tab]['headers']):
            output[tab]['sheet'].write(output[tab]['row'],col,outrow[header])
        output[tab]['row']+=1


## data processing ## calculating values per subject ID
for filename in filenames:
    sheet = pd.read_excel(filename,'Main',index_col='Trial Number',na_values=['NA'])
    subject_id = filename.split('_')[0] #getting subject ID from filename

    gen_accuracy=[]
    accuracy_thr[subject_id]={} 
    general_accuracy_thr[subject_id]={}
    for x in ['threshold','choice']:
        data[x]={}
        for game in games:
            data[x][game]=[]
            accuracy_thr[subject_id][game]={} 
            general_accuracy_thr[subject_id][game]={}

    #get raw data from "sheet" and turn it into a list
    rawdata = [[],[],[],[]]
    for i in range(0,len(data_header)):
        rawdata[i] = list(sheet[data_header[i]])

    #reorganize raw data
    for i in range(0,len(rawdata[0])):
        data[rawdata[0][i]][rawdata[1][i]].append([i,rawdata[2][i],rawdata[3][i]]) #(trial number, difficulty, score)

    for game in games:
        if game!='Math':
            if data['threshold'][game]!=[]:
                #calculate current game's accuracy
                print('processing',subject_id, game)
                (accuracy_thr[subject_id][game],general_accuracy_thr[subject_id][game]) = accuracy_calculation(game)
                ##write outputs on game sheets
                for dif in accuracy_thr[subject_id][game].keys():
                    score = accuracy_thr[subject_id][game][dif][0].astype(np.float64) #turn score from int64 to float64
                    outrow = {'Type':'threshold','Subject_ID':subject_id,'Difficulty':dif,'Total_Score':score,'Total_Trial':accuracy_thr[subject_id][game][dif][1],'Accuracy':float(accuracy_thr[subject_id][game][dif][2])}
                    write_to_file(game+'_all',outrow,'no_extra_row')
                    
                ##write outputs on summary sheets
                score_sum = general_accuracy_thr[subject_id][game][0].astype(np.float64)
                outrow_sum= {'Type':'threshold','Subject_ID':subject_id,'Game':game,'Difficulty':dif,'Total_Score':score_sum,'Total_Trial':general_accuracy_thr[subject_id][game][1],'Accuracy':float(general_accuracy_thr[subject_id][game][2])}
                write_to_file('Summary',outrow_sum,'no_extra_row')

                #create list of accuracy only for all games
                gen_accuracy.append(float(general_accuracy_thr[subject_id][game][2]))
        
            else: print(subject_id,game,'skipped')

    ##calculating and writing outputs for mean_perID
    if gen_accuracy!=[]:
        mean_perID = float(sum(gen_accuracy)/len(gen_accuracy))
        # print 'mean_perID',mean_perID
        mean_all.append(mean_perID) #appending mean_perID to a list
        outrow_perID = {'Type':'threshold','Subject_ID':subject_id,'Accuracy':float(mean_perID)}
        write_to_file('Mean_perID',outrow_perID,'no_extra_row')

    #add extra row after each participant's data for better visual
    for game in games: write_to_file(game+'_all',outrow,'extra_row')
    write_to_file('Summary',outrow_sum,'extra_row')

##calculate the over all mean of all IDs
if mean_all!=[]:
    mean_allID = float(sum(mean_all)/len(mean_all))
    outrow_perID = {'Type':'threshold','Subject_ID':'Mean_all','Accuracy':float(mean_allID)}
    write_to_file('Mean_perID',outrow_perID,'no_extra_row')
    
## data processing ## calculating values per game/task across all subject ID
mean_task={}
for game in games:
    mean_task[game]=[]
    if game!='Math':
        accuracy_byTask[game]={}
        print('processing',game,'mean')
        for filename in filenames:
            subject_id = filename.split('_')[0]
            for dif in accuracy_thr[subject_id][game].keys():
                accuracy_byTask[game][dif]=[]

        for filename in filenames:
            subject_id = filename.split('_')[0]
            for dif in accuracy_thr[subject_id][game].keys():
                accuracy_byTask[game][dif].extend([accuracy_thr[subject_id][game][dif][2]])

        ##calculate mean accuracy per difficulty level byTask
        for dif in accuracy_byTask[game].keys():
            accuracy_task = float(sum(accuracy_byTask[game][dif])/len(accuracy_byTask[game][dif]))
            mean_task[game].append(accuracy_task)
            outrow_byTask = {'Type':'threshold','Game':game,'Difficulty':dif,'Accuracy':float(accuracy_task)}
            write_to_file('Mean_byTask',outrow_byTask,'no_extra_row')

        ##calculate overall mean accuracy byTask
        if mean_task[game]!=[]:
            mean_task_value = float(sum(mean_task[game])/len(mean_task[game]))
            outrow_byTask = {'Type':'threshold','Game':game+'_mean','Difficulty':'','Accuracy':float(mean_task_value)}
            write_to_file('Mean_byTask',outrow_byTask,'no_extra_row')

        write_to_file('Mean_byTask',outrow_byTask,'extra_row')








os.chdir(script_dir+'/data_analysis')
wb.save('accuracy.xls')
print('file written')
# pp.pprint(accuracy_byTask)



