import os, math, csv, itertools, nltk
import pandas as pd
from pyxdameraulevenshtein import damerau_levenshtein_distance as DLevdist
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as NDLevdist
import random, numpy
from random import choice, shuffle, sample
from operator import mul, itemgetter
import string

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
#reads in sheet
sheet = pd.read_excel('combined_gradewordlist_with_toolbox.xlsx','Sheet1',index_col='No',na_values=['NA'])

#preparing output file
stimfile = open('readingstim_anagram_new.csv', 'w')
fieldnames = ['Difficulty','Grade','Target','Foil_sound_alike','Foil_look_alike','Foil_sound_look_alike','Foil_no_sound_look']
headers = dict((n,n) for n in fieldnames)
writer = csv.DictWriter(stimfile,fieldnames=fieldnames, lineterminator= '\n')
writer.writerow(headers)


## INITIALIZE DICTIONARIES & OTHER VARIABLES ##
difficulty = 1
wordDict = {} #dictionary of words for each grade level
cmuDict = {} #dictionary of cmu transcriptions
foilDict = {} #to store all possible foils a grade can have
foil_anagram = {}
grade_2bletter = ['letter','lettersound']
grade_2button = ['k','grade1a','grade1b']
grade_4b = ['grade2','grade3','grade4']
grade_4b_anagram = ['grade2_anagram','grade3_anagram','grade4_anagram']
grade_4button = grade_4b + grade_4b_anagram
gradelevel = grade_2bletter + grade_2button + grade_4b + grade_4b_anagram
gradelvl = ['k','grade1a','grade1b','grade2','grade3','grade4','grade5'] #grade levels names
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
sound = ['B','D','F','H','J','K','L','M','N','P','R','S','T','V','W','Y','Z']
look = {'A':['K','M','N','V','W','X','Y'],'B':['D','E','H','O','P','R'],'C':['D','G','J','O','P','Q','S','U'],'D':['B','C','G','J','O','P','Q','U'],'E':['B','F','H','M','N','W'],'F':['E','H','I','L','M','N','P','T'],'G':['C','D','J','O','P','Q','U'],'H':['B','E','F','I','L','M','N','T'],'I':['F','J','L','T'],'J':['C','G','I','L','U'],'K':['A','M','N','R','V','W','X','Y','Z'],'L':['F','H','T'],'M':['A','E','F','H','K','N','V','W','X','Y','Z'],'N':['A','E','F','H','K','M','V','W','X','Y','Z'],'O':['B','C','D','G','Q','U'],'P':['B','C','D','F','R'],'Q':['C','D','G','O','U'],'R':['B','K','P'],'S':['C','Z'],'T':['F','H','I','L','Y'],'U':['C','D','G','J','O','Q','V','W','X','Y'],'V':['A','K','M','N','U','W','X','Y','Z'],'W':['A','K','M','N','U','V','X','Y','Z'],'X':['A','K','M','N','U','V','W','Y','Z'],'Y':['K','M','N','S','V','W','X','Z'],'Z':['K','M','N','V','W','X','Y']}

#no audio file in google for grade word list + for toolbox + not in cmudict
nofile = ['pat', 'seek', 'pool', 'meant','America','Friday','Saturday','Sunday','asked','bones','books','carried','cities','close','countries','desert','died','dishes','do','eyes','filled','getting','happened','happiest','inches','kids','largest','live','lived','lots','minute','pan','playing','present','read','says','sending','stairs','stopped','stories','things','turned','use','wind']+['gelastic','antagonizing','annunciating','dolorific','oscillating','exacerbating','imperiousness','juncous','eccentricities','forisfamiliate','imparidigitate','imperspicuity','effigial','suffrutescent','fringillaceous','lugubriousness','ranunculaceous','cucurbitaceous','magniloquently','accrementitial','synechdochism','brobdingnagian']+['transposition','whelp','fenestration','nutate','ablation','amicability','fumigant','sinew','issuant','expostulate','pedagogue','conviviality','malevolence','scintillating','valetudinarian','abysm','dissolubility','perspicuity','eclecticism','interstitial','recrudescence','platitudinous','perfunctorily','viscera','apopemptic','reliquary','malapropism','automatism','diamantiferous','sesquipedalian','deliquescence','sanguineous','achromatism','satiety','recapitulatory','saxifragaceous','abstemiously','dodecahedral']


## INITIALIZE DICTIONARIES, CREATE GENERAL WORD LIST AND FOIL FOR ALL GRADE LEVELS ##
gr_cmudict = nltk.corpus.cmudict.dict() #initialize cmudict
cmu_entries = nltk.corpus.cmudict.entries() #cmu entries: (word,transcriptions tuples)
cmu_words = [entry[0] for entry in cmu_entries]

