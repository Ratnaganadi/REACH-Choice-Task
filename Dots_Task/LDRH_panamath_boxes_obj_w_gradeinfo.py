from psychopy import visual, core, data, event, logging, gui, sound
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os, random, xlwt, sys
from task_function import task_functions
if __name__ != '__main__': from Feedback import feedback

#if you want to leave the mask up after presentation of dots times out
leave_mask_up=True

#touchscreen? if False, uses conventional mouse
touchscreen = True

class Dots_Game(task_functions):

    def __init__(self, win, conditions):

        #get dir for importing conditions, images and audio
        self.fn = os.path.dirname(__file__)

        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'
        self.dotstim_path = 'Images/Stimuli/Dots/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')

        self.dots_inst1 = sound.Sound(aud_inst_path + 'dots_inst1.wav')
        self.dots_inst2 = sound.Sound(aud_inst_path + 'dots_inst2.wav')
        self.dots_inst3 = sound.Sound(aud_inst_path + 'dots_inst3.wav')

        #instructions
        self.instructions = visual.MovieStim(win=win,filename = aud_inst_path + 'dots_instructions.mp4', size = [1500,850], flipHoriz = True)
        self.audio_inst = sound.Sound(aud_inst_path + 'dots_instructions.wav')

        #Initialise components for routine: trial
        self.trialClock=core.Clock()

        #time constrains
        self.timer_limit = 3
        self.t_fixcross = 1.5
        self.t_fixline = 1.5

        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image= image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

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

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0


    # def run_instructions(self, win):
    #     "Display the instructions for the game."
    #     #display instructions and wait
    #     self.audio_inst.play()
    #     while self.instructions._player.time <= int(self.instructions.duration):
    #         self.instructions.draw()
    #         win.flip()
    #     win.flip()

    def run_practice(self, win, grade):
        "Run practice"

        inst_set=[self.practice_cue1,None,None]
        aud_set=[self.practice_aud1,None,None]
        stim_set = [39,30,35]
        stim_repeat = stim_set

        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat)
        # def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option):
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
        #     if with_practice==True:
        #         output = self.run_game(win, "", stim_condition)
        #         print 'run practice' #run first practice trial

        # def run_3_practice(inst,audio,stimuli):
        #     #draw practice instructions, and do sub practice
        #     for txt,aud,stim in zip(inst,audio,stimuli):
        #         run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option')

        # inst_set=[self.practice_cue1,None,None]
        # aud_set=[self.practice_aud1,None,None]
        # stim_set = [39,30,35]

        # run_3_practice(inst_set,aud_set,stim_set)
        # go_to_choice=False
        # while go_to_choice==False:
        #     repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt')
        #     if repeat_or_continue=='repeat':
        #         run_3_practice(inst_set,aud_set,stim_set)
        #     elif repeat_or_continue=='continue':
        #         print 'continue2'
        #         go_to_choice=True
        #     if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    def run_game(self, win, grade, thisIncrement):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement)

    def run_trial(self, win, thisIncrement):

        #Start of routine trial
        t=0; self.trialClock.reset()
        frameN=-1

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

        #randomize side of stimuli
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

        t1 = self.t_fixcross
        t2 = self.t_fixcross + self.t_fixline
        tf = self.t_fixcross + self.t_fixline + self.timer_limit
        score = None
        while t<=t2:
            t = self.trialClock.getTime()
            if t<=t1: self.fix_point.draw()
            if t>t1 and t<=t2:
                self.target_box.draw()
                self.foil_box.draw()
            theseKeys = event.getKeys()
            if len(theseKeys)>0:
                if theseKeys[-1] in ['q','escape']: return 'QUIT'
            win.flip()

        start_time = self.trialClock.getTime()
        timer = 0
        thisResp = None
        self.mouse.getPos()

        while score==None:
            t = self.trialClock.getTime()
            if t>t2 and t<=tf:
                self.target_box.draw()
                self.foil_box.draw()
                self.target.draw()
                self.foil.draw()
                win.flip()

                while thisResp==None:
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

    def end_game(self,n_level,filename):
        #completed (level_now) repeats of 'n_level'

        #get names of stimulus parameters
        if n_level.trialList in ([], [None], None):  params=[]
        else:  params = n_level.trialList[0].keys()
        #save data for this loop
        n_level.saveAsPickle(filename+'n_level')
        n_level.saveAsExcel(filename+'.xlsx', sheetName='n_level',
            stimOut=params,
            dataOut=['n','all_mean','all_std', 'all_raw'])

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

    win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix') #Window

    #create the staircase handler
    staircase = data.StairHandler(startVal = 90, stepType = 'lin', stepSizes=[8,4,2,1], #reduce step size every two reversals
        minVal=0, maxVal=118, nUp=1, nDown=3,  #will home in on the 80% threshold
        nTrials = 8)

    #create data structure
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('Dots')

    #initialize game
    game = Dots_Game(win)

    #start feedback
    fb=feedback.fb(win)

    #step through staircase to find threshold
    for thisIncrement in staircase:
        print 'thisIncrement:', thisIncrement
        output = game.run_game(win, thisIncrement)
        staircase.addData(output['Score'])
    #record the resulting threshold level of the training
    thresh = staircase._nextIntensity

    #run one iteration of game at threshold:
    game.run_game(win, thresh)

    wb.save('Test Data/dots_test_data.xls')