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


        ## initialize trial components ##

        #time components and time constrains for trial
        self.trialClock=core.Clock()
        self.timer_limit = 3
        self.t_fixcross = 1.5
        self.t_fixline = 1.5

        #trial condition
        self.trialList=conditions

        #mouse
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()

        #start feedback
        self.fb=feedback.fb(win)
        self.tf=task_function.task_functions(win)

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0


        ## initialize text, audio & image stimuli ##

        #practice instruction texts
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Touch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Let's do some more.")
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Touch anywhere to begin.")

        #audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')
        
        #fixation point, mask and blank
        self.fix_point=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.right_mask = visual.ImageStim(win, units=u'pix', image= image_path +'mask.jpg', pos=[230,0],size=[400,600])
        self.blank=visual.TextStim(win, ori=0, text=None)
        self.target = visual.ImageStim(win,image=None,pos=[0,0],size=[400,600])
        self.foil = visual.ImageStim(win,image=None,pos=[0,0],size=[400,600])
        self.target_box = visual.ImageStim(win,image= image_path +'box.png',pos=[0,0],size=[420,620])
        self.foil_box = visual.ImageStim(win,image= image_path +'box.png',pos=[0,0],size=[420,620])



    def run_practice(self, win, task, grade):
        "Run practice"
        
        #instruction texts
        inst_set=[self.practice_cue1,None,None,self.practice_cue2, self.practice_cue3]

        #instruction audio
        aud_set=[self.practice_aud1,None,None]+[None]*2#None,None]
        
        #stimuli set for practice
        stim_set = [39,30,35]+[None]*2#,None,None]

        #stimuli for repeated practice (currently the same as the initial stimuli set)
        stim_repeat = stim_set

        #variable, needed for some task's trial
        var = ''

        #score condition, whether we want to constrain trial to be correct or incorrect
        score_cond = [None]*5#,None,None,None,None]
        
        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task)

    def run_game(self, win, grade, thisIncrement, var):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement, var)

    def run_trial(self, win, thisIncrement, var):

        ## get difficulty index ##
        #normally, the difficulty level would be the diff from staircasing -1, because difficulty is ordered in the stimuli file
        try:
            diff = len(self.trialList)-thisIncrement
            index = diff-1

            #double check. if 'difficulty'!=diff, look for matching index for difficulty
            #for each index (=question) in trialList, check if the 'difficulty' value matches the difficulty from staircasing
            #assign index as the 'index' we use if match is found
            if self.trialList[index]['Difficulty']!=diff:
                for question in range(len(self.trialList)):
                    if int(self.trialList[question]['Difficulty']) == (len(self.trialList)-thisIncrement):
                        index = question
        except: 
            print 'ERROR: index set to zero. Could not get index for', thisIncrement, 'in', range(len(self.trialList))
            index = 0

        ## check iteration ##
        #ensure iteration does not exceed length of available trials:
        if self.iteration[index] > len(self.trialList[index]['Correct'])-1:
            self.iteration[index] = 0


        ## get trial variables ## 
        #using index & iteration info above

        #difficulty level
        difficulty = self.trialList[index]['Difficulty']

        #target & foil content, file path
        target_content = self.trialList[index]['Correct'][self.iteration[index]]
        foil_content = self.trialList[index]['Incorrect'][self.iteration[index]]
        target_path = self.dotstim_path + target_content
        foil_path = self.dotstim_path + foil_content
        print 'thisIncrement: {} | Difficulty: {} |'.format(thisIncrement, difficulty),
        # print 'thisIncrement: {} | Difficulty: {} | target: {}, foil: {} |'.format(thisIncrement, difficulty, target_content, foil_content),

        ## prepare stimuli, target & foil ##

        #target & foil position
        box_pos = ['left','right']
        shuffle(box_pos)
        target_pos = box_pos[0]
        foil_pos = box_pos[1]
        xpos = {'left': -230, 'right': 230}
        self.mouse.setVisible(0)
        
        #set appropriate dots image, position and color 
        for box,img,dots,pos in zip([self.target_box,self.foil_box],[self.target,self.foil],[target_path,foil_path],box_pos):
            img.setImage(dots)
            img.setPos([xpos[pos],0])
            box.setPos([xpos[pos],0])
            box.color = "white"


        ## trial ##

        ## fixation ##
        # displayed at the beginning of each trial.
        # here, experimenter has the option to pause the task temporarily, or repeat the whole subtask in special cases

        #check task_status from fixation function
        task_status = self.tf.fixation_function(win)

        #if 'QUIT' or 'repeat' returned, return task status to main choice code
        if task_status in ['QUIT','repeat_task']: return task_status


        ## if 'continue', proceed to trial ## 
        elif task_status=='continue_task':
            
            ## initialize variable ##

            #for output and triple click check
            choice_time, score, thisResp, thisResp_pos = 0, None, None, None
            double_click, double_time, double_time2, double_time3 = False, None, None, None

            #reset trialClock
            self.trialClock.reset()
            
            ## display stimuli, target, foil and trial components ##
            #display boxes for target & foil
            self.target_box.draw()
            self.foil_box.draw()
            win.flip()

            #wait for 1.5s / t1
            core.wait(self.t_fixline)

            #display boxes with target and foil dots pictures
            self.target_box.draw()
            self.foil_box.draw()
            self.target.draw()
            self.foil.draw()
            win.flip()
            

            ## check response ##

            #start timer for response
            start_time=self.trialClock.getTime()
            self.mouse.getPos()

            while score==None:

                ## QUIT check ##
                if self.tf.quit_check(win)=='QUIT': return 'QUIT'

                #check for response when time is within time limit
                while choice_time<=self.timer_limit:
                    if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
                        if self.target_box.contains(self.mouse): 
                            score,thisResp,thisResp_pos = (1,target_content,target_pos)
                            self.target_box.color = "gold"
                        elif self.foil_box.contains(self.mouse): 
                            score,thisResp,thisResp_pos = (0,foil_content,foil_pos)
                            self.foil_box.color = "gold"
                    
                    #calculate reaction time
                    choice_time = self.trialClock.getTime()-start_time
                
                ## time out ##
                #if participant does not respond by time limit  
                if self.trialClock.getTime()-start_time>self.timer_limit:
                    score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')
                    print 'TIME OUT |',


            ## feedback ##
            self.fb.present_fb(win,score,[self.target_box,self.foil_box,self.fix_point,self.target,self.foil])


            ## data output dictionary ##
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
            

            ## update iteration of current difficulty ##
            if self.iteration[index] == len(self.trialList[index]['Incorrect'])-1:
                self.iteration[index] = 0
            else:
                self.iteration[index] += 1

            return output
