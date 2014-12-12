# -*- coding: utf-8 -*-
from psychopy import visual, core, data, event, logging, gui, sound
from psychopy.constants import *
import os, random, math, copy, xlwt, numpy, csv, itertools
from xlrd import open_workbook
from xlutils.copy import copy as xlcopy
import cPickle as pickle
from random import shuffle, choice
from datetime import datetime
from Math_Task import LDRH_math_obj_4_choice_w_gradeinfo as Math_Script
from Tones_Task import LDRH_tones_obj_w_gradeinfo as Tones_Script
from Dots_Task import LDRH_panamath_boxes_obj_w_gradeinfo as Dots_Script
from Reading_Task import LDRH_reading_obj_4buttons_inst_gradeinfo as Reading_Script
from Phonology_Task import LDRH_phonology_obj_w_gradeinfo as Phonology_Script
from Star_Task import LDRH_spatial_obj_w_gradeinfo as Star_Script
from Feedback import feedback

try:
    import taskversion
    VERSION = taskversion.__doc__
except ImportError as e:
    VERSION = "no_version"

#enable pickling of data
pickle_enabled = False

#touchscreen? if False, uses conventional mouse
touchscreen = True

#How many alternatives in the choice phase
number_of_choices = 2

#which tasks to run
task_names=[
    'Spatial',
    'Phonology',
    'Math',
    'Music',
    'Reading',
    'Dots',
]

#store info about the experiment session
expName='REaCh Task'
expInfo={'participant':'','grade':'', 'choice': False}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False:
    core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()
expInfo['expName']=expName
just_choice = expInfo['choice']
# Setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data')  # if this fails (e.g. permissions) we will get error
subject_ID = (str(expInfo['participant'])).split('_')[0]
grade = str(expInfo['grade'])
filename = 'data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
ppt = expInfo['participant']
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Check for pickle
if os.path.isfile('data.p') and pickle_enabled:
    f = open('data.p', 'r')
    pdata = pickle.load(f)
    if ppt in pdata.keys():
        dates = pdata[ppt].keys()
        dlg = gui.Dlg(title="Found previous data")
        if len(dates)==1:
            dlg.addText('An incomplete dataset was found for this participant from {}, would you like to resume that session?'.format(dates[0]))
        elif len(dates)>1:
            query = '{} incomplete datasets were found for this participant from the following dates:'.format(len(dates))
            for date in dates: query = query+'\n\t{}'.format(date)
            query = query+'\nWould you like to resume one of those sessions?'
            dlg.addText(query)
        dlg.addField('Resume:', choices=['Yes','No'])
        dlg.show()  # show dialog and wait for OK or Cancel
        if dlg.OK:  # then the user pressed OK
            print dlg.data
            use_pickle=dlg.data[0]=='Yes'
            if len(dates)==1:
                this_pdata = pdata.pop(ppt)[dates[0]]
                old_date = dates[0]
            elif len(dates)>1:
                datedlg = gui.Dlg(title="Choose session")
                datedlg.addText('Please choose the incomplete session for {} that you would like to resume:'.format(ppt))
                datedlg.addField('Session:', choices=dates)
                datedlg.show()
                if datedlg.OK:
                    this_pdata=pdata[ppt].pop(datedlg.data[0])
                    old_date = datedlg.data[0]
                else: core.quit()
        else: core.quit()
        f.close()
        f = open('data.p', 'w')
        pickle.dump(pdata, f)
        f.close()
        pdata = this_pdata
        old_filename = os.path.join('data', '{}_{}.xls'.format(ppt, old_date))
        if not os.path.isfile(old_filename):
            print 'could not find old data-- looked for {}'.format(old_filename)
            core.quit()
    else: pdata=None
else: pdata=None

def can_evaluate(value):
    try:
        eval(value)
        return True
    except:
        return False

