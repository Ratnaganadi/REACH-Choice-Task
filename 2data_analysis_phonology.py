import os, math, csv, xlwt, glob
import numpy as np
import pandas as pd
import pprint as pp
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir+'/data/complete_data/phonology_all')
output_name = 'phonology_accuracy_combined.xls'
output_dir = script_dir+'/data_analysis'

#initialize list and variables
Type = ['threshold','choice']
data_header = ['Correct Response','Score','Difference Position','Phoneme Difference','Distance']
games = ['Math','Dots','Reading','Phonology','Spatial','Music']
x=''; data_byPh={}; data_byPhPos={}; data_byResp={}; data_byRespPos={}; data_byPos={}; data_byLevel={}; data_byDist={}
datalist = [data_byPh,data_byPhPos,data_byPos,data_byLevel,data_byDist]
# data_byResp,data_byRespPos,
tab_header_sum = ['Type','Variable','POA_step','VOT_step','Difficulty','Var_Value','Total_Score','Total_Trial','Accuracy']
tab_header_other = ['Type','Subject_ID','Variable','Var_Value','Total_Score','Total_Trial','Accuracy']
tab_header_byPh = ['Type','Subject_ID','Variable','Var_Value','POA_step','VOT_step','Total_Score','Total_Trial','Accuracy']
tab_names = ['Summary','Accuracy_byPhonemePos','Accuracy_byPhoneme','Accuracy_byResp','Accuracy_byRespPos','Accuracy_byPosition','Accuracy_byDistance','Accuracy_byLevel']
poa_vot = {
    'b-k':[2,1], 'p-g':[2,1], 'k-b':[2,1], 'g-p':[2,1],
    'd-p':[1,1], 't-b':[1,1], 'd-k':[1,1], 'g-t':[1,1],
    't-p':[1,0], 'd-b':[1,0], 'k-t':[1,0], 'g-d':[1,0],
    'd-t':[0,1], 'g-b':[2,0], 't-d':[0,1], 'k-p':[2,0],
    'k-g':[0,1], 'g-k':[0,1], 'b-p':[0,1], 'p-b':[0,1]
}
difficulty = {
    'dif1_D3_[POA2,VOT1]': ['b-k', 'p-g', 'k-b', 'g-p'],
    'dif2_D2_[POA1,VOT1]': ['d-p', 't-b', 'd-k', 'g-t'],
    'dif3_D1_[POA1,VOT0]': ['t-p', 'd-b', 'k-t', 'g-d'],
    'dif4_D2_[POA2,VOT0]_D1_[POA0,VOT1]': ['d-t', 'g-b', 't-d', 'k-p'],
    'dif5_D1_[POA0,VOT1]': ['k-g', 'g-k', 'b-p', 'p-b']
}
difno={
    '1': ['b-k', 'p-g', 'k-b', 'g-p'],
    '2': ['d-p', 't-b', 'd-k', 'g-t'],
    '3': ['t-p', 'd-b', 'k-t', 'g-d'],
    '4': ['d-t', 'g-b', 't-d', 'k-p'],
    '5': ['k-g', 'g-k', 'b-p', 'p-b']
}

phoneme_bank = [['b-k','k-b'], ['p-g','g-p'],
    ['d-p','p-d'], ['t-b','b-t'],['d-k','k-d'],['g-t','t-g'],
    ['t-p','p-t'], ['d-b','b-d'],['k-t','t-k'],['g-d','d-g'],
    ['d-t', 't-d'],['g-b','b-g'],['k-p','p-k'],
    ['k-g', 'g-k'], ['b-p', 'p-b']]

# poa_vot_category=['POA2, VOT0','POA1, VOT0','POA1, VOT1','POA0, VOT1']

#getting filenames
filenames = glob.glob('*.xls')
print 'total_files',len(filenames)

#create output structure
wb = xlwt.Workbook()
output={}
for tab in tab_names:
    if tab=='Summary': tab_header = tab_header_sum
    elif tab=='Accuracy_byPhoneme' or tab=='Accuracy_byPhonemePos': tab_header = tab_header_byPh
    elif tab=='Accuracy_byPosition': tab_header = tab_header_other

    #initialize each tab/sheet and its header
    output[tab] = dict(sheet = wb.add_sheet(tab), headers=tab_header, row=1)
    for col, header in enumerate(output[tab]['headers']): output[tab]['sheet'].write(0,col,header)

