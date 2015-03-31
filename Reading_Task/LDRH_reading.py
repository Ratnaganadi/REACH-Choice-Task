from __future__ import division
from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, csv, pyglet, tempfile, wave
from os.path import join, isfile
from PIL import Image
import random
from random import choice, shuffle
from game_functions import task_function, feedback
# from game_functions import task_function, practice, feedback
from practice import practice_functions

touchscreen = True

class Reading_Game(practice_functions):

    def __init__(self, win, conditions):
        
        #file paths for importing conditions, images and audio
        self.fn = os.path.dirname(__file__)
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'
        self.readingstim_path = 'Audio/Stimuli/Reading/'
        self.temp_dir = tempfile.gettempdir()

        #create window and stimuli
        self.globalClock = core.Clock()#to keep track of time
        self.trialClock = core.Clock()#to keep track of time

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')

        #foil & target button, speaker stimuli
        self.fixation = visual.TextStim(win, pos=[0,0],height=45, text='', color='white')
        #repeat and continue button
        self.repeat=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'black_button.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.cont=visual.ImageStim(win=win, name='continue_button', image= image_path + 'black_button.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

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
        self.timer_limit = 12

        #start feedback
        self.fb=feedback.fb(win)
        self.tf=task_function.task_functions(win)

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


    def run_practice(self, win, task, grade):
        "Run practice"

        inst_set=[self.practice_cue1,None,None,None,None,self.practice_cue3]
        aud_set=[self.practice_aud1,None,None,None,None,self.practice_aud3]
        stim_set = [10,9,8,6,5,None]
        stim_repeat = stim_set
        score_cond = [None,None,None,None,None,None]
        var = ['prompt_ltr','prompt_sound','prompt_word','prompt_other','prompt_other']

        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task)


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


        trial_index = len(self.trialList)-index
        for question in range(0,len(self.trialList)):
            #'self.difficulty' increases in difficulty as numbers increase, index increases in difficulty as numbers decrease
            if self.trialList[question]['Difficulty'] == (trial_index):
                n = question
                difficulty = self.trialList[n]['Difficulty']
                grade_now = self.trialList[n]['Grade']
                print 'Difficulty is:', difficulty, ', Grade:', grade_now


        #target & foil properties (positions & string)
        four_xpositions = {-360:'left', -120:'mid-left', 120:'mid-right', 360:'right'}
        two_xpositions = {-260:'left', 260:'right'}
        target_string = str(self.trialList[n]['Target'][self.iteration[n]])
        foil1_string = str(self.trialList[n]['Foil_look_alike'][self.iteration[n]]) #n=0 #don't look alike, sound alike
        foil2_string = str(self.trialList[n]['Foil_sound_alike'][self.iteration[n]]) #n=1 #look_alike, don't sound alike
        foil3_string = str(self.trialList[n]['Foil_sound_look_alike'][self.iteration[n]]) #n=2 #look alike, sound alike
        foil4_string = str(self.trialList[n]['Foil_no_sound_look'][self.iteration[n]]) #n=3 #don't look, don't sound alike

        total_foil=0
        for foil in [foil1_string,foil2_string,foil3_string,foil4_string]:
            if len(foil)>0: len_foil=1
            else: len_foil=len(foil)
            total_foil+=len_foil

        if total_foil==1:
            for foiltmp in [foil1_string,foil2_string,foil3_string,foil4_string]:
                if len(foiltmp)!=0: foil_string = [foiltmp]
            foil_text = [self.foil1]
            foil_button = [self.foil_2button]
            target_button = self.target_2button
            pos = two_xpositions
            xpositions = two_xpositions.keys()

        elif total_foil==3:
            for foiltmp in [foil3_string,foil4_string]:
                if len(foiltmp)!=0: foil_string = [foil1_string,foil2_string,foiltmp]
            foil_text = [self.foil1,self.foil2,self.foil3]
            foil_button = [self.foil1_4button,self.foil2_4button,self.foil3_4button]
            target_button = self.target_4button
            pos = four_xpositions
            xpositions = four_xpositions.keys()

        points = [1,0,0,0]
        shuffle(xpositions)
        feedback_screen = [self.speaker,target_button] + foil_button + [self.target] + foil_text
        # if grade_now=='lettersound': object_var = zip(points,['target_string']+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        # else: object_var = zip(points,[target_string]+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        object_var = zip(points,[target_string]+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        
        #assigning text's string, color and position to target & foil
        for pts,string,text,xpos,button in object_var:
            text.setText(string)
            text.setColor('white')
            text.setPos([xpos,-150])
            button.setPos([xpos,-150])

        #play audio + buttons
        touch_prompt = None
        if prompt_itm=='prompt_ltr'or grade_now=='letter': touch_prompt='touch_letter'
        elif prompt_itm=='prompt_sound' or grade_now=='lettersound': touch_prompt='touch_sound'
        elif prompt_itm=='prompt_word' or grade_now=='k': touch_prompt='touch_word'
        else: touch_prompt=None

        print 'prompt_itm', prompt_itm
        print 'touch_prompt', touch_prompt

        #get audio & audio_length
        if grade_now=='lettersound': audio_stim = get_audio('sound_'+target_string.lower())
        else: audio_stim = get_audio(target_string.lower())
        if touch_prompt!=None: 
            audio_prompt = get_audio(touch_prompt)
            aud_list=[audio_prompt,audio_stim]
        elif touch_prompt==None:
            aud_list=[audio_stim]


        def draw_buttons(object_var,top,flip,time,audio):
            for pts,string,text,xpos,button in object_var:
                button.draw()
                text.draw()
            if top!=None: top.draw()
            if flip=='yes-flip': win.flip()
            # if time>0: core.wait(time)
            core.wait(time)
            if event.getKeys(keyList=['escape']): return 'QUIT'

            for aud in audio:
                aud[0].play()
                start_time = self.trialClock.getTime()
                while self.trialClock.getTime() < start_time + aud[1]:
                    if event.getKeys(keyList=['escape']): return 'QUIT'

        #display fixation with repeat, pause & continue button
        task_status = self.tf.fixation_function(win)
        print '*********task_status',task_status
        
        if task_status in ['QUIT','repeat_task']:
            return task_status

        elif task_status=='continue_task':
            t=0; self.trialClock.reset()

            draw_buttons(object_var,None,'yes-flip',self.t_initialbuttons,[])
            draw_buttons(object_var,self.speaker,'yes-flip',self.t_initialspeaker,[])
            draw_buttons(object_var,self.speaker_playing,'yes-flip',0,aud_list)
            draw_buttons(object_var,self.speaker,'yes-flip',0,[])

            #start timer for response
            start_time=self.trialClock.getTime()
            choice_time=0
            thisResp=None
            thisResp_pos=None
            score = None
            self.mouse.getPos()

            while thisResp==None and choice_time<=self.timer_limit:
                if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                    for pts,string,text,xpos,button in object_var:
                        if button.contains(self.mouse):
                            score,thisResp,thisResp_pos = (pts,string,pos[xpos])
                            text.setColor('gold')
                    if self.speaker.contains(self.mouse):
                        draw_buttons(object_var,self.speaker_playing,'yes-flip',0,[audio_stim])
                if event.getKeys(keyList=['escape']): return 'QUIT'
                choice_time = self.trialClock.getTime()-start_time
            if t>self.timer_limit: score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')

            
            #give feedback
            self.fb.present_fb(win,score, [self.speaker]+feedback_screen)#[self.speaker, self.foil_2button, self.foil1, self.target_2button, self.target])
        
            #write data
            output = {
                'threshold_var': grade_now,
                'level': difficulty,
                'score': score,
                'resp_time': choice_time,
                'resp': choice_time,
                'resp_pos': thisResp_pos,
                'target': target_string,
                'target_pos':pos[xpositions[0]],
                'foil1': foil1_string,
                'foil2': foil2_string,
                'foil3': foil3_string,
                'foil4': foil4_string,
            }
            
            i=1
            for name,foiltmp in zip(['foil1_pos','foil2_pos','foil3_pos','foil4_pos'],[foil1_string,foil2_string,foil3_string,foil4_string]):
                if foiltmp!='':
                    output[name] = pos[xpositions[i]]
                    if total_foil==3: i+=1
                elif foiltmp=='': output[name] = ''

            if (self.iteration[n] == len(self.trialList[n]['Target'])-1): self.iteration[n] = 0
            else: self.iteration[n] += 1
            print 'iteration:', self.iteration[n]
            print '*'

            return output