def importConditions(path):
    out = []
    with open(path, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        for row in reader:
             out.append(dict(zip(headers,[eval(cell) if can_evaluate(cell) else cell for cell in row])))
    return out

#conditions files to read in
all_conditions = {
    'Math': {
        'addition': importConditions('Math_Task/math_stims_addition.csv'),
        'subtraction': importConditions('Math_Task/math_stims_subtraction.csv'),
        'multiplication': importConditions('Math_Task/math_stims_multiplication.csv'),
        'division': importConditions('Math_Task/math_stims_division.csv')
        },
    'Dots': importConditions('Dots_Task/dots_conds2.csv'),
    'Reading': importConditions('Reading_Task/readingstim_anagram_new.csv'),
    'Phonology': importConditions('Phonology_Task/phonology_stims_new.csv'),
    'Spatial': None,
    'Music': importConditions('Tones_Task/tones_stims_new.csv')}

#[Music, Phonology, Dots, Reading, Spatial]
low_thresh = {
    'Music':len(all_conditions['Music'])-1,
    'Phonology':len(all_conditions['Phonology'])-1,
    'Dots':len(all_conditions['Dots'])-1,
    'Reading':len(all_conditions['Reading'])-1,
    'Spatial':150
}
low_thresh_operations = {'addition': len(all_conditions['Math']['addition'])-1}

math_operations = ['addition','subtraction','multiplication','division']

#load pickled data if applicable
if pdata:
    for k in pdata.keys():
        exec('{} = pdata[k]'.format(k))
    wb_read = open_workbook(old_filename)
    wb = xlcopy(wb_read)
    all_sheets = {}
    for i, sheet in enumerate(wb_read.sheet_names()):
        ws_read = wb_read.sheet_by_index(i)
        all_sheets[sheet] = dict(sheet = wb.get_sheet(i), headers=[ws_read.cell_value(0,col) for col in range(ws_read.ncols)], row=ws_read.nrows)

else:
    print 'loading things outside of pickle'
    points = 0
    thesePoints=0
    first_pass=True
    trial_number = 1

    #create output structure
    wb = xlwt.Workbook()
    choice_headers = [("choice_task_{choice}".format(choice=i+1), "choice_points_{choice}".format(choice=i+1), "choice_pos_{choice}".format(choice=i+1))[j%3] for j,i in enumerate(sorted(range(0, number_of_choices)*3))]

    all_sheets = {
        # 'Main': dict(sheet = wb.add_sheet('Main'), headers = 'subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','spatial_click1','spatial_click2','stim1','stim2','resp','resp_pos','target','target_pos','resp_target_dist','foil1','foil1_pos','foil2','foil2_pos','foil3','foil3_pos','foil4','foil4_pos','phoneme_difference','POA_steps','VOT_steps','VOT_or_POA','phoneme_dif_pos','phoneme_dist','tones_details','tones_contour','tones_notes_different','tones_root','choice_icon_pos','task_version'], row=1),
        'Spatial': dict(sheet = wb.add_sheet('Spatial'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','spatial_click1','spatial_click2','resp_pos','target_pos','resp_target_dist','task_version'], row=1),
        'Phonology': dict(sheet = wb.add_sheet('Phonology'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','stim1','stim2','resp','resp_pos','target','target_pos','phoneme_difference','POA_steps','VOT_steps','VOT_or_POA','phoneme_dif_pos','phoneme_dist','task_version'], row=1),
        'Math': dict(sheet = wb.add_sheet('Math'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','stim','resp','resp_pos','target','target_pos','foil1','foil1_pos','foil2','foil2_pos','foil3','foil3_pos','task_version'], row=1),
        'Music': dict(sheet = wb.add_sheet('Music'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','stim1','stim2','resp','resp_pos','target','target_pos','tones_details','tones_contour','tones_notes_different','tones_root','task_version'], row=1),
        'Reading': dict(sheet = wb.add_sheet('Reading'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','resp','resp_pos','target','target_pos','foil1','foil1_pos','foil2','foil2_pos','foil3','foil3_pos','foil4','foil4_pos','task_version'], row=1),
        'Dots' dict(sheet = wb.add_sheet('Dots'), headers = ['subject_ID','task','type','trial_number','threshold_var','level','score','resp_time','resp','resp_pos','target','target_pos','task_version'], row=1)
        'Task_Times': dict(sheet = wb.add_sheet('Task_Times'), headers = ['task','instructions','practice','staircase','total', 'task_version'],row=1)}
    }
    # all_sheets = {
    #     'Main': dict(sheet = wb.add_sheet('Main'), headers=['trial_number', 'task', 'level', 'score','type','choice_icon_pos', 'task_version'] + choice_headers, row=1),
    #     'Math': dict(sheet = wb.add_sheet('Math'), headers = ['trial_number', 'Operation', 'level','Stimulus','Target','Foil1','Foil2','Foil3','score','Resp Time', 'task_version'], row=1),
    #     'Dots': dict(sheet = wb.add_sheet('Dots'), headers = ['trial_number', 'level','Correct','Incorrect','Ratio','score','Resp Time', 'task_version'], row=1),
    #     'Reading': dict(sheet = wb.add_sheet('Reading'), headers = ['trial_number', 'level','Grade','Target','Foil1','Foil2','Foil3','Foil4','Response','score','Resp Time', 'task_version'], row=1),
    #     'Phonology': dict(sheet = wb.add_sheet('Phonology'), headers = ['trial_number', 'level','Stim1','Stim2','Response','Correct Response','score','Resp Time','POA_steps','VOT_steps','VOT_or_POA','Difference Position','Distance','Number of Phonemes','Phoneme Difference', 'task_version'], row=1),
    #     'Spatial': dict(sheet = wb.add_sheet('Spatial'), headers = ['level', 'score', 'First_Click_Time', 'Second_Click_Time', 'Resp Time', 'Star_Pos', 'Resp_Pos', 'Resp_Distance', 'task_version'], row=1),
    #     'Music': dict(sheet = wb.add_sheet('Music'), headers = ['trial_number', 'level', 'soundA','soundB','Details','Contour','Notes Different','Root','Response','Correct Response','score','Resp Time', 'task_version'], row=1),
    #     'Task_Times': dict(sheet = wb.add_sheet('Task_Times'), headers = ['task','instructions','practice','staircase','total', 'task_version'],row=1)}

    #initialize headers for each sheet
    for key in all_sheets.keys():
        for col, header in enumerate(all_sheets[key]['headers']): all_sheets[key]['sheet'].write(0,col,header)

    #create handlers
    all_handlers = {
        'Math': {
                'addition': data.StairHandler(startVal= len(all_conditions['Math']['addition'])-1, stepSizes=[2,1,1,1],
                    minVal=0, maxVal=len(all_conditions['Math']['addition'])-1, nUp=1, nDown=3, nTrials=10, stepType = 'lin'),
                'subtraction': data.StairHandler(startVal= len(all_conditions['Math']['subtraction'])-1, stepSizes=[2,1,1,1],
                    minVal=0, maxVal=len(all_conditions['Math']['subtraction'])-1, nUp=1, nDown=3, nTrials=10, stepType = 'lin'),
                'multiplication': data.StairHandler(startVal= len(all_conditions['Math']['multiplication'])-1, stepSizes=[2,1,1,1],
                    minVal=0, maxVal=len(all_conditions['Math']['multiplication'])-1, nUp=1, nDown=3, nTrials=10, stepType = 'lin'),
                'division': data.StairHandler(startVal= len(all_conditions['Math']['division'])-1, stepSizes=[2,1,1,1],
                    minVal=0, maxVal=len(all_conditions['Math']['division'])-1, nUp=1, nDown=3, nTrials=10, stepType = 'lin')
                },
        'Music': data.StairHandler(startVal = 14, stepType = 'lin', stepSizes=[2,1,1,1,1,1], #reduce step size every two reversals
            minVal=0, maxVal=len(all_conditions['Music'])-1, nUp=1, nDown=3,  #will home in on the 80% threshold
            nTrials = 10),
        'Dots': data.StairHandler(startVal = 35, stepType = 'lin', stepSizes=[5,3,2,2,1,1], #reduce step size every two reversals
            minVal=0, maxVal=len(all_conditions['Dots'])-1, nUp=1, nDown=3,  #will home in on the 80% threshold
            nTrials = 10),
        'Reading': data.StairHandler(startVal = 8, stepType = 'lin', stepSizes=[1,1,1,1], #reduce step size every two reversals
            minVal=0, maxVal=len(all_conditions['Reading'])-1, nUp=1, nDown=3,  #will home in on the 80% threshold
            nTrials = 10, nReversals = 0),
        'Phonology': data.StairHandler(startVal = 4, stepType = 'lin', stepSizes=[1,1,1,1], #reduce step size every two reversals
            minVal=0, maxVal=len(all_conditions['Phonology'])-1, nUp=1, nDown=3,  #will home in on the 80% threshold
            nTrials = 10, nReversals = 0),
        'Spatial': data.StairHandler(startVal = 150,
            stepType = 'db', stepSizes=[3,3,2,2,1,1],#[8,4,4,2,2,1,1], #reduce step size every two reversals
            minVal=0, maxVal=350, nUp=1, nDown=3,  #will home in on the 80% threshold
            nTrials = 10)
        }

    #dictionry of ring tracking
    num_rings = {'Math': 4, 'Music': 4, 'Reading': 4, 'Dots': 4, 'Phonology': 4, 'Spatial': 4}

    #dictionary of threshold tracking
    all_thresholds = {}

    #create list to randomize order of presentation
    # shuffle(task_names)
    staircased = []

if just_choice:
    for task in task_names:
        if task=='Math':
            for operation in math_operations:
                all_thresholds[operation] = all_handlers[task][operation].startVal
        else:
            all_thresholds[task] = all_handlers[task].startVal
    dialog=gui.DlgFromDict(dictionary=all_thresholds,title="Thresholds (set to -1 to exclude)")
    if dialog.OK==False:
        core.quit() #user pressed cancel
    all_thresholds["Math"] = {}
    for operation in math_operations:
        if all_thresholds[operation] > -1:
            all_thresholds["Math"][operation] = all_thresholds[operation]
        del all_thresholds[operation]

# Initialize things regardless of pickle
win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix', fullscr=True) #Window
trialClock=core.Clock()
image_choice_path = 'Images/Choice/'
audio_path = 'Audio/General/'
aud_inst_path = 'Audio/Instructions/'

retry_instructions = visual.TextStim(win=win, text='Touch anywhere to try again.', height=28)
#choice_instructions = visual.TextStim(win=win, height=28, wrapWidth=800, text=
#    "Now we are going to play all of the games together. In this next part you can choose which game you want to play by touching one of the game buttons on the screen. Each time you play, you will earn points that will fill up the colored bar at the top of the screen. Each game button will have colored rings. The more rings there are, the more points you'll earn for playing that game. For example, a game button with four rings will give you a lot of points. But another game that has less rings or no rings will give you less points. You can still play the game button that has no rings. You will win when the colored bar on top is fully colored! \n\n\n\n\nTouch anywhere on the screen to play.")
instructions = visual.MovieStim(win=win,filename = aud_inst_path + 'choice_instructions.mp4', size = [1500,850], flipHoriz = True)
audio_inst = sound.Sound(aud_inst_path + 'choice_instructions.wav')
math_icon = visual.ImageStim(win=win, image = image_choice_path + 'math.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
dots_icon = visual.ImageStim(win=win, image = image_choice_path + 'panamath.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
reading_icon = visual.ImageStim(win=win, image = image_choice_path + 'reading.png', units = 'pix', ori = 0, pos = [0,0], size = [126, 120], opacity = 1, mask =None, interpolate = True)
phonology_icon = visual.ImageStim(win=win, image = image_choice_path + 'phonology2.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
spatial_icon = visual.ImageStim(win=win, image = image_choice_path + 'stars.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
music_icon = visual.ImageStim(win=win, image = image_choice_path + 'music.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
selection_circle = visual.ImageStim(win=win, image = image_choice_path + 'selection_circle.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
progress_frame = visual.Rect(win=win, units='pix',pos=[0,300],size=[1206,56],lineColor='white',fillColor=None,lineWidth=3)
progress_fill = visual.Rect(win=win, units='pix',pos=[0,300],size=[0,30], fillColor='lime', lineColor='lime')
progress_animation = visual.Rect(win=win, units='pix',pos=[0,300],size=[0,30], fillColor='lime')

math_benchmarks = {'subtraction': {'addition': {'thresh': 3, 'count': 0}}, 'multiplication': {'addition': {'thresh': 5, 'count': 0}, 'subtraction': {'thresh': 3, 'count': 0}}, 'division': {'multiplication': {'thresh': 3, 'count': 0}}}

congratulations_text = visual.TextStim(win=win, text="You did it! You win!", height=38, pos = [0,200])

try:
    fireworks = visual.MovieStim(win=win, filename=audio_path + 'fireworks.mp4', pos = [0,-100])
except AttributeError:
    fireworks = None

applause = sound.Sound(audio_path + 'applause.wav')
applause.setVolume(0.6)

score = visual.TextStim(win, units = 'pix', ori=0, font=u'Arial', pos=[0, -10], color=u'white', text='000')
cash_register = sound.Sound(value= audio_path + 'cash_register.wav')
cash_register.setVolume(0.2)
mouse=event.Mouse(win=win)
mouse.setVisible(0)
mouse.getPos()
point_intervals=12

#create rings and store in dictionary
colors_for_rings=['red','orange','light_orange','yellow']
all_rings = {'Math': {}, 'Dots': {}, 'Reading': {}, 'Phonology': {}, 'Spatial': {}, 'Music': {}}
for ring in range(len(colors_for_rings)):
    all_rings['Math'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)
    all_rings['Dots'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)#copy.copy(all_rings['Math'][ring])
    all_rings['Reading'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)#copy.copy(all_rings['Math'][ring])
    all_rings['Phonology'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)#copy.copy(all_rings['Math'][ring])
    all_rings['Spatial'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)#copy.copy(all_rings['Math'][ring])
    all_rings['Music'][ring] = visual.ImageStim(win=win, image = image_choice_path + '%s_ring.png' %colors_for_rings[ring], units = 'pix', ori = 0, pos = [0,0], size = [134+(ring*17), 134+(ring*17)], opacity = 1, mask =None, interpolate = True)#copy.copy(all_rings['Math'][ring])

#initialize games
all_games = {'Math': Math_Script.Math_Game(win, all_conditions['Math']),
    'Music': Tones_Script.Tones_Game(win, all_conditions['Music']),
    'Dots': Dots_Script.Dots_Game(win, all_conditions['Dots']),
    'Reading': Reading_Script.Reading_Game(win, all_conditions['Reading']),
    'Phonology': Phonology_Script.Phonology_Game(win, all_conditions['Phonology']),
    'Spatial': Star_Script.Star_Game(win)}

#dictionary of icons
all_icons = {'Math': math_icon, 'Music': music_icon, 'Reading': reading_icon, 'Dots': dots_icon, 'Phonology': phonology_icon, 'Spatial': spatial_icon}

#method to get clicks
if touchscreen:
    def click():
        if mouse.mouseMoved(): return True
        else: return False
elif not touchscreen:
    def click():
        if mouse.getPressed()==[1,0,0]: return True
        else: return False

def save(complete=False):
    wb.save('data/'+ '%s_%s' %(ppt, expInfo['date']+'.xls'))
    if complete:
        wb.save('data/complete_data/'+ '%s_%s' %(ppt, expInfo['date']+'.xls'))

#save data to xls then quit
def save_and_quit(complete=False):
    save(complete=complete)
    core.quit()

#pickle data then save_and_quit
def pickle_and_quit():
    if not pickle_enabled: save_and_quit()
    # load previous pickle if exists
    if os.path.isfile('data.p'):
        f = open('data.p', 'r')
        pdata = pickle.load(f)
        f.close()
        f = open('data.p', 'w')
    else:
        pdata = {}
        f = open('data.p', 'w')

    # create dictionary to pickle
    this_pdata = dict(points=points, thesePoints=thesePoints, first_pass=first_pass, trial_number=trial_number,
        all_handlers=all_handlers, num_rings=num_rings,
        all_thresholds=all_thresholds, task_names=task_names)

    # nest dictionary into outer dicts with ppt and date as keys
    if ppt in pdata.keys():
        pdata[ppt][expInfo['date']] = this_pdata
    else:
        pdata[ppt] = {expInfo['date']: this_pdata}

    # dump, save, and quit
    pickle.dump(pdata, f)
    f.close()
    print 'pickled data to {}'.format(f)
    save_and_quit()

def run_staircase(task, operation=None):
    global trial_number
    if operation:
        handler = all_handlers[task][operation]
    else:
        handler = all_handlers[task]

    try:
        thisIncrement = handler.next()
        print 'thisIncrement:', thisIncrement
        #run game-- output is a dictionary of values
        if operation: output = all_games[task].run_game(win, grade, operation, thisIncrement)
        else: output = all_games[task].run_game(win, grade, thisIncrement)
        if output=='QUIT': pickle_and_quit()

        #first write trial number to output, then write the output variables
        header_for_all = [subject_ID,task,'threshold',trial_number]
        for col,header in enumerate(header_for_all):
            all_sheets[task]['sheet'].write(all_sheets[task]['row'],col,header)
        # all_sheets[task]['sheet'].write(all_sheets[task]['row'], 0, trial_number)

        for col,header in enumerate(all_sheets[task]['headers'][4:]):
            if header=="Task Version":
                all_sheets[task]['sheet'].write(all_sheets[task]['row'],col+4, VERSION)
            else:
                all_sheets[task]['sheet'].write(all_sheets[task]['row'],col+4, output[header])
        #increment row on output structure
        all_sheets[task]['row'] += 1

        #write output for main sheet
        "!!!!!!!!!!! LOOK AT IT AGAIN !!!!!!!!!!!!"
        main_output = {'trial_number':trial_number, 'task': task, 'level': output['level'],'score':output['score'],'type':'threshold','choice_icon_pos':'', 'task_version': VERSION}
        for col,header in enumerate(all_sheets['Main']['headers']):
            all_sheets['Main']['sheet'].write(trial_number, col, main_output.get(header, ""))

        #update handler only if not a "same" trial from tones or phonology
        #if 'Correct Response' in output.keys() and output['Correct Response'].lower() != 'same': all_handlers[task].addData(output['score'])
        #else: print 'same trial-- did not update stairhandler'
        handler.addData(output['score'])

        # This code is to boost the staircase level of 'lower' operations when a student is successful on
        # more difficult operations. As a first pass, this simply records a success in *all* operations up to the one
        # that the student achieves the success in.
        if operation and output['score']:
            operations = ['addition', 'subtraction', 'multiplication', 'division']
            for operation_name in operations[0:operations.index(operation)]:
                all_handlers[task][operation_name].addData(output['score'])

        #increment trial number
        trial_number+=1

        output['thisIncrement'] = thisIncrement

        save()

    except StopIteration:
        output={}
        output['score'] = 'StopIteration'
        output['thisIncrement'] = handler.intensities[-1]

    return output


#STAIRCASING SECTION

# set up timers
instructions_times = {}
practice_times = {}
staircasing_times = {}
total_times = {}

if not just_choice:
    #run through instructions, practice, and staircase for each task
    for task in [task for task in task_names if task not in all_thresholds.keys()]: #only loops through tasks with no threshold yet
        #display icon for the task
        all_icons[task].draw()
        win.flip()
        start_time=trialClock.getTime()
        while trialClock.getTime()<start_time+3:
            if event.getKeys(keyList=['q', 'escape']): pickle_and_quit()

        #run instructions for task
        instructions_start = trialClock.getTime()
        if all_games[task].run_instructions(win)=='QUIT': pickle_and_quit()
        instructions_times[task] = trialClock.getTime() - instructions_start

        #run practice for task
        practice_start = trialClock.getTime()
        if hasattr(all_games[task], 'run_practice'):
            if all_games[task].run_practice(win, grade)=='QUIT': pickle_and_quit()
        practice_times[task] = trialClock.getTime() - practice_start

        #run staircase; math needs special circumstances
        staircasing_start = trialClock.getTime()
        if task=='Math':
            if 'Math' not in all_thresholds.keys():
                all_thresholds['Math']={}
            streaks = {'addition': {}, 'subtraction': {}, 'multiplication': {}, 'division': {}}
            add_count_for_mult = 0
            active_operations = ['addition']

            while active_operations:
                for operation in math_operations:
                    if operation in active_operations:
                        #one trial of staircase is run here
                        output = run_staircase(task, operation=operation)

                        for new_operation, reqs in math_benchmarks.items():
                            if operation in reqs.keys() and output['score'] and (len(all_conditions[task][operation]) - output['thisIncrement']) >= reqs[operation]['thresh']: reqs[operation]['count']+=1
                        for new_operation, reqs in math_benchmarks.items():
                            if False not in [benchmark['count'] >=3 for req_operation, benchmark in reqs.items()]:
                                active_operations.append(new_operation)
                                math_benchmarks.pop(new_operation)
                                print '{} is now active'.format(new_operation)
                        #separate logic for OR case with multiplication
                        if operation=='addition' and output['score'] and (len(all_conditions[task]['multiplication']) - output['thisIncrement']) >= 6:
                            add_count_for_mult+=1

                        if 'multiplication' not in active_operations and 'multiplication' in math_benchmarks.keys() and add_count_for_mult >= 3:
                            active_operations.append('multiplication')
                            math_benchmarks.pop('multiplication')
                            print '{} is now active'.format(new_operation)

                        #handle StopIterations
                        if output['score']=='StopIteration':
                            if sum(streaks.get(operation, {}).get(output['thisIncrement'], []))/float(len(streaks.get(operation, {}).get(output['thisIncrement'], []))) >= 0.8:
                                all_thresholds[task][operation] = output['thisIncrement']
                            else:
                                all_thresholds[task][operation] = min(output['thisIncrement'] + 1, len(all_conditions[task][operation])-1)
                            #record threshold and remove operation
                            active_operations.remove(operation)
                            continue

                        #keep track of streaks
                        streaks[operation][output['thisIncrement']] = streaks[operation].get(output['thisIncrement'], []) + [output["Score"]]

                        #handle streak breaking
                        if (len(streaks[operation][output['thisIncrement']]) > 9) and (sum(streaks[operation][output['thisIncrement']])/float(len(streaks[operation][output['thisIncrement']])) >= 0.8):
                            all_thresholds[task][operation] = output['thisIncrement']
                            active_operations.remove(operation)
                        #remove operation from being active, don't record a threshold
                        if output['thisIncrement']==len(all_conditions[task][operation])-1:
                            if (len(streaks[operation][output['thisIncrement']]) > 3) and (sum(streaks[operation][output['thisIncrement']])/float(len(streaks[operation][output['thisIncrement']])) <= 0.5):
                                active_operations.remove(operation)

                #add new operation if applicable
                for new_operation, reqs in math_benchmarks.items():
                    if new_operation in all_thresholds[task].keys(): continue

                    if False not in [req_operation in all_thresholds[task].keys() and (len(all_conditions[task][req_operation]) - all_thresholds[task][req_operation]) >= benchmark for req_operation, benchmark in reqs.items()]:
                        active_operations.append(new_operation)
                        print 'added', new_operation

        else:
            streaks = {}
            while True:
                #one trial of staircase is run here
                output = run_staircase(task)

                #handle StopIterations
                if output['score']=='StopIteration':
                    #record threshold and remove operation
                    if sum(streaks.get(output['thisIncrement'], []))/float(len(streaks.get(output['thisIncrement'], []))) >= 0.8:
                        all_thresholds[task] = output['thisIncrement']
                    else:
                        all_thresholds[task] = min(output['thisIncrement'] + 1, low_thresh[task])
                    break

                #keep track of streaks
                streaks[output['thisIncrement']] = streaks.get(output['thisIncrement'], []) + [output["Score"]]

                print 'pos_streak:', streaks[output['thisIncrement']]
                #handle streak breaking
                if len(streaks[output['thisIncrement']]) > 9:
                    if sum(streaks[output['thisIncrement']])/float(len(streaks[output['thisIncrement']])) >= 0.8:
                        all_thresholds[task] = output['thisIncrement']
                        break
                    if sum(streaks[output['thisIncrement']])/float(len(streaks[output['thisIncrement']])) <= 0.5:
                        break
        staircasing_times[task] = trialClock.getTime() - staircasing_start
        total_times[task] = instructions_times[task]+practice_times[task]+staircasing_times[task]
        save()

    print 'instruction times', instructions_times
    print 'practice_times', practice_times
    print 'staircasing times', staircasing_times
    print 'total times', total_times
    #record task times
    for task in task_names:
        all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],0, task)
        all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],1, instructions_times[task])
        all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],2, practice_times[task])
        all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],3, staircasing_times[task])
        all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],4, total_times[task])
        all_sheets['Task_Times']['row']+=1


#CHOICE SECTION

class Preference(object):

    def __init__(self, items, number_of_choices):
        self.points = 2
        self.items = [{"name": item, "points": self.points} for item in items]
        self.item_sequence = []
        self.number_of_choices = number_of_choices
        self.current_options = None
        self.preference_history = []

    def next(self):
        if not self.item_sequence:
            self.item_sequence = [item for item in itertools.combinations(self.items, self.number_of_choices)]
            random.shuffle(self.item_sequence)
        self.current_options = self.item_sequence.pop()
        return self.current_options

    def record_preference(self, task):
        if not self.current_options:
            raise Exception("There is no choice to make!")
        if task not in self.current_options:
            raise Exception("Invalid preference for current choices!")
        else:
            self.update_model(self.current_options, task)

    def update_model(self, options, choice):
        self.preference_history.append({
            "options": options,
            "choice": choice,
        })

#method to draw all icons, rings, and progress bar
def draw_main_screen(tasks):
    progress_frame.draw()
    progress_fill.draw()
    for num,task in enumerate(tasks):
        all_icons[task["name"]].draw()
        for ring in range(0, task["points"] - 1):
            all_rings[task["name"]][ring].draw()

#present instructions for choice task
choice_start = trialClock.getTime()
mouse.getPos()
audio_inst.play()
while instructions._player.time <= int(instructions.duration):
    instructions.draw()
    win.flip()
win.flip()

#choice_instructions.draw()
#win.flip()
while True:
    if click(): break
    if event.getKeys(['escape','q']): pickle_and_quit()
win.flip()

preferences = Preference(task_names, number_of_choices)

track_spatial_errors = []

while True:
    tasks = preferences.next()
    thesePoints=0
    progress_fill.setSize([points,50])
    #starting point =-250; position should be = -250 + 1/2 pos
    progress_fill.setPos([-300+ (points/4), 300])

    xy = [('left',[-200,0]),('right',[200,0]),('top-left',[-100,173]),('top-right',[100,173]),('bottom-right',[100,-173]),('bottom-left',[-100,-173])]
    xy = xy[0:number_of_choices]
    shuffle(xy)
    for num,task in enumerate(tasks):
        all_icons[task["name"]].setPos(xy[num][1])
        for ring in range(0, task["points"] - 1): #will give us the number of rings we want to display
            all_rings[task["name"]][ring].setPos(xy[num][1])
    draw_main_screen(tasks)
    win.flip()

    #draw animation of progress bar if applicable
    progress_colors=['red','orangered','orange','gold','yellow']
    if not first_pass:
        start_time = trialClock.getTime()
        t = trialClock.getTime()
        while t<start_time+0.35:
            t = trialClock.getTime()
            if event.getKeys(["escape"]): pickle_and_quit()
        progress_frame.setLineColor('aqua')
        progress_animation.setFillColor(progress_colors[this_task["points"]])
        progress_animation.setSize([points,50])
        progress_animation.setPos([-300+ (points/4), 300])
        progress_animation.setOpacity(1)
        steps=points_to_add/point_intervals
        for step in range(1,steps+1):
            start_time=trialClock.getTime()
            cash_register.play()
            while t<start_time+0.35:
                t = trialClock.getTime()
                progress_animation.setSize([points+(points_to_add*step/steps),50])
                progress_animation.setPos([-300+ ((points+(points_to_add*step/steps))/4), 300])
                draw_main_screen(tasks)
                progress_frame.draw()
                progress_animation.draw()
                progress_fill.draw()
                win.flip()
                if event.getKeys(["escape"]): pickle_and_quit()


        #add points, create normal progress bar
        points+=points_to_add
        progress_frame.setLineColor('white')
        progress_fill.setSize([points,50])
        progress_fill.setPos([-300+ (points/4), 300])
        if progress_fill.size[0]>=1200: #break if progress bar is filled
            progress_frame.draw()
            progress_fill.draw()
            win.flip()
            core.wait(0.75)
            break
        draw_main_screen(tasks)
        win.flip()

    this_task = None
    mouse.getPos()
    while this_task==None:
        if click():
            for task in tasks:
                if all_icons[task["name"]].contains(mouse):
                    this_task = task
                    preferences.record_preference(this_task)
        if event.getKeys(['escape','q']):
            pickle_and_quit()

    print 'task chosen:', this_task["name"]

    #show selection screen and wait 0.5 seconds
    #draw_main_screen(tasks)
    all_icons[this_task["name"]].draw()
    progress_frame.draw()
    progress_fill.draw()
    selection_circle.setPos(all_icons[this_task["name"]].pos)
    selection_circle.draw()
    win.flip()
    start_time = trialClock.getTime()
    while True:
        if event.getKeys(['escape','q']): pickle_and_quit()
        if trialClock.getTime() - start_time > 0.5: break

    if this_task["name"]!='Math':
        all_thresholds[this_task["name"]] = all_thresholds[this_task["name"]] if this_task["name"] in all_thresholds else low_thresh[this_task["name"]]
    else:
        low_thresh_operations.update(all_thresholds[this_task["name"]])
        all_thresholds[this_task["name"]] = low_thresh_operations

    #run game until get a correct answer
    score = None
    while score!=1:
        if this_task["name"]=='Math':
            print all_thresholds['Math'].keys()
            operation = choice(all_thresholds['Math'].keys())
            output = all_games[this_task["name"]].run_game(win, grade, operation, all_thresholds[this_task["name"]][operation])
        else:
            output = all_games[this_task["name"]].run_game(win, grade, all_thresholds[this_task["name"]]) #None, all_sheets[this_task["name"]]['sheet'])

        score = output.get('score', 0) if output else 0
        thesePoints += score*(this_task["points"])*point_intervals

        #first write trial number to output
        all_sheets[this_task["name"]]['sheet'].write(all_sheets[this_task["name"]]['row'], 0, trial_number)

        #next write the output variables
        for col,header in enumerate(all_sheets[this_task["name"]]['headers'][1:-1]):
            all_sheets[this_task["name"]]['sheet'].write(all_sheets[this_task["name"]]['row'],col+1,output[header])

        all_sheets[this_task["name"]]['sheet'].write(all_sheets[this_task["name"]]['row'],len(all_sheets[this_task["name"]]['headers'])-1,VERSION)

        #increment row for output records
        all_sheets[this_task["name"]]['row'] += 1

        #write output for main sheet
        main_output = {'trial_number':trial_number, 'task': this_task["name"], 'level': output['level'],'score':output['score'],'type':'choice','choice_icon_pos':[tup[0] for tup in xy if tup[1][0]==all_icons[this_task["name"]].pos[0] and tup[1][1]==all_icons[this_task["name"]].pos[1]][0]}
        choice_output = {("Task Choice {choice}".format(choice=i+1), "Task Points {choice}".format(choice=i+1), "Task Position {choice}".format(choice=i+1))[j%3]: tasks[i][("name", "points")[j%3]] if j%3!=2 else xy[i][0] for j,i in enumerate(sorted(range(0, number_of_choices)*3))}
        main_output.update(choice_output)
        for col,header in enumerate(all_sheets['Main']['headers']):
            if header=="Task Version":
                all_sheets['Main']['sheet'].write(trial_number, col, VERSION)
            else:
                all_sheets['Main']['sheet'].write(trial_number, col, main_output[header])

        #increment trial number
        trial_number+=1

        #display retry screen if incorrect trial
        if score==0:
            if this_task["name"]=='Spatial':
                track_spatial_errors.append(score)
                if len(track_spatial_errors)>=2:
                    all_thresholds[this_task["name"]] = all_thresholds[this_task["name"]]*1.2
                    track_spatial_errors = []
            mouse.getPos()
            retry_instructions.draw()
            win.flip()
            while True:
                if click():
                    break
                if event.getKeys(keyList=['q', 'escape']):
                    pickle_and_quit()

    if thesePoints!=0:
        points_to_add=thesePoints

    first_pass=False
    save()

#record choice time
all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],0, 'Choice Section')
all_sheets['Task_Times']['sheet'].write(all_sheets['Task_Times']['row'],4, trialClock.getTime()-choice_start)
print 'choice time:', trialClock.getTime()-choice_start
save(complete=True)

#fireworks yay!!
start_time = trialClock.getTime()
applause.play()
if fireworks:
    fireworks.draw()
while start_time + 20 > trialClock.getTime() and fireworks._player.time <= int(fireworks.duration):
    congratulations_text.draw()
    win.flip()
    if event.getKeys(keyList=['q', 'escape']):
        save_and_quit(complete=True)
start_time = trialClock.getTime()
applause.fadeOut(5000)

save_and_quit(complete=True)
