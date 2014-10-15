from __future__ import division
from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, csv, pyglet, tempfile, wave
from os.path import join, isfile
from PIL import Image
import random
from random import choice, shuffle
if __name__ != '__main__': from Feedback import feedback

touchscreen = True

class Reading_Game:

    def __init__(self, win, conditions):
        self.fn = os.path.dirname(__file__)

        #get tempfile
        self.temp_dir = tempfile.gettempdir()

        #create window and stimuli
        self.globalClock = core.Clock()#to keep track of time
        self.trialClock = core.Clock()#to keep track of time

        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="         Let's do some practice.\n\n\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")
        self.message1 = visual.TextStim(win, units=u'pix', pos=[0,+150], height=28, text='In this game you will words on the left and the right side of the screen, then you will hear a spoken word. Touch the word you hear.')
        self.message2 = visual.TextStim(win, units=u'pix', pos=[0,-150],height=28, text="Touch anywhere on the screen when you are ready to start.")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')
        self.reading_inst1 = sound.Sound(aud_inst_path + 'reading_inst1.wav')
        self.reading_inst2 = sound.Sound(aud_inst_path + 'reading_inst2.wav')
        self.reading_inst3 = sound.Sound(aud_inst_path + 'reading_inst3.wav')
        self.general_inst_last = sound.Sound(aud_inst_path + 'general_inst_last.wav')

        #instructions
        self.instructions = visual.MovieStim(win=win,filename = aud_inst_path + 'reading_instructions.mp4', size = [1500,850], flipHoriz = True)
        self.audio_inst = sound.Sound(aud_inst_path + 'reading_instructions.wav')

        #foil & target button, speaker stimuli
        self.fixation = visual.TextStim(win, pos=[0,0],height=45, text='', color='white')
        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image= image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #for 2 buttons
        self.target2b = visual.TextStim(win, pos=[0,0],height=45, text='target2b.')
        self.foil2b = visual.TextStim(win, pos=[0,0],height=45, text='foil2b.')
        self.target_2button=visual.ImageStim(win=win, name='target_2button', image= image_path + 'general_button.png', units=u'pix', pos=[260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil_2button=visual.ImageStim(win, name='foil_2button', image= image_path + 'general_button.png', units=u'pix', pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],

        #for 4 buttons
        self.target4b = visual.TextStim(win, pos=[0,0],height=45, text='target4b.')
        self.foil4b1 = visual.TextStim(win, pos=[0,0],height=45, text='foil4b1.')
        self.foil4b2 = visual.TextStim(win, pos=[0,0],height=45, text='foil4b2.')
        self.foil4b3 = visual.TextStim(win, pos=[0,0],height=45, text='foil4b3.')
        self.target_4button=visual.ImageStim(win=win, name='target_4button', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil_4button1=visual.ImageStim(win, name='foil_4button1', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil_4button2=visual.ImageStim(win, name='foil_4button2', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil_4button3=visual.ImageStim(win, name='foil_4button3', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],

        #speaker
        self.speaker = visual.ImageStim(win=win, name='speaker', image=image_path + '/speaker.png', mask = None, units=u'pix', ori=0, pos=[0,200], size=[115,115])
        self.speaker_playing = visual.ImageStim(win=win, name='speaker',units=u'pix', image=image_path + '/speaker_playing_white.png', mask = None, ori=0, pos=[45,200], size=[220,155])
        #feedback
        self.correct = visual.ImageStim(win=win, name='correct', image=image_path + '/green_check2.png', pos=[0,0], size=[128, 128])
        self.incorrect = visual.ImageStim(win=win, name='incorrect', image=image_path + '/red_x.png', units=u'pix', pos=[0, 0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1)
        self.feedback = [self.incorrect, self.correct]
        #start feedback
        self.fb=feedback.fb(win)

        #initializing scores
        self.scores=[]
        #self.mouse
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()

        self.trialList = conditions
        print 'len(trialList)', len(self.trialList)
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0

    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions.status != visual.FINISHED:
            self.instructions.draw()
            win.flip()
        #wait a second before checking for mouse movement
        core.wait(1)
        self.mouse.getPos()
        #check for a touch
        cont=False
        while cont==False:
            if self.click():
                cont=True
            if 'escape' in event.getKeys():
                core.quit()


    def run_practice(self, win, grade):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,repeat_option, practice_set):
            # self.repeat_button.draw() # self.continue_button.draw()
            if repeat_option=='no_repeat_option':
                text_cue.draw()
                aud_cue.play()
                win.flip() #display instructions

                #wait 1 seconds before checking for touch
                start_time = self.trialClock.getTime()
                while start_time+1 > self.trialClock.getTime():
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

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
                aud_cue.play()
                win.flip() #display instructions

                #wait 1 seconds before checking for touch
                start_time = self.trialClock.getTime()
                while start_time+1 > self.trialClock.getTime():
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    if self.click():
                        if self.repeat_button.contains(self.mouse): #self.mouse.mouseMoved()
                            aud_cue.stop(); return 'repeat'
                            break
                        elif self.continue_button.contains(self.mouse):
                            aud_cue.stop(); return 'continue'
                            break
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'
            print 'with_practice', with_practice

            #run practice trial if with_practice is true
            if with_practice==True: output = self.run_trial(win, stim_condition,practice_set,'practice'); print 'run practice'

        def run_3_practice(inst,audio,stimuli,practice_set):
            #draw practice instructions, and do sub practipractice_setce
            for txt,aud,stim in zip(inst,audio,stimuli):
                run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option',practice_set)
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,2,True,'no_repeat_option',practice_set)
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,3,True,'no_repeat_option',practice_set)

        inst_set=[self.practice_cue1,self.practice_cue2,self.practice_cue2]
        aud_set=[self.practice_aud1,self.practice_aud2,self.practice_aud2]
        stim_set = [4,2,3]

        "!!!Don't forget to put in stim_set based on grade level here when the letter level is ready!!!"

        run_3_practice(inst_set,aud_set,stim_set,'practice_set1')
        run_3_practice(inst_set,aud_set,stim_set,'practice_set2')
        # run_3_practice('practice_set1')
        # run_3_practice('practice_set2')
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt', 'practice_set1')
            if repeat_or_continue=='repeat':
                run_3_practice(inst_set,aud_set,stim_set,'practice_set1')
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
        if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    def run_game(self, win, grade, thisIncrement):
        "Run one iteration of the game without touch"
        return self.run_trial(win, thisIncrement, 'trial_set', 'game')

    def run_trial(self, win, index,practice_set, task_phase):
        "Run one iteration of the game."

        def draw_buttons(time,top,change,string_ls,text_ls,xpositions,button_ls):
            for string,text,xpos,button in zip(string_ls,text_ls,xpositions,button_ls):
                text.setText(string)
                text.setColor('white')
                text.setPos([xpos,-150])
                button.setPos([xpos,-150])
                button.draw()
                text.draw()
            if top=='yes-speaker':
                self.speaker.draw()
            if change=='yes-flip':
                win.flip()
            if time > 0:
                core.wait(time)

        def concat_wavs(infiles, length_between_files):
            data=[]
            for infile in infiles:
                w = wave.open(infile, 'rb')
                data.append( w.readframes(w.getnframes()) )
                if infile != infiles[-1]: data.append( '\x00\x00' * int(w.getframerate()*float(length_between_files)) ) #insert blank space
                w.close()
            outfile = join(self.temp_dir,'temp_stim.wav')
            output = wave.open(outfile, 'w')
            output.setparams(w.getparams())
            for i in range(len(data)):
                output.writeframes(data[i])
            output.close()
            return outfile

        def play_with_psychopy(fn):
            # load stim
            #fn = 'audio_concated/touch_{}.wav'.format(audio)
            audio_stim = sound.Sound(value=fn)

            # get stim length
            wavefile = wave.open(fn, 'r')
            audio_length = wavefile.getnframes()/float(wavefile.getframerate())

            #play stim
            self.speaker_playing.draw()
            win.flip()
            audio_stim.play()

            # wait length of stimulus
            start_time = self.globalClock.getTime()
            while start_time + audio_length > self.globalClock.getTime():
                if event.getKeys(keyList=['escape']): core.quit()

        def play_with_button(audio_fnn,a,b,c,d):
            draw_buttons(0,'no-speaker','no-flip',a,b,c,d)
            play_with_psychopy(audio_fnn)
            draw_buttons(0,'yes-speaker','yes-flip',a,b,c,d)

        def extra_feedback(target):
            "That's right! You touched the word ... That is correct!"
            "That's incorrect. You are supposed to touch the word ... But you touched the wrong one. Let's try some more."

        t = 0; self.trialClock.reset()
        t=self.trialClock.getTime()

        trial_index = len(self.trialList)-index
        for question in range(0,len(self.trialList)):
            #'self.difficulty' increases in difficulty as numbers increase, index increases in difficulty as numbers decrease
            if self.trialList[question]['Difficulty'] == (trial_index):
                n = question
                difficulty = self.trialList[n]['Difficulty']
                grade = self.trialList[n]['Grade']
                print 'Difficulty is:', difficulty, ', Grade:', grade

        c=['look_alike','sound_alike','sound_look_alike','no_sound_look']

        two_xpositions = [-220,220]
        four_xpositions = [-360, -120, 120, 360]
        #putting text and button variables in a list
        text_2b = [self.target2b, self.foil2b]
        text_4b = [self.target4b, self.foil4b1, self.foil4b2, self.foil4b3]
        button_2b = [self.target_2button, self.foil_2button]
        button_4b = [self.target_4button, self.foil_4button1, self.foil_4button2, self.foil_4button3]

        if difficulty <= 3: #for grade k, 1a, 1b
            criteria = str(self.trialList[n]['Criteria'][self.iteration[n]]) # target_header = 'Target_'+criteria; foil_header = 'Foil_'+criteria
            index_value = self.iteration[n] - self.iteration[n]*int(self.iteration[n]/len(self.trialList[n]['Target_'+criteria]))
            self.target_string =  str(self.trialList[n]['Target_'+criteria][index_value])
            self.foil_string = str(self.trialList[n]['Foil_'+criteria][index_value])
            string_2b = [self.target_string, self.foil_string]
            # target_word = self.target_string
            shuffle(two_xpositions)
            twoButton = [self.target_string,string_2b,text_2b,two_xpositions,button_2b]
            B = twoButton
            feedback_screen = [self.speaker] + button_2b + text_2b

        elif difficulty > 3:
            #not done yet!!!
            criteria = ''
            self.target4b_string = str(self.trialList[n]['Target_4button'][self.iteration[n]])
            self.foil4b1_string = str(self.trialList[n]['Foil_look_alike'][self.iteration[n]])
            self.foil4b2_string = str(self.trialList[n]['Foil_sound_alike'][self.iteration[n]])
            foil4b3 = str(self.trialList[n]['Foil_sound_look_alike'][self.iteration[n]])
            foil4b4 = str(self.trialList[n]['Foil_no_sound_look'][self.iteration[n]])
            if foil4b3!='': self.foil4b3_string = foil4b3
            elif foil4b3=='': self.foil4b3_string = foil4b4
            string_4b = [self.target4b_string, self.foil4b1_string, self.foil4b2_string, self.foil4b3_string]

            shuffle(four_xpositions)
            fourButton = [self.target4b_string,string_4b,text_4b,four_xpositions,button_4b]
            B = fourButton
            feedback_screen = [self.speaker] + button_4b + text_4b

            # draw_buttons(1,'no-speaker','yes-flip',string_4b,text_4b,four_xpositions,button_4b)
            # draw_buttons(1.5,'yes-speaker','yes-flip',string_4b,text_4b,four_xpositions,button_4b)

        if task_phase=='instructions':
            play_with_psychopy(self.reading_inst1,'no_drawing')
            draw_buttons(1,'no_speaker','no_flip',B[1],B[2],B[3],B[4])
            play_with_psychopy(self.reading_inst2,'no_drawing')
            draw_buttons(0,'yes_speaker','yes_flip',B[1],B[2],B[3],B[4])

            audio_touchfn = concat_wavs([self.fn+'/wav_files/touch_word.wav'],0.4)
            play_with_button(audio_touchfn,B[1],B[2],B[3],B[4])
            os.remove(audio_touchfn)
            audio_fn = concat_wavs([self.fn+'/wav_files/{}.wav'.format(B[0])],0.2)
            os.remove(audio_fn)

            play_with_psychopy(self.reading_inst3,'no_drawing')
            draw_buttons(0,'yes_speaker','yes_flip',B[1],B[2],B[3],B[4])

            win.flip()
            self.message2.draw()
            self.general_inst_last.play()

            #wait a second before accepting touch
            start_time=self.trialClock.getTime()
            while start_time+1>self.trialClock.getTime():
                if 'escape' in event.getKeys(): return 'QUIT'
            #wait for a touch
            self.mouse.getPos()
            cont=False
            while cont==False:
                if self.click(): cont=True
                if 'escape' in event.getKeys(): return 'QUIT'

        else:
            draw_buttons(1,'no-speaker','yes-flip',B[1],B[2],B[3],B[4]) #string_2b,text_2b,two_xpositions,button_2b)
            draw_buttons(1.5,'yes-speaker','yes-flip',B[1],B[2],B[3],B[4]) #string_2b,text_2b,two_xpositions,button_2b)

            #play audio + buttons
            if practice_set=='practice_set1':
                audio_touchfn = concat_wavs([self.fn+'/wav_files/touch_word.wav'],0.4)
                play_with_button(audio_touchfn,B[1],B[2],B[3],B[4])
                os.remove(audio_touchfn)
                audio_fn = concat_wavs([self.fn+'/wav_files/{}.wav'.format(B[0])],0.2)
                play_with_button(audio_fn,B[1],B[2],B[3],B[4])
            elif (practice_set=='practice_set2') or (practice_set=='trial_set'):
                audio_fn = concat_wavs([self.fn+'/wav_files/{}.wav'.format(B[0])],0.2)
                play_with_button(audio_fn,B[1],B[2],B[3],B[4])

            #start the timer for the response
            start_timer=self.trialClock.getTime()
            timer=0
            score = None
            thisResp = None
            self.mouse.getPos()
            while thisResp == None and timer<15:
                self.mouse_moved=self.mouse.mouseMoved()
                # self.mouse_pos=self.mouse.getPos()
                if difficulty <= 3:
                    if self.mouse_moved and (self.target_2button.contains(self.mouse)):
                        score, thisResp = (1,'correct')
                        self.target2b.setColor('yellow')
                    elif self.mouse_moved and self.foil_2button.contains(self.mouse):
                        score, thisResp = (0,'incorrect')
                        self.foil2b.setColor('yellow')
                elif difficulty > 3:
                    if self.mouse_moved and (self.target_4button.contains(self.mouse)):
                        score, thisResp = (1,'correct')
                        self.target4b.setColor('yellow')
                    elif self.mouse_moved and self.foil_4button1.contains(self.mouse):
                        score, thisResp = (0,'incorrect')
                        self.foil4b1.setColor('yellow')
                    elif self.mouse_moved and self.foil_4button2.contains(self.mouse):
                        score, thisResp = (0,'incorrect')
                        self.foil4b2.setColor('yellow')
                    elif self.mouse_moved and self.foil_4button3.contains(self.mouse):
                        score, thisResp = (0,'incorrect')
                        self.foil4b3.setColor('yellow')
                if self.mouse_moved and self.speaker.contains(self.mouse):
                    play_with_button(audio_fn,B[1],B[2],B[3],B[4])
                if event.getKeys(keyList=['q', 'escape']): return 'QUIT'
                # if event.getKeys(keyList=['escape']): core.quit()
                timer=self.trialClock.getTime()-start_timer

            print ', response:', thisResp

            #calculate response time
            if timer<=15: choice_time=timer
            else: choice_time = 'timed out'

            self.scores.append(score) #store score data on scores=[]

            #give feedback
            self.fb.present_fb(win,score, feedback_screen)#[self.speaker, self.foil_2button, self.foil2b, self.target_2button, self.target2b])

            # if practicing==True:
                # "That's right! You touched the word ... That is correct!"
                # "That's incorrect. You are supposed to touch the word ... But you touched the wrong one. Let's try some more."


            self.fixation.draw()
            win.flip()
            core.wait(1)

        if difficulty <=3:
            output = {'Difficulty':difficulty,'Grade':grade,'Criteria':criteria,'Target_2b':self.target_string,'Foil_2b':self.foil_string,'Target_4b':None,'Foil_4b1':None,'Foil_4b2':None,'Foil_4b3':None,'Foil_4b4':None,'Response':thisResp,'Score':score,'Resp Time':choice_time}
        elif difficulty >3:
            output = {'Difficulty':difficulty,'Grade':grade,'Criteria':criteria,'Target_2b':None,'Foil_2b':None,'Target_4b': self.target4b_string,'Foil_4b1': self.foil4b1_string,'Foil_4b2': self.foil4b2_string,'Foil_4b3': foil4b3,'Foil_4b4': foil4b4, 'Response':thisResp,'Score':score,'Resp Time':choice_time}

        #update iteration of current difficulty
        if difficulty <=3:
            if (self.iteration[n] == len(self.trialList[n]["Criteria"])-1):
                self.iteration[n] = 0
            else:
                self.iteration[n] += 1
                print 'iteration:', self.iteration[n]
        elif difficulty >3:
            if (self.iteration[n] == len(self.trialList[n]['Target_4button'])-1):
                self.iteration[n] = 0
            else:
                self.iteration[n] += 1
                print 'iteration:', self.iteration[n]
        print '*'
        # if self.iteration[#indexNo] == len(self.trialList[#indexNo]['Target_'+criteria])-1: self.iteration[#indexNo] = 0
        # else: self.iteration[#indexNo] += 1

        return output

    #method to get clicks
    def click(self):
        if touchscreen and self.mouse.mouseMoved(): return True
        elif not touchscreen and self.mouse.getPressed()==[1,0,0]: return True
        else: return False

# if __name__=='__main__':
#     sys.path.append(os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
#     from Feedback import feedback

#     win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix') #Window

#     conditions = data.importConditions('stimulus_gradelist_sorted.csv')

#     #initialize game
#     game = Reading_Game(win, conditions)

#     #start feedback
#     fb=feedback.fb(win)

#     #step through staircase to find threshold
#     for i in range(len(conditions)):
#         output = game.run_trial(win,i)
#     for i in range(len(conditions)):
#         for j in range(len(conditions[i]['Difficulty'])):
#             output = game.run_trial(win, i+1)
#     #record the resulting threshold level of the training
