from psychopy import visual, core, data, event, logging, gui, sound
import os

class task_functions:
    def __init__(self, win):
        self.trialClock=core.Clock()
        image_path = 'Images/Tasks/'
        self.aud_inst_path = 'Audio/Instructions/'

        #create practice cue & audio instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        # self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")
        self.practice_instructions1 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 1: administrator demonstrates to child')
        self.practice_instructions2 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 2: administrator walks through trials with child')
        self.practice_instructions3 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 3: child completes trials on his/her own')
        self.practice_instructions4 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text="Let's do some more practice")
        self.try_again = visual.TextStim(win, units='pix', pos=[0,0], height=20, text="Let's try that again.")

        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        # self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')

        #practice instructions for star task
        
        # PRACTICE & FIXATION - fix, pause, repeat and continue button
        self.fixation=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.pause=visual.ImageStim(win=win, name='pause', image= image_path + 'black_button.png', units=u'pix', pos=[280, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.repeat=visual.ImageStim(win=win, name='repeat', image= image_path + 'black_button.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.cont=visual.ImageStim(win=win, name='continue', image= image_path + 'black_button.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()


    def run_instruction_functions(self, win, task):
        "Display the instructions for the game."

        instructions = visual.MovieStim(win=win,filename = self.aud_inst_path + task + '_instructions.mp4', size = [1500,850], flipHoriz = True)
        audio_inst = sound.Sound(self.aud_inst_path + task + '_instructions.wav')
        #display instructions and wait

        audio_inst.play()
        while instructions._player.time <= int(instructions.duration):
            instructions.draw()
            win.flip()
        win.flip()

    def run_practice_functions(self, win, grade, stim_set, stim_repeat, score_cond, var, task):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,score_cond,var):
            # self.repeat.draw() # self.cont.draw()
            if option=='no_repeat_option':
                if text_cue!=None:
                    text_cue.draw()
                    if aud_cue: aud_cue.play()
                    win.flip() #display instructions

                    #wait 1 seconds before checking for touch
                    start_time = self.trialClock.getTime()
                    while start_time+1 > self.trialClock.getTime():
                        if 'escape' in event.getKeys(): return 'QUIT'

                    #check for a touch
                    cont=False
                    self.mouse.getPos()
                    while cont==False:
                        if self.click(): 
                        	if aud_cue: aud_cue.stop()
                        	cont=True
                        if 'escape' in event.getKeys(): 
                        	if aud_cue: aud_cue.stop()
                        	return 'QUIT'
                else: win.flip()

            elif option=='repeat_opt':
                self.repeat.draw()
                self.cont.draw()
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
                        if self.repeat.contains(self.mouse): #self.mouse.mouseMoved()
                            if aud_cue: aud_cue.stop()
                            return 'repeat'
                            break
                        elif self.cont.contains(self.mouse):
                            if aud_cue: aud_cue.stop()
                            return 'continue'
                            break
                    if 'escape' in event.getKeys():
                    	if aud_cue: aud_cue.stop()
                    	return 'QUIT'

            print 'with_practice', with_practice
            if with_practice==True:
                output = self.run_game(win, "", stim_condition,var)
                print 'run practice' #run first practice trial

                if score_cond:
                    while output['score']!=score_cond:
                        self.try_again.draw()
                        win.flip()
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
                        output = self.run_game(win, "", stim_condition,var)

        def run_3_practice(inst,audio,stimuli,score_cond,var):
            #draw practice instructions, and do sub practice
            for txt,aud,stim,score in zip(inst,audio,stimuli,score_cond):
                run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option',score,var)

        if task in ['phonology','math','music','dots']:
            inst_set=[self.practice_cue1,None,None]
            aud_set=[self.practice_aud1,None,None]
        elif task=='reading':
            inst_set=[self.practice_cue1,None,None,None,None]
            aud_set=[self.practice_aud1,None,None,None,None]
        elif task=='spatial':
            inst_set = [[self.practice_instructions1,None,None],[self.practice_instructions2,None],[self.practice_instructions3,None],[self.practice_instructions4,None]]
            aud_set = [[None,None,None],[None,None],[None,None],[None,None]]
        

        if var=='star_task':
            run_3_practice(inst_set[0],aud_set[0],stim_set[0],score_cond[0],var)
            run_3_practice(inst_set[1],aud_set[1],stim_set[1],score_cond[1],var)
            run_3_practice(inst_set[2],aud_set[2],stim_set[2],score_cond[2],var)
        else: run_3_practice(inst_set,aud_set,stim_set,score_cond,var)

        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt',var,score_cond)
            if repeat_or_continue=='repeat':
                if var=='star_task': run_3_practice(inst_set[3],aud_set[3],stim_repeat,score_cond[3],var)
                else: run_3_practice(inst_set,aud_set,stim_repeat,score_cond,var)
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

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
            if event.getKeys(keyList=['escape']): return 'QUIT'
            choice_time=self.trialClock.getTime()-start_time


        if self.trialClock.getTime()-start_time>1.5: thisResp='continue_task'

        if thisResp!=None: return thisResp