#create a function for accuracy calculations and write_to_file
def write_to_file(tab,outrow,extra_row):
    if extra_row=='extra_row':
        for key in outrow.keys(): outrow[key]=''
        for col,header in enumerate(output[tab]['headers']):
            output[tab]['sheet'].write(output[tab]['row'],col,'')
        output[tab]['row']+=1
    else:
        for col,header in enumerate(output[tab]['headers']):
            item = outrow[header]
            # if (type(outrow[header]) is not str) and (type(outrow[header]) is not int) and (type(outrow[header]) is not float):
                # item=outrow[header].astype(np.float64)
            output[tab]['sheet'].write(output[tab]['row'],col,item)
        output[tab]['row']+=1

def calculate_accuracy_then_save(datalist,task_type,subject,var,name):
    for key in datalist.keys():
        templist = [item.astype(np.float64) for item in datalist[key]]
        #calculating total score, trial, and accuracy
        total_score = sum(templist)
        total_trial = len(templist)
        accuracy_byVar= float(total_score/total_trial)
        outrow={'Type':task_type,'Variable':var,'Var_Value':key,'Total_Score':total_score,'Total_Trial':total_trial,'Accuracy':accuracy_byVar}

        poa = ''; vot = ''; diff = ''
        if name=='Accuracy_byPhoneme' or var=='Phoneme': 
            poa = poa_vot[key][0]
            vot = poa_vot[key][1]
            for difkey in difno.keys():
                if key in difno[difkey]: diff = difkey;
        elif name=='Accuracy_byPhonemePos' or var=='PhonemePos':
            ph = key.split('_')[0]
            poa = poa_vot[ph][0]
            vot = poa_vot[ph][1]
            for difkey in difno.keys():
                if ph in difno[difkey]: diff = difkey
        if subject!=None: outrow['Subject_ID']=subject
        if (subject!=None and poa!='' and vot!='') or subject==None:
            outrow['POA_step']=poa
            outrow['VOT_step']=vot
            outrow['Difficulty']=diff

        # 'POA_step':poa,'VOT_step':vot,'Var_Value':key,'Total_Score':total_score,'Total_Trial':total_trial,'Accuracy':accuracy_byVar}
        write_to_file(name,outrow,'no_extra_row')


