import os, math, csv, itertools, jellyfish, nltk
import pandas as pd
from jellyfish import metaphone
from pyxdameraulevenshtein import damerau_levenshtein_distance as DLevdist
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as NDLevdist
import random, numpy
from random import choice, shuffle, sample
from operator import mul, itemgetter
import string

# os.chdir('/Users/Ratnaganadi_Paramita/Work/LDRH_Task/LDRH_Reading/stimulus_generator')
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
#reads in sheet
sheet = pd.read_excel('combined_gradewordlist_with_toolbox.xlsx','Sheet1',index_col='No',na_values=['NA'])

#preparing output file
stimfile = open('stimulus_gradelist_anagram.csv', 'w')
fieldnames = ['Difficulty','Grade','Criteria','Target_4button','Target_sound_alike','Target_look_alike','Target_sound_look_alike','Target_no_sound_look','Foil_sound_alike','Foil_look_alike','Foil_sound_look_alike','Foil_no_sound_look']
fieldnames_anagram=['Grade','Target','Anagram_word','Anagram_non_word']
headers = dict((n,n) for n in fieldnames)
writer = csv.DictWriter(stimfile,fieldnames=fieldnames, lineterminator= '\n')
writer.writerow(headers)


## INITIALIZE DICTIONARIES & OTHER VARIABLES ##
difficulty = 1
wordDict = {} #dictionary of words for each grade level
cmuDict = {} #dictionary of cmu transcriptions
foilDict = {} #to store all possible foils a grade can have
targetDict_2b = {}
foilDict_2b = {}
foil_2b = {}
criteriaDict = {} #dictionary of all possible foils for all grade levels
targetDict_4b = {}
foilDict_4b = {}
foil_4b = {}
foilDict_4b1 = {}
foilDict_4b2 = {}
foilDict_4b3 = {}
foilDict_4b4 = {}
foil_anagram = {}
criteria = ['sound_alike','look_alike','sound_look_alike','no_sound_look']
criteria_name = ''
grade_2bletter = ['letter','lettersound']
grade_2button = ['k','grade1a','grade1b']
grade_4b = ['grade2','grade3','grade4']
grade_4b_anagram = ['grade2_anagram','grade3_anagram','grade4_anagram']
grade_4button = grade_4b + grade_4b_anagram
gradelevel = grade_2bletter + grade_2button + grade_4b + grade_4b_anagram
gradelvl = ['k','grade1a','grade1b','grade2','grade3','grade4','grade5'] #grade levels names
letter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
sound = ['B','D','F','H','J','K','L','M','N','P','R','S','T','V','W','Y','Z']
look = {'A':['K','M','N','V','W','X','Y'],'B':['D','E','H','O','P','R'],'C':['D','G','J','O','P','Q','S','U'],'D':['B','C','G','J','O','P','Q','U'],'E':['B','F','H','M','N','W'],'F':['E','H','I','L','M','N','P','T'],'G':['C','D','J','O','P','Q','U'],'H':['B','E','F','I','L','M','N','T'],'I':['F','J','L','T'],'J':['C','G','I','L','U'],'K':['A','M','N','R','V','W','X','Y','Z'],'L':['F','H','T'],'M':['A','E','F','H','K','N','V','W','X','Y','Z'],'N':['A','E','F','H','K','M','V','W','X','Y','Z'],'O':['B','C','D','G','Q','U'],'P':['B','C','D','F','R'],'Q':['C','D','G','O','U'],'S':['C','Z'],'T':['F','H','I','L','Y'],'U':['C','D','G','J','O','Q','V','W','X','Y'],'V':['A','K','M','N','U','W','X','Y','Z'],'W':['A','K','M','N','U','V','X','Y','Z'],'X':['A','K','M','N','U','V','W','Y','Z'],'Y':['K','M','N','S','V','W','X','Z']}

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
    targetDict_2b[grade]={} #to store the final 2button target list for saving purposes
    foilDict_2b[grade]={} #to store the final 2button foil list for saving purposes
    foilDict[grade]={} #to store all possible foils a grade can have
    foil_2b[grade]={}
    targetDict_4b[grade]=[] #list of target word for 4 buttons
    foilDict_4b[grade]=[] #to store all 4 foils, ready for
    foil_4b[grade]={} #to store all 4 foils
    foilDict_4b1[grade]=[]
    foilDict_4b2[grade]=[]
    foilDict_4b3[grade]=[]
    foilDict_4b4[grade]=[]
    foil_anagram[grade]={}
    
    #initializing lists
    for name in criteria: 
        tfDict[grade][name]=[] #for different criteria in each grade level
        targetDict_2b[grade][name]=[] #for target
        foilDict_2b[grade][name]=[] #for foils
        # foil_4b[grade][name]={} #list of foils only, indexed by target word for 4 buttons

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
    for ltr in letter: cmuDict[ltr] = ''.join((gr_cmudict[ltr.lower()])[0])
    for word in wordDict[grade]: cmuDict[word]= ''.join((gr_cmudict[word.lower()])[0])

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
foilDict['k'] = (wordDict['k']) + (wordDict['grade1a'])
for i in range(1,len(gradelvl)-1): foilDict[gradelvl[i]] = (wordDict[gradelvl[i-1]]) + (wordDict[gradelvl[i]]) + (wordDict[gradelvl[i+1]])
# soundComb = list(itertools.combinations(sound,2))
foilSound=[]

