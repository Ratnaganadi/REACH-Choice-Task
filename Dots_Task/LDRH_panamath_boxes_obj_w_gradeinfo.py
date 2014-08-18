from psychopy import visual, core, data, event, logging, gui, sound
import numpy as np 
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os, random, xlwt, sys
if __name__ != '__main__': from feedback import feedback

#if you want to leave the mask up after presentation of dots times out
leave_mask_up=True

#touchscreen? if False, uses conventional mouse
touchscreen = True

class Dots_Game():
    
    def __init__(self, win, conditions):
        
        #get dir for importing conditions, images and audio
        self.fn = os.path.dirname(__file__)

        image_path = 'Images/Tasks/'
        audio_path = 'Audio/'
        dotstim_path = 'Images/Stimuli/Dots'
        
        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="         Let's do some practice.\n\n\n\nTouch anywhere to start practicing.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")
        self.practice_aud1 = sound.Sound('practice_cue1.wav')
        self.practice_aud2 = sound.Sound('practice_cue2.wav')
        self.practice_aud3 = sound.Sound('practice_cue3.wav')
        self.message1 = visual.TextStim(win, units=u'pix', pos=[0,+150], height=28, text='In this game you will words on the left and the right side of the screen, then you will hear a spoken word. Touch the word you hear.')
        self.message2 = visual.TextStim(win, units=u'pix', pos=[0,-150],height=28, text="Touch anywhere on the screen when you are ready to start.")
        
        #Initialise components for routine: trial
        self.trialClock=core.Clock()
        
        self.t_fixcross = 1.5
        self.t_fixline = 1.5
        self.t_stims = 3
        self.t_mask_initial = 1
        self.t_mask_end = 1
        
        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image= image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #INITIALIZING FIXATION POINT, MASK & BLANK#
        self.line = visual.ShapeStim(win, name='line', units=u'pix', lineWidth = 2.0, lineColor = 'white', lineColorSpace='rgb',pos = [0,0], vertices = ((0,-300),(0,0),(0,300)),interpolate = True)
        self.fix_point=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.mask=visual.ImageStim(win, units=u'pix', image= image_path +'/mask.jpg', pos=[0, 0], size=[900, 600], color=[1,1,1])
        self.left_mask = visual.ImageStim(win, units=u'pix', image= image_path +'/mask.jpg', pos=[-230,0],size=[400,600])
        self.right_mask = visual.ImageStim(win, units=u'pix', image= image_path +'/mask.jpg', pos=[230,0],size=[400,600])
        self.blank=visual.TextStim(win, ori=0, text=None)
        self.left = visual.ImageStim(win,image=None,pos=[-230,0],size=[400,600])
        self.right = visual.ImageStim(win,image=None,pos=[230,0],size=[400,600])
        self.left_box = visual.ImageStim(win,image= image_path +'/box.png',pos=[-230,0],size=[420,620])
        self.right_box = visual.ImageStim(win,image= image_path +'/box.png',pos=[230,0],size=[420,620])
        
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
        
        
    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.message1.draw()
        self.message2.draw()
        win.flip()
        #wait a second before checking for mouse movement
        core.wait(1)
        self.mouse.getPos()
        #check for a touch
        cont=False
        while cont==False:
            if self.click(): cont=True
            if 'escape' in event.getKeys(): return 'QUIT'
    
    def run_practice(self, win, grade):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,repeat_option):
            # self.repeat_button.draw() # self.continue_button.draw()
            if repeat_option=='no_repeat_option':
                text_cue.draw()
                # aud_cue.play()
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
            if with_practice==True: output = self.run_game(win, stim_condition); print 'run practice' #run first practice trial

        def run_3_practice(inst,stimuli,score_conds):
            #draw practice instructions, and do sub practice
            for txt,stim,score in zip(inst,stimuli,score_conds):
                run_sub_practice(self,win,txt,self.practice_aud2,stim,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue1,self.practice_aud1,39,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,30,True,'no_repeat_option')
            # run_sub_practice(self,win,self.practice_cue2,self.practice_aud2,35,True,'no_repeat_option')
        
        inst_set=[self.practice_cue1,self.practice_cue2,self.practice_cue2]
        aud_set=[self.practice_aud1,self.practice_aud2,self.practice_aud2]
        stim_set = [39,30,35]

        run_3_practice(inst_set,aud_set,stim_set)
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt')
            if repeat_or_continue=='repeat': run_3_practice()
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

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
        
        #randomize side of stimuli
        incorrect = dotstim_path+self.trialList[index]['Incorrect'][self.iteration[index]]
        correct = dotstim_path+self.trialList[index]['Correct'][self.iteration[index]]
        correct_side = random.choice(['left','right'])
        
        if correct_side=='left':
            self.left.setImage(correct)
            self.right.setImage(incorrect)
        else:
            self.left.setImage(incorrect)
            self.right.setImage(correct)
        
        #draw fixation
        self.fix_point.draw()
        win.flip()
        start_time=self.trialClock.getTime()
        while self.trialClock.getTime()-start_time<(self.t_fixcross):
            if event.getKeys(keyList=['q','escape']): return 'QUIT'
        
        #draw line with fixation
        self.left_box.draw()
        self.right_box.draw()
        #self.fix_point.draw()
        win.flip()
        start_time=self.trialClock.getTime()
        while self.trialClock.getTime()-start_time<(self.t_fixline):
            if event.getKeys(keyList=['q', 'escape']): return 'QUIT'
            
        #draw stims
        #self.fix_point.draw()
        self.left_box.draw()
        self.left.draw()
        self.right_box.draw()
        self.right.draw()
        #self.line.draw()
        win.flip()
        
        #define a function to check for a response
        def check_for_response():
            resp=None
            if self.click():
                if self.right_box.contains(self.mouse): resp = 'right'
                elif self.left_box.contains(self.mouse): resp = 'left'
            return resp
        
        #put stims up for 2 seconds and wait for response
        theseKeys=[]
        start_time=self.trialClock.getTime()
        resp=None
        self.mouse.getPos()
        event.clearEvents()
        while self.trialClock.getTime()-start_time<(self.t_stims) and resp==None:
            resp = check_for_response()
            resp_rt=self.trialClock.getTime()-start_time
            if event.getKeys(keyList=['q', 'escape']): return 'QUIT'
        
        
        if resp==None: resp_rt='timed out'
        score = int(correct_side==resp)
        print score
        
        #reset box opacity
        #self.box.setOpacity(1)
        
        #set pos and opacity of response box
        if resp=='left' and resp_rt!='timed out': self.left_box.color = "gold"
        elif resp=='right'and resp_rt!='timed out': self.right_box.color = "gold"
        #elif resp_rt=='timed out': self.box.setOpacity(0)
        
        #give feedback
        self.fb.present_fb(win,score,[self.left_box,self.right_box,self.fix_point,self.left,self.right])
        
        #reset colors of boxes
        self.left_box.color = "white"
        self.right_box.color = "white"
        
        #write data #self.headers = ['Difficulty','Correct','Incorrect','Ratio','Score','Resp Time','Adaptive']
        output = {'Difficulty': difficulty, 'Correct': self.trialList[index]['Correct'][self.iteration[index]], 'Incorrect': self.trialList[index]['Incorrect'][self.iteration[index]],
            'Ratio': self.trialList[index]['Ratio'][self.iteration[index]], 'Score': score, 'Resp Time': resp_rt}
        
        #update iteration of current difficulty
        if self.iteration[index] == len(self.trialList[index]['Incorrect'])-1: self.iteration[index] = 0
        else: self.iteration[index] += 1
        
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
    from feedback import feedback
    
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