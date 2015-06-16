from psychopy import visual, core, data, event, logging, gui, sound
import os

class task_functions:
    #initialize fixation cross and mouse
    def __init__(self, win):
        self.trialClock=core.Clock()
        image_path = 'Images/Tasks/'
        self.fixation=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()
        self.double_click = False
        self.double_time = None
        self.double_time2 = None
        self.double_time3 = None

    def quit_check(self,win):
        ## QUIT check ##
        #get key inputs
        key = event.getKeys()

        #check for 'QUIT' from the keyboard
        if key==['escape'] or key==['period']*3: return 'QUIT'

        #check for 'QUIT' from the clicker (triple click)
        if self.double_time and not self.double_time2 and self.trialClock.getTime()-self.double_time>=1: self.double_click, self.double_time = False, None
        elif self.double_time2 and not self.double_time3 and self.trialClock.getTime()-self.double_time2>=1: self.double_click, self.double_time, self.double_time2 = False, None, None
        
        if self.double_click==False and key==['period']:
            self.double_click = 'maybe'
            self.double_time = self.trialClock.getTime()
        elif self.double_click=='maybe' and key==['period']:
            self.double_time2 = self.trialClock.getTime()
            if self.double_time2 - self.double_time >1: self.double_click, self.double_time, self.double_time2 = False, None, None
            elif self.double_time2 - self.double_time<=1:self.double_click = 'yes'
        elif self.double_click=='yes' and key==['period']:
            self.double_time3 = self.trialClock.getTime()
            if self.double_time3-self.double_time2>1: self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None
            elif self.double_time3-self.double_time2<=1: 
                return 'QUIT'


    def fixation_function(self,win):
        'Fixation cross with pause, play, repeat the whole thing'

        #initialize variables#
        thisResp=None #denotes if we continue, repeat, or pause the task
        pause=False #pause variable
        # self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None #double click variable

        #initialize clock time
        self.trialClock.reset(); t=0

        #draw fixation cross
        self.fixation.draw()
        win.flip()

        #initialize start time and choice time for click
        start_time=self.trialClock.getTime()
        choice_time=0
        #get mouse position
        self.mouse.getPos()

        #get touch screen response
        #experimenter may pause or abort the whole subtask within 1.5s of the fixation cross
        while (thisResp==None and choice_time<=1.5) or pause==True:
            key = event.getKeys()
            if key==['pagedown'] or key==['right']:
                thisResp='continue_task'
                pause=False
            elif key==['pageup'] or key==['left']:
                thisResp='repeat_task'
                pause=False
            if key==['escape'] or key==['period']*3: return 'QUIT'
            
            #check for triple click
            if self.double_time and not self.double_time2 and self.trialClock.getTime()-self.double_time>=1: 
                self.double_click, self.double_time = False, None
            elif self.double_time2 and not self.double_time3 and self.trialClock.getTime()-self.double_time2>=1: 
                self.double_click, self.double_time, self.double_time2 = False, None, None
            
            #pausing if pressed once, quit if pressed three times
            if self.double_click==False and (key==['period'] or key==['down']):
                thisResp, pause = None, True
                self.double_click = 'maybe'
                self.double_time = self.trialClock.getTime()
            elif self.double_click=='maybe' and key==['period']:
                self.double_time2 = self.trialClock.getTime()
                if self.double_time2 - self.double_time >1: 
                    self.double_click, self.double_time, self.double_time2 = False, None, None
                elif self.double_time2 - self.double_time<=1:
                    self.double_click = 'yes'
            elif self.double_click=='yes' and key==['period']:
                self.double_time3 = self.trialClock.getTime()
                if self.double_time3-self.double_time2>1: 
                    self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None
                elif self.double_time3-self.double_time2<=1:
                    return 'QUIT'
            choice_time=self.trialClock.getTime()-start_time
        
        #if fixation cross is over, then continue to trial
        if self.trialClock.getTime()-start_time>1.5:
            if thisResp!='repeat_task': thisResp='continue_task'

        #return thisResp (continue, repeat, quit) to run_trial method
        if thisResp!=None: return thisResp

