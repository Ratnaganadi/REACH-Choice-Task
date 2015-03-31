from psychopy import visual, core, data, event, logging, gui, sound
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os, random, xlwt, sys
from game_functions import task_function, feedback
from practice import practice_functions

#if you want to leave the mask up after presentation of dots times out
leave_mask_up=True

#touchscreen? if False, uses conventional mouse
touchscreen = True

class Dots_Game(practice_functions):

    def __init__(self, win, conditions):

        #file paths for importing conditions, images and audio
        self.fn = os.path.dirname(__file__)
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'
        self.dotstim_path = 'Images/Stimuli/Dots/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')

        #Initialise components for routine: trial
        self.trialClock=core.Clock()

        #time constrains
        self.timer_limit = 3
        self.t_fixcross = 1.5
        self.t_fixline = 1.5

        #repeat and continue button
        self.repeat=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'black_button.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.cont=visual.ImageStim(win=win, name='continue_button', image= image_path + 'black_button.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #INITIALIZING FIXATION POINT, MASK & BLANK#
        self.fix_point=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.right_mask = visual.ImageStim(win, units=u'pix', image= image_path +'mask.jpg', pos=[230,0],size=[400,600])
        self.blank=visual.TextStim(win, ori=0, text=None)
        self.target = visual.ImageStim(win,image=None,pos=[0,0],size=[400,600])
        self.foil = visual.ImageStim(win,image=None,pos=[0,0],size=[400,600])
        self.target_box = visual.ImageStim(win,image= image_path +'box.png',pos=[0,0],size=[420,620])
        self.foil_box = visual.ImageStim(win,image= image_path +'box.png',pos=[0,0],size=[420,620])

        self.message1 = visual.TextStim(win, units=u'pix', pos=[0,+100],height=28, wrapWidth=700, text='In this game you will see two boxes with dots inside, one on each side of the screen. Touch the box that has more dots.')
        self.message2 = visual.TextStim(win, units=u'pix', pos=[0,-150],height=28, wrapWidth=700, text="Touch anywhere on the screen when you're ready to start.")

        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()

        self.trialList=conditions

        #start feedback
        self.fb=feedback.fb(win)
        self.tf=task_function.task_functions(win)

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0


    def run_practice(self, win, task, grade):
        "Run practice"

        inst_set=[self.practice_cue1,None,None,self.practice_cue3]
        aud_set=[self.practice_aud1,None,None,self.practice_aud3]
        stim_set = [39,30,35,None]
        stim_repeat = stim_set
        var = ''
        score_cond = [None,None,None,None]
        
        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task)

    def run_game(self, win, grade, thisIncrement, var):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement, var)

    def run_trial(self, win, thisIncrement, var):

        #set the index to the current difficulty level for indexing into the conditions file
        for question in range(len(self.trialList)):
            #'self.difficulty' increases in difficulty as numbers increase, thisIncrement increases in difficulty as numbers decrease
            if self.trialList[question]['Difficulty'] == (len(self.trialList)-thisIncrement):
                index = question
                difficulty = self.trialList[index]['Difficulty']
        print 'Difficulty is:', difficulty

        # Ensure iteration does not exceed length of available trials:
        if self.iteration[index] > len(self.trialList[index]['Correct'])-1:
            self.iteration[index] = 0


        #initializing variables
        target_content = self.trialList[index]['Correct'][self.iteration[index]]
        foil_content = self.trialList[index]['Incorrect'][self.iteration[index]]
        target_path = self.dotstim_path + target_content
        foil_path = self.dotstim_path + foil_content

        box_pos = ['left','right']
        shuffle(box_pos)
        target_pos = box_pos[0]
        foil_pos = box_pos[1]
        xpos = {'left': -230, 'right': 230}
        self.mouse.setVisible(0)
        
        for box,img,dots,pos in zip([self.target_box,self.foil_box],[self.target,self.foil],[target_path,foil_path],box_pos):
            img.setImage(dots)
            img.setPos([xpos[pos],0])
            box.setPos([xpos[pos],0])
            box.color = "white"

        #display fixation with repeat, pause & continue button
        task_status = self.tf.fixation_function(win)
        print '*********task_status',task_status
        
        if task_status in ['QUIT','repeat_task']:
            return task_status

        if task_status=='continue_task':
            t=0; self.trialClock.reset()

            t1 =  self.t_fixline
            tf =  self.t_fixline + self.timer_limit
            score = None

            self.target_box.draw()
            self.foil_box.draw()
            win.flip()
            core.wait(t1)

            start_time = self.trialClock.getTime()
            choice_time=0
            thisResp = None
            thisResp_pos = None
            self.mouse.getPos()

            while score==None:
                t = self.trialClock.getTime()
                if t>t1 and t<=tf:
                    self.target_box.draw()
                    self.foil_box.draw()
                    self.target.draw()
                    self.foil.draw()
                    win.flip()

                    while thisResp==None and choice_time<=self.timer_limit:
                        if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
                            if self.target_box.contains(self.mouse): 
                                score,thisResp,thisResp_pos = (1,target_content,target_pos)
                                self.target_box.color = "gold"
                            elif self.foil_box.contains(self.mouse): 
                                score,thisResp,thisResp_pos = (0,foil_content,foil_pos)
                                self.foil_box.color = "gold"
                        if event.getKeys(keyList=['escape']): return 'QUIT'
                        choice_time = self.trialClock.getTime()-start_time

                    
                if t>tf: score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')

            #give feedback
            self.fb.present_fb(win,score,[self.target_box,self.foil_box,self.fix_point,self.target,self.foil])

            #write data
            output = {
                'threshold_var': self.trialList[index]['Ratio'][self.iteration[index]],
                'level': difficulty,
                'score': score,
                'resp_time': choice_time,
                'resp': thisResp,
                'resp_pos': thisResp_pos,
                'target': target_content,
                'target_pos': target_pos,
                }
            
            #update iteration of current difficulty
            if self.iteration[index] == len(self.trialList[index]['Incorrect'])-1: self.iteration[index] = 0
            else: self.iteration[index] += 1

            print output
            return output
