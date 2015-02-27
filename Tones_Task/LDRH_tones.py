from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, tempfile, wave#,xlwt
from os.path import join, isfile
from math import floor, log
from random import randint, choice, shuffle
from numpy import linspace,sin,pi,int16
from scipy.io.wavfile import write
from game_functions import task_function, feedback
# from game_functions import task_function, practice, feedback
from practice import practice_functions

#touchscreen or not
touchscreen = True

class Tones_Game(practice_functions):

    def __init__(self, win, conditions):
        "Initialize the stimuli and import conditions"
        #get dir for importing resources
        self.fn = os.path.dirname(__file__)
        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'
        #get temp directory
        self.temp_dir = tempfile.gettempdir()
        self.stim_dir = 'Audio/Stimuli/Tones'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')
        
        #repeat and continue button
        self.repeat=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'black_button.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.cont=visual.ImageStim(win=win, name='continue_button', image= image_path + 'black_button.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #create stimuli
        self.speaker = visual.ImageStim(win=win, name='speaker',image=image_path + 'speaker.png', mask = None, units=u'pix',ori=0, pos=[0,200], size=[115,115])
        self.speaker_playing = visual.ImageStim(win=win, name='speaker',units=u'pix',image=image_path + 'speaker_playing_white.png', mask = None,ori=0, pos=[45,200], size=[220,155])
        self.same_button = visual.ImageStim(win, image= image_path + 'happy_button.png', pos=[-260, -200])
        self.different_button = visual.ImageStim(win, image= image_path + 'sad_button.png', pos=[260, -200])
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()
        self.trialClock = core.Clock()

        #time constrains
        self.t_initialspeaker = 1
        self.t_stimgap = 1
        self.timer_limit = 12
        
        #start feedback
        self.fb=feedback.fb(win)
        self.tf=task_function.task_functions(win)

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

    # def run_instructions(self, win, task):
    #     self.tf.run_instruction_functions(win,task)

    def run_practice(self, win, task, grade):
        "Run practice"

        inst_set=[self.practice_cue1,None,None]
        aud_set=[self.practice_aud1,None,None]
        stim_set = [12,15,9] #[2,1,0]
        stim_repeat = [13,16,10] #[5,4,3]
        var = ''
        score_cond = [None,None,None]
        
        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task)


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

    def run_game(self, win, grade, thisIncrement,var):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement, self.trialList, var)

    def run_trial(self, win, thisIncrement, trialList, var):
        "Run one iteration of the game."
        
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

        # check current iteration is not beyond the range of current difficulty trials. Reset if so.
        if self.iteration[index] > len(trialList[index]['soundA'])-1:
            self.iteration[index] = 0


        #load trial variables
        difficulty = self.trialList[index]['Difficulty']
        tones_root = trialList[index]['Root'][self.iteration[index]]
        raw_soundA = eval(trialList[index]['soundA'][self.iteration[index]])
        raw_soundB = eval(trialList[index]['soundB'][self.iteration[index]])
        target_content = trialList[index]['Corr_Answer'][self.iteration[index]]
        contents = ['same','different']
        contents.remove(target_content)
        foil_content = contents[0]

        #######################
        #check history to make sure we don't get more than three identical answers in a row; modify iteration if needed
        #######################
        count=0 #give up after 50 tries
        while len(self.answer_history)>=3 and len(set(self.answer_history[-3:]))==1 and target_content==self.answer_history[-1] and count<50:
            if self.iteration[index] >= len(trialList[index]['soundA'])-1:
                self.iteration[index] = 0
            else:
                self.iteration[index] += 1
            count+=1

        #update answer_history
        self.answer_history.append(target_content)

        #check for and set octave for trial
        print eval(tones_root)[0]
        for num,key in self.tone_key.items():
            if eval(tones_root)[0] == key: root = int(num)
        octave = eval(tones_root)[1]
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

        sounds = [[soundA,raw_soundA],[soundB,raw_soundB]]
        shuffle(sounds)
        stim1 = sounds[0][0]
        stim2 = sounds[1][0]
        raw_stim1 = str(sounds[0][1])
        raw_stim2 = str(sounds[1][1])

        pos = {'same':['left',self.same_button], 'different':['right',self.different_button]}
        target_pos = pos[target_content][0]
        foil_pos = pos[foil_content][0]
        self.target_button = pos[target_content][1]
        self.foil_button = pos[foil_content][1]
        
        #display fixation with repeat, pause & continue button
        task_status = self.tf.fixation_function(win)
        print '*********task_status',task_status
        
        if task_status=='repeat_task':
            return task_status

        elif task_status=='continue_task':
            t=0; self.trialClock.reset()

            #draw speaker
            self.speaker.draw()
            win.flip()
            core.wait(self.t_initialspeaker)    
            self.speaker_playing.draw()
            win.flip()

            #draw first melody
            stim1.play()
            start_time = self.trialClock.getTime()
            while self.trialClock.getTime() < start_time + stim1.getDuration():
                if event.getKeys(keyList=['q', 'escape']): return 'QUIT'

            #after tone is played, wait one second and then play second tone
            self.speaker.draw()
            win.flip()
            core.wait(self.t_initialspeaker)
            self.speaker_playing.draw()
            win.flip()

            #play second melody
            stim2.play()
            start_time = self.trialClock.getTime()
            while self.trialClock.getTime() < start_time + stim2.getDuration():
                if event.getKeys(keyList=['q', 'escape']): return 'QUIT'

            self.speaker.draw()
            self.target_button.draw()
            self.foil_button.draw()
            win.flip()

            #start timer for response
            start_time=self.trialClock.getTime()
            choice_time=0
            thisResp=None
            score = None
            self.mouse.getPos() #called to prevent last movement of mouse from triggering click
            while thisResp==None and choice_time<=self.timer_limit:
                if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                    if self.target_button.contains(self.mouse): score,thisResp,thisResp_pos = (1,target_content,target_pos)
                    elif self.foil_button.contains(self.mouse): score,thisResp,thisResp_pos = (0,foil_content,foil_pos)
                if event.getKeys(keyList=['escape']): return 'QUIT'
                choice_time=self.trialClock.getTime()-start_time

            if t>self.timer_limit: score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')    

            #give feedback
            self.fb.present_fb(win,score,[self.speaker,self.target_button,self.foil_button])

            #write data
            for thresh,lvl in zip(['2tones','3tones','5tones'],[[1,2],[3,6],[7,17]]):
                if difficulty>=lvl[0] and difficulty<=lvl[1]: threshold_var = thresh
            
            output = {
                'threshold_var': threshold_var,
                'level': difficulty,
                'score': score,
                'resp_time': choice_time,
                'stim1': str(raw_stim1),
                'stim2': str(raw_stim2),
                'resp': thisResp,
                'resp_pos': thisResp_pos,
                'target': target_content,
                'target_pos': target_pos,
                'tones_details': trialList[index]['Details'][self.iteration[index]],
                'tones_contour': trialList[index]['Contour'][self.iteration[index]],
                'tones_notes_different': trialList[index]['Notes_Different'][self.iteration[index]],
                'tones_root': str(tones_root)
            }

            output_header = ['tones_details','tones_contour','tones_notes_different']
            stim_header = ['Details','Contour','Notes_Different']
            for out_col,stim_col in zip(output_header,stim_header):
                output.update({out_col:trialList[index][stim_col][self.iteration[index]]})

            #update iteration of current difficulty
            if self.iteration[index] == len(trialList[index]['soundA'])-1:
                self.iteration[index] = 0
            else:
                self.iteration[index] += 1

            return output

    