## data processing ## calculating values per subject ID
for filename in filenames:
    sheet = pd.read_excel(filename,'Phonology',index_col='Trial Number',na_values=['NA'])
    subject_id = filename.split('_')[0] #getting subject ID from filename 
    print('processing', subject_id)

    #get raw data from "sheet" and turn it into a list
    #rawdata = [index,'Correct Response','Score','Difference Position','Phoneme Difference','Distance']
    rawdata = [[],[],[],[],[],[],[]]
    rawdata[0] = list(sheet.index)
    for i in range(0,len(data_header)): rawdata[i+1] = list(sheet[data_header[i]])


    #initializing dictionaries and lists
    for data in datalist: data[subject_id] = {}

    for x in ['threshold','choice']:
        for data in datalist: data[subject_id][x]={}

        for i in range(0,len(rawdata[0])):
            data_byPos[subject_id][x][rawdata[3][i]] = []
            data_byDist[subject_id][x][rawdata[5][i]] = []
            # data_byResp[subject_id][x][rawdata[0][i]] = []
            # data_byRespPos[subject_id][x][rawdata[0][i]+'_'+str(int(rawdata[3][i]))] = []

            for pair in phoneme_bank:
                if rawdata[4][i] in pair and rawdata[4][i] not in data_byPh[subject_id][x].keys():
                    data_byPh[subject_id][x][pair[0]]=[]
                    for pos in [1,2,3]: data_byPhPos[subject_id][x][pair[0]+'_'+str(pos)]=[]

        for dif in difficulty.keys():
            data_byLevel[subject_id][x][dif]=[]

    #determining data_type (threshold or choice)
    for i in range(0,len(rawdata[0])):
        if i==0 and (rawdata[0][i+1]-rawdata[0][i])==1: data_type='threshold'
        elif i!=0 and (rawdata[0][i]-rawdata[0][i-1])==1: data_type='threshold'
        else: data_type='choice'

        #reorganize raw data into prepared dictionaries/lists
        if rawdata[1][i]=='different' and pd.isnull(rawdata[3][i])!=True:
            data_byPos[subject_id][data_type][rawdata[3][i]].append(rawdata[2][i]) #datalist['threshold'][position]=score
            data_byDist[subject_id][data_type][rawdata[5][i]].append(rawdata[2][i]) #datalist['threshold'][distance]=score
            # data_byResp[subject_id][x][rawdata[0][i]].append(rawdata[2][i])
            # data_byRespPos[subject_id][x][rawdata[0][i]+'_'+str(int(rawdata[3][i]))].append(rawdata[2][i])

            #put score data of the same phoneme pairs in the same list
            for pair in phoneme_bank:
                if rawdata[4][i] in pair: 
                    data_byPh[subject_id][data_type][pair[0]].append(rawdata[2][i])
                    data_byPhPos[subject_id][data_type][pair[0]+'_'+str(int(rawdata[3][i]))].append(rawdata[2][i])
                    # if subject_id=='P0204': print 'test',subject_id,pair[0]+'_'+str(int(rawdata[3][i]))
            #organize score data based on level of difficulty only
            for dif in difficulty.keys():
                if rawdata[4][i] in difficulty[dif]:
                    data_byLevel[subject_id][data_type][dif].append(rawdata[2][i]) #datalist['threshold'][difficulty_level]=score

    #removing empty dictionaries:
    for x in Type:
        for data in datalist: data[subject_id][x] = dict((k,v) for k,v in data[subject_id][x].items() if v)
    
        # x='threshold'
        #calculate accuracy by position, phoneme_pair and distance
        calculate_accuracy_then_save(data_byPh[subject_id][x],x,subject_id,'Phoneme_Pair','Accuracy_byPhoneme')
        calculate_accuracy_then_save(data_byPhPos[subject_id][x],x,subject_id,'Phoneme_Pair','Accuracy_byPhonemePos')
        # calculate_accuracy_then_save(data_byResp[subject_id][x],x,subject_id,'Correct_Resp','Accuracy_byPhoneme')
        # calculate_accuracy_then_save(data_byRespPos[subject_id][x],x,subject_id,'Correct_Resp','Accuracy_byPhonemePos')
        calculate_accuracy_then_save(data_byPos[subject_id][x],x,subject_id,'Difference_Position','Accuracy_byPosition')
        calculate_accuracy_then_save(data_byDist[subject_id][x],x,subject_id,'Distance','Accuracy_byDistance')
        calculate_accuracy_then_save(data_byLevel[subject_id][x],x,subject_id,'Difficulty_Level','Accuracy_byLevel')

    #adding extra row at the end of each participant's data
    write_to_file('Accuracy_byPhoneme',{},'extra_row')
    write_to_file('Accuracy_byPhonemePos',{},'extra_row')
    write_to_file('Accuracy_byPosition',{},'extra_row')
    write_to_file('Accuracy_byDistance',{},'extra_row')
    write_to_file('Accuracy_byLevel',{},'extra_row')

# print 'databylevel',data_byLevel
## data processing ## calculating values per game/task across all subject ID
# print 'data_byPh', data_byPh

y='threshold'
#initializing dictionaries and lists
sum_byPh = {}; sum_byPhPos = {}; sum_byPos = {}; sum_byDist = {}; sum_byPOA_VOT = {}; sum_byLevel = {}
sum_byPh[y] = {}; sum_byPhPos[y] = {}; sum_byPos[y] = {}; sum_byDist[y] = {}; sum_byPOA_VOT[y] = {}; sum_byLevel[y] = {}
for filename in filenames:
    subject_id = filename.split('_')[0]
    datalist1 = [data_byPos[subject_id][y], data_byPh[subject_id][y], data_byPhPos[subject_id][y], data_byDist[subject_id][y], data_byLevel[subject_id][y]]
    sumlist = [sum_byPos[y], sum_byPh[y], sum_byPhPos[y], sum_byDist[y], sum_byLevel[y]]

    for i in range(0,5):
        for dif in datalist1[i].keys(): 
            sumlist[i][dif]=[]
            if i==1:
                category = 'POA'+str(poa_vot[dif][0])+'_VOT'+str(poa_vot[dif][1])
                sum_byPOA_VOT[y][category]=[]

for filename in filenames:
    subject_id = filename.split('_')[0]
    datalist1 = [data_byPos[subject_id][y], data_byPh[subject_id][y], data_byPhPos[subject_id][y], data_byDist[subject_id][y], data_byLevel[subject_id][y]]
    sumlist = [sum_byPos[y], sum_byPh[y], sum_byPhPos[y], sum_byDist[y], sum_byLevel[y]]
    for i in range(0,5):
        for dif in datalist1[i].keys(): 
            sumlist[i][dif].extend(datalist1[i][dif])
            if i==1:
                category = 'POA'+str(poa_vot[dif][0])+'_VOT'+str(poa_vot[dif][1])
                sum_byPOA_VOT[y][category].extend(datalist1[i][dif])

