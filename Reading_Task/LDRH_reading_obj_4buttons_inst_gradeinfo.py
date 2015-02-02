from __future__ import division
from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, csv, pyglet, tempfile, wave
from os.path import join, isfile
from PIL import Image
import random
from random import choice, shuffle
from task_function import task_functions
if __name__ != '__main__': from Feedback import feedback

touchscreen = True

class Reading_Game(task_functions):

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
        self.readingstim_path = 'Audio/Stimuli/Reading/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
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

        #for texts
        self.target = visual.TextStim(win, pos=[0,0],height=45, text='target.')
        self.foil1 = visual.TextStim(win, pos=[0,0],height=45, text='foil1.')
        self.foil2 = visual.TextStim(win, pos=[0,0],height=45, text='foil2.')
        self.foil3 = visual.TextStim(win, pos=[0,0],height=45, text='foil3.')

        #for 2 & 4 buttons
        self.target_2button=visual.ImageStim(win=win, name='target_2button', image= image_path + 'general_button.png', units=u'pix', pos=[260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil_2button=visual.ImageStim(win, name='foil_2button', image= image_path + 'general_button.png', units=u'pix', pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.target_4button=visual.ImageStim(win=win, name='target_4button', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil1_4button=visual.ImageStim(win, name='foil1_4button', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil2_4button=visual.ImageStim(win, name='foil2_4button', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],
        self.foil3_4button=visual.ImageStim(win, name='foil3_4button', image=image_path + '/general_button_4.png', units=u'pix')#, pos=[-260, -200], size=[322,100], color=[1,1,1], colorSpace=u'rgb', opacity=1.0) #size=[322,152],

        #speaker
        self.speaker = visual.ImageStim(win=win, name='speaker', image=image_path + '/speaker.png', mask = None, units=u'pix', ori=0, pos=[0,200], size=[115,115])
        self.speaker_playing = visual.ImageStim(win=win, name='speaker',units=u'pix', image=image_path + '/speaker_playing_white.png', mask = None, ori=0, pos=[45,200], size=[220,155])
        #feedback
        self.correct = visual.ImageStim(win=win, name='correct', image=image_path + '/green_check2.png', pos=[0,0], size=[128, 128])
        self.incorrect = visual.ImageStim(win=win, name='incorrect', image=image_path + '/red_x.png', units=u'pix', pos=[0, 0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1)
        self.feedback = [self.incorrect, self.correct]

        #time constrains
        self.t_initialbuttons = 1
        self.t_initialspeaker = 1.5

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


    def run_practice(self, win, grade):
        "Run practice"

        inst_set=[self.practice_cue1,None,None,None,None]
        aud_set=[self.practice_aud1,None,None,None,None]
        stim_set = [10,9,8,6,5]
        stim_repeat = stim_set
        score_cond = [None,None,None]
        var = ['prompt_ltr','prompt_sound','prompt_word','prompt_other','prompt_other']

        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var)


        # def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,prompt_itm):
        #     # self.repeat_button.draw() # self.continue_button.draw()
        #     if option=='no_repeat_option':
        #         if text_cue!=None and aud_cue!=None:
        #             text_cue.draw()
        #             aud_cue.play()
        #             win.flip() #display instructions

        #             #wait 1 seconds before checking for touch
        #             start_time = self.trialClock.getTime()
        #             while start_time+1 > self.trialClock.getTime():
        #                 if 'escape' in event.getKeys(): return 'QUIT'

        #             #check for a touch
        #             cont=False
        #             self.mouse.getPos()
        #             while cont==False:
        #                 if self.click(): aud_cue.stop(); cont=True
        #                 if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'
        #         else: win.flip()

        #     elif option=='repeat_opt':
        #         self.repeat_button.draw()
        #         self.continue_button.draw()
        #         text_cue.draw()
        #         aud_cue.play()
        #         win.flip() #display instructions

        #         #wait 1 seconds before checking for touch
        #         start_time = self.trialClock.getTime()
        #         while start_time+1 > self.trialClock.getTime():
        #             if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

        #         #check for a touch
        #         cont=False
        #         self.mouse.getPos()
        #         while cont==False:
        #             if self.click():
        #                 if self.repeat_button.contains(self.mouse): #self.mouse.mouseMoved()
        #                     aud_cue.stop(); return 'repeat'
        #                     break
        #                 elif self.continue_button.contains(self.mouse):
        #                     aud_cue.stop(); return 'continue'
        #                     break
        #             if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'
        #     print 'with_practice', with_practice

        #     #run practice trial if with_practice is true
        #     if with_practice==True: output = self.run_trial(win, stim_condition,prompt_itm,'practice'); print 'run practice'

        # def run_3_practice(inst,audio,stimuli,prompt_item):
        #     #draw practice instructions, and do sub practice
        #     for txt,aud,stim,prompt_itm in zip(inst,audio,stimuli,prompt_item):
        #         run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option',prompt_itm)

        # inst_set=[self.practice_cue1,None,None,None,None]
        # aud_set=[self.practice_aud1,None,None,None,None]
        # stim_set = [10,9,8,6,5]
        # prompt_item = ['prompt_ltr','prompt_sound','prompt_word','prompt_other','prompt_other']

        # run_3_practice(inst_set,aud_set,stim_set,prompt_item)
        # go_to_choice=False
        # while go_to_choice==False:
        #     repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt', 'prompt_itm1')
        #     if repeat_or_continue=='repeat':
        #         run_3_practice(inst_set,aud_set,stim_set,prompt_item)
        #     elif repeat_or_continue=='continue':
        #         print 'continue2'
        #         go_to_choice=True
        # if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    def run_game(self, win, grade, thisIncrement, var):
        "Run one iteration of the game without touch"
        return self.run_trial(win, thisIncrement, 'trial_set')

    def run_trial(self, win, index, prompt_itm):
        "Run one iteration of the game."

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

        def get_audio(audio_name):
            fn = concat_wavs([self.readingstim_path + '{}.wav'.format(audio_name)],0.3)        
            #load audio
            audio = sound.Sound(value=fn)
            # get stim length
            wavefile = wave.open(fn, 'r')
            audio_length = wavefile.getnframes()/float(wavefile.getframerate())
            return [audio,audio_length]
            os.remove(fn)

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
                grade_now = self.trialList[n]['Grade']
                print 'Difficulty is:', difficulty, ', Grade:', grade

        # c=['look_alike','sound_alike','sound_look_alike','no_sound_look']

        #target & foil properties (positions & string)
        four_xpositions = {-360:'left', -120:'mid-left', 120:'mid-right', 360:'right'}
        two_xpositions = {-260:'left', 260:'right'}
        target_string = str(self.trialList[n]['Target'][self.iteration[n]])
        foil1_string = str(self.trialList[n]['Foil_look_alike'][self.iteration[n]]) #n=0 #don't look alike, sound alike
        foil2_string = str(self.trialList[n]['Foil_sound_alike'][self.iteration[n]]) #n=1 #look_alike, don't sound alike
        foil3_string = str(self.trialList[n]['Foil_sound_look_alike'][self.iteration[n]]) #n=2 #look alike, sound alike
        foil4_string = str(self.trialList[n]['Foil_no_sound_look'][self.iteration[n]]) #n=3 #don't look, don't sound alike

        if foil2_string !='':
            foil_string = [foil1_string,foil2_string]
            if foil3_string!='': foil_string.extend(foil3_string)
            else: foil_string.append(foil4_string)

            foil_text = [self.foil1,self.foil2,self.foil3]
            foil_button = [self.foil1_4button,self.foil2_4button,self.foil3_4button]
            target_button = self.target_4button
            pos = four_xpositions
            xpositions = four_xpositions.keys()

        else:
            foil_string = [foil1_string]
            foil_text = [self.foil1]
            foil_button = [self.foil_2button]
            target_button = self.target_2button
            pos = two_xpositions
            xpositions = two_xpositions.keys()

        points = [1,0,0,0]
        shuffle(xpositions)
        feedback_screen = 
        if grade_now=='letter_sound': object_var = zip(points,['sound_'+target_string.lower()]+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        else: object_var = zip(points,[target_string.lower()]+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        
        #assigning text's string, color and position to target & foil
        for pts,string,text,xpos,button in object_var:
            text.setText(string)
            text.setColor('white')
            text.setPos([xpos,-150])
            button.setPos([xpos,-150])

        #play audio + buttons
        touch_prompt = None
        if prompt_itm=='prompt_ltr'or grade=='letter': touch_prompt='touch_letter'
        elif prompt_itm=='prompt_sound' or grade=='letter_sound': touch_prompt='touch_sound'
        elif prompt_itm=='prompt_word': touch_prompt='touch_word'
        print 'prompt_itm', prompt_itm
        print 'touch_prompt', touch_prompt

        #get audio & audio_length
        audio_prompt = get_audio(touch_prompt)
        audio_stim = get_audio(target_string.lower())
        
        prompt = audio_prompt[0]
        stim = audio_stim[0]
        t_prompt = audio_prompt[1]
        t_stim = audio_stim[1]

        #time constrains
        t1 = self.t_initialbuttons
        t2 = self.t_initialbuttons + self.t_initialspeaker
        t3 = self.t_initialbuttons + self.t_initialspeaker + t_prompt
        t4 = self.t_initialbuttons + self.t_initialspeaker + t_stim

        #the game
        score=None:
        while score==None and touch_prompt!=None:
            t=self.trialClock.getTime()

            if t>=0 and t<=tf:
                for pts,string,text,xpos,button in object_var:
                    button.draw()
                    text.draw()
                if t>t1 and t<=t2: self.speaker.draw()
                if t>t2 and t<=t3:
                    self.speaker_playing.draw()
                    prompt.play()
                if t>t3 and t<=t4:
                    self.speaker_playing.draw()
                    stim.play()
                if t>t4 and t<=tf:
                    self.self.speaker.draw()

                    start_time = self.trialClock.getTime()
                    timer = 0

                    click = self.click()
                    thisResp = None
                    self.mouse.getPos()
                    while thisResp==None:
                        for pts,string,text,xpos,button in object_var:
                            if click and button.contains(self.mouse):
                                score,thisResp,thisResp_pos = (pts,string,pos[xpos])
                                text.setColor('gold')
                        if event.getKeys(keyList=['escape']): return 'QUIT'
                        choice_time = self.trialClock.getTime()-start_time
            if t>tf and t<=tf+1: 
                score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')
                self.fixation.draw()
        
        #give feedback
        self.fb.present_fb(win,score, [self.speaker,feedback_screen)#[self.speaker, self.foil_2button, self.foil1, self.target_2button, self.target])
    
        #write data
        output = {
            'threshold_var': grade,
            'level': difficulty,
            'score': score,
            'resp_time': choice_time,
            'resp': choice_time,
            'resp_pos': thisResp_pos,
            'target': target_string,
            'foil1': foil1_string,
            'foil2': foil2_string,
            'foil3': foil3_string,
            'foil4': foil4_string,
        }

        foil_name = [['foil3_pos',3],['foil4_pos',4]]

        if foil3_string!='': order = [0,1]
        elif foil4_string!='': order = [1,0]

        for i in order:
            output[foil_name[i][0]] = xpositions[foil_name[i][1]

        elif foil4_string!='': output['foil4_pos'] = xpositions[4]
        
        output_header = ['target_pos','foil1_pos','foil2_pos']
        for var,xpos in zip(output_header,xpositions):
            output[var] = string
            output[var+'_pos'] = pos[xpos]

        output = {
        'Difficulty':difficulty,'Grade':grade,'Target':target,'Foil1':foil1,'Foil2':foil2,'Foil3':foil3,'Foil4':foil4,'Response':thisResp,'Score':score,'Resp Time':choice_time}
        
        if (self.iteration[n] == len(self.trialList[n]['Target'])-1): self.iteration[n] = 0
        else: self.iteration[n] += 1
        print 'iteration:', self.iteration[n]
        print '*'

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