#stimuli dictionary: {grade: {criteria: [target,...], [foil,...], [criteria,...], [lev,...], [cmu,...]}}
lev_cutoff = {'k':0.34,'grade1a':0.34,'grade1b':0.34 ,'grade2':0.29,'grade3':0.29,'grade4':0.29,'grade5':0.34} #lev_cutoff = {'k':0.33,'grade1a':0.33,'grade1b':0.33,'grade2':0.283,'grade3':0.286,'grade4':0.286, 'grade5':0.33}
cmu_cutoff = {'letter':0.5,'lettersound':0.5,'k':0.34,'grade1a':0.34,'grade1b':0.21,'grade2':0.21,'grade3':0.21,'grade4':0.21,'grade5':0.23} #cmu_cutoff = {'k':0.33,'grade1a':0.33,'grade1b':0.2,'grade2':0.2,'grade3':0.2,'grade4':0.2,'grade5':0.22}
c = ['sound_alike','look_alike','sound_look_alike','no_sound_look']
look = {'A':['K','M','N','V','W','X','Y'],'B':['D','E','H','O','P','R'],'C':['D','G','J','O','P','Q','S','U'],'D':['B','C','G','J','O','P','Q','U'],'E':['B','F','H','M','N','W'],'F':['E','H','I','L','M','N','P','T'],'G':['C','D','J','O','P','Q','U'],'H':['B','E','F','I','L','M','N','T'],'I':['F','J','L','T'],'J':['C','G','I','L','U'],'K':['A','M','N','R','V','W','X','Y','Z'],'L':['F','H','T'],'M':['A','E','F','H','K','N','V','W','X','Y','Z'],'N':['A','E','F','H','K','M','V','W','X','Y','Z'],'O':['B','C','D','G','Q','U'],'P':['B','C','D','F','R'],'Q':['C','D','G','O','U'],'S':['C','Z'],'T':['F','H','I','L','Y'],'U':['C','D','G','J','O','Q','V','W','X','Y'],'V':['A','K','M','N','U','W','X','Y','Z'],'W':['A','K','M','N','U','V','X','Y','Z'],'X':['A','K','M','N','U','V','W','Y','Z'],'Y':['K','M','N','S','V','W','X','Z']}


for target in letter:
    for foil in letter:
        if target!=foil:
            cmu_score = NDLevdist(cmuDict[target],cmuDict[foil])
            if cmu_score<0.5: #if sound alike
                if foil in look[target]: #sound alike, look alike
                else: #sound alike, don't look alike


# for x in soundComb:
#     cmu_score = NDLevdist(cmuDict[x[0]],cmuDict[x[1]])
#     if cmu_score < 0.5: foilSound.append(x)


def target_foil_processing(grade,targetList,foilList):
    so = None
    for target in targetList:
        target = str(target)
        for foil in foilList:
            lev_score = NDLevdist(target,foil)
            cmu_score = NDLevdist(cmuDict[target],cmuDict[foil])

            if target!=foil:
                #calculating scores
                lev_score = NDLevdist(target,foil)
                cmu_score = NDLevdist(cmuDict[target],cmuDict[foil])
                # lev_cmu = lev_score * cmu_score
                # sumsqrt_lev_cmu = math.sqrt((lev_score)**2 + (cmu_score)**2)
                foilsIn = {}
                if lev_score!=0 and cmu_score!=0:
                    if grade in grade_2bletter:
                        foilsIn = foil_2b[grade]
                        if foil in look[target]: so = 'look_alike'
                        else: so ='no_look_alike'
                    elif grade in (grade_2button + grade_4button):
                        foilsIn = foil_4b[grade]
                        if lev_score <= lev_cutoff[gradename]: so = 'look_alike'
                        elif cmu_score > cmu_cutoff[gradename]: so = 'no_look_alike'

                    if so=='look_alike':
                        if cmu_score > cmu_cutoff[gradename]: n=1 #look_alike, don't sound alike
                        elif cmu_score <= cmu_cutoff[gradename]: n=2 #look alike, sound alike
                    elif so=='no_look_alike':
                        if cmu_score <= cmu_cutoff[gradename]: n=0 #don't look alike, sound alike
                        elif cmu_score > cmu_cutoff[gradename]:n=3 #don't look, don't sound alike


                    foilsIn[target] = foilsIn.get(target, {})
                    foilsIn[target][n] = foilsIn[target].get(n, [])
                    foilsIn[target][n].append(foil)


