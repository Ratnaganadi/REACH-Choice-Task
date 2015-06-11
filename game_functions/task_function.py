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

    def fixation_function(self,win):
        'Fixation cross with pause, play, repeat the whole thing'

        #initialize variables#
        thisResp=None #denotes if we continue, repeat, or pause the task
        pause=False #pause variable
        double_click, double_time, double_time2, double_time3 = False, None, None, None #double click variable

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
            if double_time and not double_time2 and self.trialClock.getTime()-double_time>=1: 
                double_click, double_time = False, None
#                print 'no click2, double_time reset to False '
            elif double_time2 and not double_time3 and self.trialClock.getTime()-double_time2>=1: 
                double_click, double_time, double_time2 = False, None, None
#                print 'no_click3, double_time reset to False'
            
            #pausing if pressed once, quit if pressed three times
            if double_click==False and (key==['period'] or key==['down']):
                thisResp, pause = None, True
                double_click = 'maybe'
                double_time = self.trialClock.getTime()
#                print 'double_time',double_time,'pausing task...'
            elif double_click=='maybe' and key==['period']:
                double_time2 = self.trialClock.getTime()
                if double_time2 - double_time >1: 
                    double_click, double_time, double_time2 = False, None, None
#                    print 'gap12 too long',double_time2-double_time
                elif double_time2 - double_time<=1:
#                    print 'gap12', double_time2-double_time
                    double_click = 'yes'
            elif double_click=='yes' and key==['period']:
                double_time3 = self.trialClock.getTime()
                if double_time3-double_time2>1: 
                    double_click, double_time, double_time2, double_time3 = False, None, None, None
#                    print 'gap23 too long',double_time3-double_time2
                elif double_time3-double_time2<=1:
#                    print 'gap23',double_time3-double_time2
                    return 'QUIT'
            choice_time=self.trialClock.getTime()-start_time
        
        #if fixation cross is over, then continue to trial
        if self.trialClock.getTime()-start_time>1.5:
            if thisResp!='repeat_task': thisResp='continue_task'

        #return thisResp (continue, repeat, quit) to run_trial method
        if thisResp!=None: return thisResp