markov_probs = {}
for letter in string.lowercase:
    markov_probs[letter] = {}
    for let in string.lowercase:
        markov_probs[letter][let] = 0
        markov_probs[letter]["total"] = 0

for word in cmu_words:
    for i, letter in enumerate(word[1:]):
        if word[i] in string.lowercase and letter in string.lowercase:
            markov_probs[word[i]][letter] += 1
            markov_probs[word[i]]["total"] += 1

for value in markov_probs.values():
    for letter in string.lowercase:
        value[letter] = value[letter]/float(value["total"])

for grade in gradelevel:
    foilDict[grade]={} #to store all possible foils a grade can have
    foil_anagram[grade]={}
    
wordDict={'letter':letters, 'lettersound':sound}
for grade in gradelvl:
    #creating dictionary for Dict of words, then drop any empty cells, remove nofile words
    wordDict[grade] = list((sheet.loc[:,grade]).dropna())
    #check for unremoved words, then remove them    
    for i in range(0,3):
        for word in wordDict[grade]: 
            if word in nofile: wordDict[grade].remove(word)

    anagram = grade + '_anagram'
    if anagram in grade_4b_anagram: 
        wordDict[anagram] = []
        wordDict[anagram].extend(wordDict[grade])
        # print anagram, wordDict[anagram]

    #create  dictionary of cmu transcription for all letters and grade level
    for word in wordDict[grade]: 
        # print word
        cmuDict[word]= ''.join((gr_cmudict[word.lower()])[0])

for ltr in letters: 
    ltr = str(ltr.lower())
    cmuDict[ltr] = ''.join((gr_cmudict[ltr])[0])

for grade in grade_4button:
    for target in wordDict[grade]:
        if len(target) > 3:
            inner_letters = target[1:-1]
            temp_foil_anagram = [target[0] + ''.join(x) + target[-1] for x in itertools.permutations(inner_letters) if DLevdist("".join(x), inner_letters) > 0] #create list of anagram as foils

            # assign markov chain probability to each word

            for i, temp_word in enumerate(temp_foil_anagram):
                probs = []
                for j, letter in enumerate(temp_word[1:]):
                    probs.append(markov_probs[temp_word[j]][letter])
                temp_foil_anagram[i] = {
                    "word": temp_word,
                    "prob": reduce(mul, probs),
                    "edit": DLevdist(temp_word, target)
                }
            
            anagrams = sorted(temp_foil_anagram, key=itemgetter("prob"), reverse=True)
            anagrams = sorted(anagrams, key=itemgetter("edit"))

            if anagrams:
                foil_anagram[grade][target] = [x["word"] for x in anagrams[0:1]]

# creating foil Dicts for all grades
foilDict={'letter':letters, 'lettersound':sound, 'k':(wordDict['k'])+(wordDict['grade1a'])}
for i in range(1,len(gradelvl)-1): foilDict[gradelvl[i]] = (wordDict[gradelvl[i-1]]) + (wordDict[gradelvl[i]]) + (wordDict[gradelvl[i+1]])

#stimuli dictionary: {grade: {criteria: [target,...], [foil,...], [criteria,...], [lev,...], [cmu,...]}}
lev_cutoff = {'k':0.34,'grade1a':0.34,'grade1b':0.34 ,'grade2':0.29,'grade3':0.29,'grade4':0.29,'grade5':0.34} #lev_cutoff = {'k':0.33,'grade1a':0.33,'grade1b':0.33,'grade2':0.283,'grade3':0.286,'grade4':0.286, 'grade5':0.33}
cmu_cutoff = {'letter':0.5,'lettersound':0.5,'k':0.34,'grade1a':0.34,'grade1b':0.21,'grade2':0.21,'grade3':0.21,'grade4':0.21,'grade5':0.23} #cmu_cutoff = {'k':0.33,'grade1a':0.33,'grade1b':0.2,'grade2':0.2,'grade3':0.2,'grade4':0.2,'grade5':0.22}
c = ['sound_alike','look_alike','sound_look_alike','no_sound_look']


