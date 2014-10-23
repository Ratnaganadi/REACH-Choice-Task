from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, tempfile, wave#,xlwt
from os.path import join, isfile
from math import floor, log
from random import randint, choice
from numpy import linspace,sin,pi,int16
from scipy.io.wavfile import write
if __name__ != '__main__': from Feedback import feedback

#touchscreen or not
touchscreen = True

class Tones_Game:

    def __init__(self, win, conditions):
        "Initialize the stimuli and import conditions"
        #get dir for importing resources
        self.fn = os.path.dirname(__file__)
        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="         Let's do some practice.\n\n\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')
        # self.tones_inst1 = sound.Sound(aud_inst_path + 'tones_inst1.wav')
        # self.tones_inst2 = sound.Sound(aud_inst_path + 'tones_inst2.wav')
        # self.tones_inst3 = sound.Sound(aud_inst_path + 'tones_inst3.wav')

        #instructions
        self.instructions = visual.MovieStim(win=win,filename = aud_inst_path + 'music_instructions.mp4', size = [1500,850])
        self.audio_inst = sound.Sound(aud_inst_path + 'music_instructions.wav')

        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image=image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image=image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #create stimuli
        self.speaker = visual.ImageStim(win=win, name='speaker',image=image_path + 'speaker.png', mask = None, units=u'pix',ori=0, pos=[0,200], size=[115,115])
        self.speaker_playing = visual.ImageStim(win=win, name='speaker',units=u'pix',image=image_path + 'speaker_playing_white.png', mask = None,ori=0, pos=[45,200], size=[220,155])
        self.same_button = visual.ImageStim(win, image= image_path + 'happy_button.png', pos=[-260, -200])
        self.different_button = visual.ImageStim(win, image= image_path + 'sad_button.png', pos=[260, -200])

        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()
        self.trialClock = core.Clock()

        #start feedback
        self.fb=feedback.fb(win)

        #create tone dictionary and set values for notes
        self.tone_key = {'1':'C','2':'C#','3':'D','4':'D#','5':'E','6':'F','7':'F#','8':'G','9':'G#','10':'A','11':'A#','12':'B'}
        self.freq_key = dict(C=261.62, Csh=277.18,D=293.66,Dsh=311.13,E=329.63,F=349.23,
            Fsh=369.99,G=392.00,Gsh=415.30,A=440.00,Ash=466.16, B=493.88)
        self.q_int = 0.029302 #quarter note ratio

        #set conditions for trial
        self.trialList=conditions

        #set conditions for practice
        self.practiceList = data.importConditions(join(self.fn, 'practice.xlsx'))

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0

        #list to keep track of history of answers
        self.answer_history = []

        #get temp directory
        self.temp_dir = tempfile.gettempdir()
        self.stim_dir = 'Tones_Task/notes'

    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions._player.time <= int(self.instructions.duration):
            self.instructions.draw()
            win.flip()
        win.flip()

    def run_practice(self, win, grade):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,repeat_option):
            # self.repeat_button.draw() # self.continue_button.draw()
            if repeat_option=='no_repeat_option':
                text_cue.draw()
                aud_cue.play()
                win.flip() #display instructions

                #wait 1 seconds before checking for touch
                start_time = self.trialClock.getTime()
                while start_time+1 > self.trialClock.getTime():
                    if 'escape' in event.getKeys(): return 'QUIT'

                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    if self.click(): aud_cue.stop(); cont=True
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

            elif repeat_option=='repeat_opt':
                self.repeat_button.draw()
                self.continue_button.draw()
                text_cue.draw()
                # aud_cue.play()
                win.flip() #display instructions

                #wait 1 seconds before checking for touch
                start_time = self.trialClock.getTime()
                while start_time+1 > self.trialClock.getTime():
                    if event.getKeys(keyList=['q', 'escape']): return 'QUIT'#if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    print 'repeat_option', event.getKeys()
                    if self.click():
                        if self.repeat_button.contains(self.mouse): #self.mouse.mouseMoved()
                            aud_cue.stop(); return 'repeat'
                            break
                        elif self.continue_button.contains(self.mouse):
                            aud_cue.stop(); return 'continue'
                            break
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

            print 'with_practice', with_practice
            if with_practice==True: output = self.run_trial(win, stim_condition, trialList = self.practiceList); print 'run practice' #run first practice trial

        def run_3_practice(inst,audio,stimuli):
            #draw practice instructions, and do sub practice
            for txt,aud,stim in zip(inst,audio,stimuli):
                run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue1,self.practice_aud1,2,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,1,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,0,True,'no_repeat_option')

        inst_set=[self.practice_cue1,self.practice_cue2,self.practice_cue2]
        aud_set=[self.practice_aud1,self.practice_aud2,self.practice_aud2]
        stim_set = [14,10,7]

        run_3_practice(inst_set,aud_set,stim_set)
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt')
            if repeat_or_continue=='repeat':
                run_3_practice(inst_set,aud_set,stim_set)
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys():
                go_to_choice=True
                return 'QUIT'

    def concat_wavs(self, infiles, outfile):
        data=[]
        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        output = wave.open(outfile, 'w')
        output.setparams(data[0][0])
        for i in range(len(infiles)):
            output.writeframes(data[i][1])
        output.close()

    def run_game(self, win, grade, thisIncrement):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement, trialList=self.trialList)

    def run_trial(self, win, thisIncrement, trialList):
        "Run one iteration of the game."
        self.trialClock.reset(); t=0
        #set the index to the current difficulty level for indexing into the conditions file
        difficulty=None
        for question in range(len(trialList)):
            #'self.difficulty' increases in difficulty as numbers increase, thisIncrement increases in difficulty as numbers decrease
            if trialList[question]['Difficulty'] == (len(trialList)-thisIncrement):
                index = question
                difficulty = trialList[index]['Difficulty']
        if difficulty == None:
            print 'could not find index for', trialList[question]['Difficulty'], 'in', range(len(trialList))
        print 'Difficulty is:', difficulty

        #check history to make sure we don't get more than three identical answers in a row; modify iteration if needed
        count=0 #give up after 50 tries
        while len(self.answer_history)>=3 and len(set(self.answer_history[-3:]))==1 and trialList[index]['Corr_Answer'][self.iteration[index]]==self.answer_history[-1] and count<50:
            if self.iteration[index] == len(trialList[index]['soundA'])-1: self.iteration[index] = 0
            else: self.iteration[index] += 1
            count+=1

        #update answer_history
        self.answer_history.append(trialList[index]['Corr_Answer'][self.iteration[index]])

        #check for and set octave for trial
        print eval(trialList[index]['Root'][self.iteration[index]])[0]
        for num,key in self.tone_key.items():
            if eval(trialList[index]['Root'][self.iteration[index]])[0] == key: root = int(num)
        octave = eval(trialList[index]['Root'][self.iteration[index]])[1]

        raw_soundA = eval(trialList[index]['soundA'][self.iteration[index]])
        raw_soundB = eval(trialList[index]['soundB'][self.iteration[index]])
        print 'soundA is', raw_soundA
        print 'soundB is', raw_soundB

        note_duration=0.35
        note_volume=0.55
        crecendo_duration=0.04
        crecendo_steps=15
        step_size = 1./crecendo_steps

        if 'temp_sound.wav' in os.listdir(os.getcwd()): os.remove(os.getcwd()+os.sep+'temp_sound.wav')

        #create sounds for presentation
        soundA = []
        soundB = []

        A_files = []
        for note in range(len(raw_soundA)):
            note_number = (root - 1) + raw_soundA[note]
            new_octave = octave + floor((note_number-1)/11.6)
            note_name = self.tone_key[str(int(note_number - floor((note_number-1)/11.6)*12))]
            if '.5' in str(note_number): quarter = 'q'
            else: quarter = ''
            note_file = "%s%s%s.wav" %(note_name, str(int(new_octave)), quarter)
            A_files.append(join(self.stim_dir, note_file))
            fn = join(self.temp_dir,'temp_a.wav')
            self.concat_wavs(A_files, fn)
            soundA = sound.Sound(value=fn)
            soundA.setVolume(note_volume)
            os.remove(fn)

        B_files = []
        for note in range(len(raw_soundB)):
            note_number = (root - 1) + raw_soundB[note]
            new_octave = octave + floor((note_number-1)/11.6)
            note_name = self.tone_key[str(int(note_number - floor((note_number-1)/11.6)*12))]
            if '.5' in str(note_number): quarter = 'q'
            else: quarter = ''
            note_file = "%s%s%s.wav" %(note_name, str(int(new_octave)), quarter)
            B_files.append(join(self.stim_dir,note_file))
            fn = join(self.temp_dir,'temp_b.wav')
            self.concat_wavs(B_files, fn)
            soundB = sound.Sound(value=fn)
            soundB.setVolume(note_volume)
            os.remove(fn)

        #draw the center dot
        self.speaker.draw()
        win.flip()

        #play the stimuli
        core.wait(1.0)
        self.speaker_playing.draw()
        win.flip()

        #play first melody
        sounds = [soundA, soundB]
        this_sound = sounds.pop(choice([0,1]))
        this_sound.play()
        start_time = self.trialClock.getTime()
        while self.trialClock.getTime() < start_time + this_sound.getDuration():
            if event.getKeys(keyList=['q', 'escape']): return 'QUIT'

        #after tone is played, wait one second and then play second tone
        self.speaker.draw()
        win.flip()
        core.wait(1.0)
        self.speaker_playing.draw()
        win.flip()

        #play second melody
        this_sound = sounds[0]
        this_sound.play()
        start_time = self.trialClock.getTime()
        while self.trialClock.getTime() < start_time + this_sound.getDuration():
            if event.getKeys(keyList=['q', 'escape']): return 'QUIT'

        #self.same_text.setColor('White')
        #self.different_text.setColor('White')
        #after the second tone has finished, put up the same and different buttons
        self.speaker.draw()
        self.same_button.draw()
        #self.same_text.draw()
        self.different_button.draw()
        #self.different_text.draw()
        win.flip()

        #start timer for response
        start_time=self.trialClock.getTime()
        timer=0

        #wait for response
        thisResp=None
        score = 0
        self.mouse.getPos() #called to prevent last movement of mouse from triggering click
        while thisResp==None and timer<15:
            if self.click():
                if self.same_button.contains(self.mouse):
                    if trialList[index]['Corr_Answer'][self.iteration[index]] == 'same': score, thisResp = (1,'same') #correct answer
                    elif trialList[index]['Corr_Answer'][self.iteration[index]] == 'different': score, thisResp = (0,'same') #incorrect answer
                elif self.different_button.contains(self.mouse):
                    if trialList[index]['Corr_Answer'][self.iteration[index]] == 'same': score, thisResp = (0, 'different') #incorrect answer
                    elif trialList[index]['Corr_Answer'][self.iteration[index]] == 'different': score, thisResp = (1, 'different') #correct answer
            if event.getKeys(keyList=['q', 'escape']):
                return 'QUIT'
            timer=self.trialClock.getTime()-start_time
        #calculate response time
        if timer<=15: choice_time = timer
        else: choice_time = 'timed out'

        #create index for incorrect and correct strings:
        #resp_list = {'same':self.same_text,'different':self.different_text}
        #resp_text= resp_list[thisResp]
        #resp_text.setColor('gold')

        #give feedback
        self.fb.present_fb(win,score,[self.speaker,self.same_button,self.different_button])

        #write data
        #self.headers = ['Difficulty','soundA','soundB','Details','Contour','Notes Different','Root','Response','Correct Response','Score','Resp Time','Adaptive']
        output = {'Difficulty': trialList[index]['Difficulty'], 'soundA': str(raw_soundA), 'soundB': str(raw_soundB), 'Details': trialList[index]['Details'][self.iteration[index]], 'Contour': trialList[index]['Contour'][self.iteration[index]],
            'Notes Different': trialList[index]['Notes_Different'][self.iteration[index]], 'Root': str(trialList[index]['Root'][self.iteration[index]]),'Response': thisResp, 'Correct Response': trialList[index]['Corr_Answer'][self.iteration[index]], 'Score': score,
            'Resp Time': choice_time}

        #update iteration of current difficulty
        if self.iteration[index] == len(trialList[index]['soundA'])-1: self.iteration[index] = 0
        else: self.iteration[index] += 1

        return output

    #method to get clicks
    def click(self):
        if touchscreen and self.mouse.mouseMoved(): return True
        elif not touchscreen and self.mouse.getPressed()==[1,0,0]: return True
        else: return False