# foil_len={}
for grade in gradelevel:
    foil_len[grade]=[0,0,0,0]
    gradename = grade.split("_")[0]
    print grade,'len', len(wordDict[gradename])

    if grade == letter:
        current_targetList = letter
        current_foilList = letter
        
        for target in letter:
        for foil in letter:
            if target!=foil:
                cmu_score = NDLevdist(cmuDict[target],cmuDict[foil])
                if foil in look[target]:
                    if cmu_score > cmu_cutoff[gradename]: n=1 #look_alike, don't sound alike
                    elif cmu_score <= cmu_cutoff[gradename]: n=2 #look alike, sound alike
                else:
                    if cmu_score <= cmu_cutoff[gradename]: n=0 #don't look alike, sound alike
                    elif cmu_score > cmu_cutoff[gradename]:n=3 #don't look, don't sound alike
                
                tfDict[gradename][criteria[n]].append([target,foil])

    elif grade in (grade_2button + grade_4button):
        current_targetList = wordDict[gradename]
        current_foilList = foilDict[gradename]

        for target in current_targetList:
            target = str(target)
            for foil in current_foilList:
                if target!=foil:
                    #calculating levenshtein(orthographic) and cmu(phonological) scores
                    lev_score = NDLevdist(target,foil)
                    cmu_score = NDLevdist(cmuDict[target],cmuDict[foil])
                    # lev_cmu = lev_score * cmu_score
                    # sumsqrt_lev_cmu = math.sqrt((lev_score)**2 + (cmu_score)**2)

                    #setting lev_score and cmu_score cutoff for the different criteria: ['sound_alike','look_alike','sound_look_alike','no_sound_look']
                    if lev_score!=0 and cmu_score!=0:
                        if lev_score <= lev_cutoff[gradename]:
                            if cmu_score > cmu_cutoff[gradename]: n=1 #look_alike, don't sound alike
                            elif cmu_score <= cmu_cutoff[gradename]: n=2 #look alike, sound alike
                        elif lev_score > lev_cutoff[gradename]:
                            if cmu_score <= cmu_cutoff[gradename]: n=0 #don't look alike, sound alike
                            elif cmu_score > cmu_cutoff[gradename]:n=3 #don't look, don't sound alike

                        #for 2buttons - creating [target,foil] list for 2 button trials for different criteria list
                        if grade in grade_2button:
                            criteria_name = criteria[n]
                            foil_2b[gradename][criteria_name].append([target,foil])
                        #for 4buttons - create a list of all possible foil for indexed by categories, and target word
                        elif grade in grade_4button:
                            foil_4b[gradename][target] = foil_4b[gradename].get(target, {})
                            foil_4b[gradename][target][n] = foil_4b[gradename][target].get(n, [])
                            foil_4b[gradename][target][n].append(foil)

            if grade in grade_4button or grade in grade_4b_anagram:
                #store all 4 foil categories in a temporary list, and calculate its length for each target
                foil1_temp = foil_4b[gradename].get(target, {}).get(0, [])
                foil1_ln = len(foil1_temp)
                foil2_temp = foil_4b[gradename].get(target, {}).get(1, [])
                foil2_ln = len(foil2_temp)
                foil3_temp = foil_4b[gradename].get(target, {}).get(2, [])
                foil3_ln = len(foil3_temp)
                if grade in grade_4b:
                    foil4_temp = foil_4b[gradename].get(target, {}).get(3, [])
                    foil4_ln = len(foil4_temp)
                elif grade in grade_4b_anagram:
                    foil4_temp = foil_anagram[grade].get(target, [])
                    foil4_ln = len(foil4_temp)
                #see how many words 
                # if grade=='grade5' and (foil1_temp!=[] or foil2_temp!=[] or foil3_temp!=[] or foil4_temp!=[]):
                    # print grade,',',target,',', foil1_ln, foil2_ln, foil3_ln, foil4_ln
                if (foil1_temp!=[] and foil2_temp!=[] and foil4_temp!=[]):
                    print grade,',',target,',', foil1_ln, foil2_ln, foil3_ln, foil4_ln
                    if foil3_temp==[] or grade in grade_4b_anagram:
                        foil_min = min([foil1_ln, foil2_ln, foil4_ln])
                        foil_4b_temp = list(itertools.product([target],sample(foil1_temp,foil_min),sample(foil2_temp,foil_min),[''],sample(foil4_temp,foil_min)))
                    else: 
                        foil_min = min([foil1_ln, foil2_ln, foil3_ln, foil4_ln]) #; print 'foil_min', foil_min
                        foil_4b_temp = list(itertools.product([target],sample(foil1_temp,foil_min),sample(foil2_temp,foil_min),sample(foil3_temp,foil_min),['']))
                    (foilDict_4b[grade]).extend(foil_4b_temp)
                # print foilDict_4b[grade]
        # print 'foil_len', grade, foil_len[grade]

    #appending and writing [target,foil] into an csv file for 2-button-trials
    if grade in grade_2button:
        criteriaDict[grade]=[]
    
        #create a 100 randomized criteria for all grade k, 1a, 1b
        for i in range(0,100):
            criteria_choice = random.choice(c)
            criteriaDict[grade].append(criteria_choice)

        for name in criteria:
            shuffle(foil_2b[grade][name]) #shuffle items in the list
            if name==criteria[3]: foil_2b[grade][name] = foil_2b[grade][name][:500] #size down the 'no_sound_look' list to 500 items
            print grade, name, len(foil_2b[grade][name])

            #after the list/order is shuffled, put target and foil in a different list
            for i in range(0,len(foil_2b[grade][name])-1):
                (targetDict_2b[grade][name]).append(foil_2b[grade][name][i][0])
                (foilDict_2b[grade][name]).append(foil_2b[grade][name][i][1])

        outrow = {'Difficulty': difficulty,
            'Grade': grade,
            'Criteria': criteriaDict[grade],
            'Target_4button': None,
            'Target_sound_alike': targetDict_2b[grade]['sound_alike'],
            'Target_look_alike': targetDict_2b[grade]['look_alike'],
            'Target_sound_look_alike': targetDict_2b[grade]['sound_look_alike'],
            'Target_no_sound_look': targetDict_2b[grade]['no_sound_look'],
            'Foil_sound_alike': foilDict_2b[grade]['sound_alike'],
            'Foil_look_alike': foilDict_2b[grade]['look_alike'],
            'Foil_sound_look_alike': foilDict_2b[grade]['sound_look_alike'],
            'Foil_no_sound_look': foilDict_2b[grade]['no_sound_look']}
        
        writer.writerow(outrow)
        print 'writing done'

        difficulty+=1

    elif grade in grade_4button or grade in grade_4b_anagram:
        for i in range(0,5):
            shuffle(foilDict_4b[grade])
        for i in range (0,(len(foilDict_4b[grade]))): #500):
            (targetDict_4b[grade]).append(foilDict_4b[grade][i][0]) #target
            (foilDict_4b1[grade]).append(foilDict_4b[grade][i][1]) #criteria0 - sound alike, don't look alike
            (foilDict_4b2[grade]).append(foilDict_4b[grade][i][2]) #criteria1 - look alike, don't sound alike
            (foilDict_4b3[grade]).append(foilDict_4b[grade][i][3]) #criteria2 - sound & look alike
            (foilDict_4b4[grade]).append(foilDict_4b[grade][i][4]) #criteria3 - no_sound_look
        # print grade, len(targetDict_4b[grade])
        outrow = {'Difficulty': difficulty,
            'Grade': grade,
            'Criteria': None,
            'Target_4button': targetDict_4b[grade],
            'Target_sound_alike': None,'Target_look_alike': None,'Target_sound_look_alike': None,'Target_no_sound_look': None,
            'Foil_sound_alike': foilDict_4b1[grade],
            'Foil_look_alike': foilDict_4b2[grade],
            'Foil_sound_look_alike': foilDict_4b3[grade],
            'Foil_no_sound_look': foilDict_4b4[grade]}

        writer.writerow(outrow)
        print 'writing done'

        difficulty+=1

stimfile.close()