def target_foil_processing(grade):
    gradename = grade.split("_")[0]
    so = None
    foilsIn = {}
    foilDict_temp = []
    targetList = wordDict[gradename]
    foilList = foilDict[gradename]
    for target in targetList:
        target = str(target)
        for foil in foilList:
            #calculating scores
            lev_score = NDLevdist(target,foil)
            cmu_score = NDLevdist(cmuDict[target.lower()],cmuDict[foil.lower()])

            if lev_score!=0 and cmu_score!=0: #lev_score!=0  ~= target!=foil
                if grade in grade_2bletter:
                    if foil in look[target.upper()]: so = 'look_alike'
                    else: so ='no_look_alike'
                elif grade in (grade_2button + grade_4button):
                    if lev_score <= lev_cutoff[gradename]: so = 'look_alike'
                    elif lev_score > lev_cutoff[gradename]: so = 'no_look_alike'
                    # print grade, target,foil, so,'cmu',cmu_score,'lev',lev_score

                if so=='look_alike':
                    if cmu_score > cmu_cutoff[gradename]: n=1 #look_alike, don't sound alike
                    elif cmu_score <= cmu_cutoff[gradename]: n=2 #look alike, sound alike
                elif so=='no_look_alike':
                    if cmu_score <= cmu_cutoff[gradename]: n=0 #don't look alike, sound alike
                    elif cmu_score > cmu_cutoff[gradename]:n=3 #don't look, don't sound alike

                foilsIn[target] = foilsIn.get(target, {})
                foilsIn[target][n] = foilsIn[target].get(n, [])
                foilsIn[target][n].append(foil)
        foil1 = foilsIn.get(target, {}).get(0, []) #n=0 #don't look alike, sound alike
        foil2 = foilsIn.get(target, {}).get(1, []) #n=1 #look_alike, don't sound alike
        foil3 = foilsIn.get(target, {}).get(2, []) #n=2 #look alike, sound alike
        if grade in grade_4b_anagram: foil4 = foil_anagram[grade].get(target, [])
        else: foil4 = foilsIn.get(target, {}).get(3, []) #n=3 #don't look, don't sound alike

        if (foil1!=[] or foil2!=[] or foil3!=[]) and grade in (grade_2bletter + grade_2button):
            foil_max = max([len(foil1), len(foil2), len(foil3)])
            print grade, target, len(foil1), len(foil2), len(foil3), len(foil4)
            if foil1!=[]: 
                foil_2b = list(itertools.product([target],foil1,[''],[''],['']))
                foilDict_temp.extend(foil_2b)
            if foil2!=[]: 
                foil_2b = list(itertools.product([target],[''],foil2,[''],['']))
                foilDict_temp.extend(foil_2b)
            if foil3!=[]: 
                foil_2b = list(itertools.product([target],[''],[''],foil3,['']))
                foilDict_temp.extend(foil_2b)
            if foil4!=[]:
                if len(foil4)>=foil_max: foil_2b = list(itertools.product([target],[''],[''],[''],sample(foil4,foil_max)))
                else: foil_2b = list(itertools.product([target],[''],[''],[''],foil4))
                foilDict_temp.extend(foil_2b)
        elif grade in grade_4button:
            if (foil1!=[] and foil2!=[] and foil4!=[]):
                if foil3==[] or grade in grade_4b_anagram: #if there is no "look alike, sound alike" or if we're on anagram level
                    foil_min = min([len(foil1), len(foil2), len(foil4)])
                    foil_4b = list(itertools.product([target],sample(foil1,foil_min),sample(foil2,foil_min),[''],sample(foil4,foil_min)))
                    foilDict_temp.extend(foil_4b)
                else:
                    foil_min = min([len(foil1), len(foil2), len(foil3), len(foil4)])
                    foil_4b = list(itertools.product([target],sample(foil1,foil_min),sample(foil2,foil_min),sample(foil3,foil_min),['']))
                    foilDict_temp.extend(foil_4b)
                print grade, target, len(foil1), len(foil2), len(foil3), len(foil4)
    for i in range(0,5): shuffle(foilDict_temp)
    return foilDict_temp


for grade in gradelevel:
    tList=[]; fList1=[]; fList2=[]; fList3=[]; fList4=[]

    print '---- processing', grade, '----'
    tfList = target_foil_processing(grade)

    for i in range(0,len(tfList)):
        tList.append(tfList[i][0])
        fList1.append(tfList[i][1]) #n=0 #don't look alike, sound alike
        fList2.append(tfList[i][2]) #n=1 #look_alike, don't sound alike
        fList3.append(tfList[i][3]) #n=2 #look alike, sound alike
        fList4.append(tfList[i][4]) #n=3 #don't look, don't sound alike
    outrow = {'Difficulty': difficulty,
    'Grade': grade,
    'Target': tList,
    'Foil_sound_alike': fList1,
    'Foil_look_alike': fList2,
    'Foil_sound_look_alike': fList3,
    'Foil_no_sound_look': fList4}

    writer.writerow(outrow)
    print 'writing done'

    difficulty +=1

stimfile.close()