if __name__=='__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
    from Feedback import feedback

    #store info about the experiment session
    expName='LDRH Task'; expInfo={'participant':''}
    dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
    if dlg.OK==False: core.quit() #user pressed cancel
    expInfo['date']=data.getDateStr(); expInfo['expName']=expName
    fileName = expInfo['participant'] + expInfo['date']
    #dataFile = open('LDRH spatial data/' + fileName+'.txt', 'w')
    #dataFile.write('Level>Answer\n')

    win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix', fullscr=True) #Window

    #create the staircase handler
    staircase = data.StairHandler(startVal = 10, stepType = 'lin', stepSizes=[2,2,1,1], #reduce step size every two reversals
        minVal=1, maxVal=9, nUp=1, nDown=3,  #will home in on the 80% threshold
        nTrials = 8)

    #create data structure
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Tones')

    #initialize game
#    game = Tones_Game(win)

    #start feedback
    fb=feedback.fb(win)

    #instructions
    game.run_instructions(win)

    #step through staircase to find threshold
    for thisIncrement in staircase:
        output = game.run_game(win, "", thisIncrement)
        staircase.addData(output['Score'])
    #record the resulting threshold level of the training
    thresh = staircase._nextIntensity

    #run one iteration of game at threshold:
    game.run_game(win, "", thresh)