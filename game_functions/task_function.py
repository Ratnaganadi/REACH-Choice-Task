from psychopy import visual, core, data, event, logging, gui, sound
import os

class task_functions:
    def __init__(self, win):
        self.trialClock=core.Clock()
        image_path = 'Images/Tasks/'

        # PRACTICE & FIXATION - fix, pause, repeat and continue button
        self.fixation=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.pause=visual.ImageStim(win=win, name='pause', image= image_path + 'black_button.png', units=u'pix', pos=[280, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.repeat=visual.ImageStim(win=win, name='repeat', image= image_path + 'black_button.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.cont=visual.ImageStim(win=win, name='continue', image= image_path + 'black_button.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()


    # def run_instruction_functions(self, win, task):
    #     "Display the instructions for the game."

    #     instructions = visual.MovieStim(win=win,filename = self.aud_inst_path + task + '_instructions.mp4', size = [1500,850], flipHoriz = True)
    #     audio_inst = sound.Sound(self.aud_inst_path + task + '_instructions.wav')
    #     #display instructions and wait

    #     audio_inst.play()
    #     if event.getKeys(keyList=['escape']): return 'QUIT'
    #     while instructions._player.time <= int(instructions.duration):
    #         instructions.draw()
    #         win.flip()
    #     win.flip()


    def fixation_function(self,win):
        'Fixation cross with pause, play, repeat the whole thing'
        self.trialClock.reset(); t=0

        self.fixation.draw()
        self.repeat.draw()
        self.cont.draw()
        self.pause.draw()
        win.flip()
        # core.wait(1.5)

        start_time=self.trialClock.getTime()
        choice_time=0
        thisResp=None
        pause=False
        self.mouse.getPos()

        while (thisResp==None and choice_time<=1.5) or pause==True:
            if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                if self.repeat.contains(self.mouse): 
                    thisResp='repeat_task'
                    pause=False
                elif self.cont.contains(self.mouse): 
                    thisResp='continue_task'
                    pause=False
                elif self.pause.contains(self.mouse): 
                    thisResp=None
                    pause=True
                    print 'pausing task...'
            if event.getKeys(keyList=['escape']): return 'QUIT'
            choice_time=self.trialClock.getTime()-start_time

        print 'pause',pause
        print 'thisResp', thisResp
        print 'choice_time',choice_time

        if self.trialClock.getTime()-start_time>1.5:
            if thisResp!='repeat_task': thisResp='continue_task'

        if thisResp!=None: return thisResp