##calculate mean accuracy per difficulty level by variables + add extra line after each variable
calculate_accuracy_then_save(sum_byPh[y],y,None,'Phoneme','Summary'); write_to_file('Summary',{},'extra_row')
calculate_accuracy_then_save(sum_byPhPos[y],y,None,'PhonemePos','Summary'); write_to_file('Summary',{},'extra_row')
calculate_accuracy_then_save(sum_byPos[y],y,None,'Position','Summary'); write_to_file('Summary',{},'extra_row')
calculate_accuracy_then_save(sum_byPOA_VOT[y],y,None,'POA and VOT','Summary'); write_to_file('Summary',{},'extra_row')
calculate_accuracy_then_save(sum_byDist[y],y,None,'Distance','Summary'); write_to_file('Summary',{},'extra_row')
calculate_accuracy_then_save(sum_byLevel[y],y,None,'Difficulty_Level','Summary'); write_to_file('Summary',{},'extra_row')

os.chdir(output_dir)
wb.save(output_name)
print('file written')









# ##data visualization## plotting data on a graph
# sheet_plot = pd.read_excel(output_name,'Summary',index_col='Variable',na_values=['NA'])
# variable = list(sheet_plot.index)
# var_value = list(sheet_plot['Var_Value'])
# plot_accuracy = list(sheet_plot['Accuracy'])
# x_var=[[],[],[],[]]; y_var = [[],[],[],[]]; plt_title=['','','']
# Vars=['Position','Distance','Phoneme','POA and VOT']
# colors = ['#3399FF','#FF6666','#FFFF66','#FF9933']

# for i in range(0,len(variable)):
#     if variable[i]=='Position': x=0
#     elif variable[i]=='Phoneme': x=2
#     elif variable[i]=='POA and VOT': x=3
#     elif variable[i]=='Distance': x=1
    
#     else: x=None
#     if x!=None:
#         x_var[x].append(var_value[i])
#         y_var[x].append(plot_accuracy[i])       
#         # plt_title[x] = 'Accuracy by '+Vars[x]

# plt_n = 121
# width=0.7
# for x in range(2,len(x_var)):
#     n=len(x_var[x])
#     idx = np.arange(n)
#     plt.subplot(plt_n)
#     plt.bar(idx,y_var[x],width,color=colors[x])
#     axes=plt.gca()
#     axes.set_ylim([0,1.0])
#     # plt.title(plt_title[x])
#     plt.ylabel('Accuracy')
#     plt.xlabel(Vars[x])
#     plt.xticks(idx+width/2,(tuple(x_var[x])))
#     plt_n+=1

# plt.show()

# x_vars=[[],[],[],[]]; y_vars=[[],[],[],[]]
# # poa_vot_category=['POA2, VOT0','POA1, VOT0','POA1, VOT1','POA0, VOT1']
# for i in range(0,len(x_var[2])):
#     phoneme = x_var[2][i]
#     accuracy = y_var[2][i]
#     no=None
#     if phoneme not in ['g-t','b-d']:
#         if poa_vot[phoneme]==[2,0]: no = 0
#         elif poa_vot[phoneme]==[1,0]: no = 1
#         elif poa_vot[phoneme]==[1,1]: no = 2
#         elif poa_vot[phoneme]==[0,1]: no = 3

#         if no!=None:
#             x_vars[no].append(phoneme)
#             y_vars[no].append(accuracy)

# plt_no=141
# for no in [0,3]:
#     n=len(x_vars[no])
#     ind = np.arange(n)
#     plt.subplot(plt_no)
#     plt.bar(ind,y_vars[no],width,color=colors[no])
#     axes=plt.gca()
#     axes.set_ylim([0,1.0])
#     # plt.ylabel('Accuracy')
#     plt.xlabel(poa_vot_category[no])
#     plt.xticks(ind+width/2,(tuple(x_vars[no])))
#     plt_no+=1

# plt.show()

# # ind + (1-(i/2))*w
# # 1= ind+w/2
# # 2= ind
# # 3= ind-w/2
# # 4= ind-w

# # 1= ind
# # 2= ind + ind
# # 3= ind
# # 4= ind
# # print('x',x)
# # print('y',y)


















