from psychopy import visual, core, data, event, logging, gui, sound
import os

class task_functions:
    
    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions._player.time <= int(self.instructions.duration):
            self.instructions.draw()
            win.flip()
        win.flip()

    def run_practice_functions(self, win, grade, inst_set, aud_set, stim_set, stim_repeat, var):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,var):
            # self.repeat_button.draw() # self.continue_button.draw()
            if option=='no_repeat_option':
                if text_cue!=None and aud_cue!=None:
                    text_cue.draw()
                    aud_cue.play()
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
                else: win.flip()

            elif option=='repeat_opt':
                self.repeat_button.draw()
                self.continue_button.draw()
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
                        if self.repeat_button.contains(self.mouse): #self.mouse.mouseMoved()
                            aud_cue.stop(); return 'repeat'
                            break
                        elif self.continue_button.contains(self.mouse):
                            aud_cue.stop(); return 'continue'
                            break
                    if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

            print 'with_practice', with_practice
            if with_practice==True:
                output = self.run_game(win, "", stim_condition,var)
                print 'run practice' #run first practice trial

        def run_3_practice(inst,audio,stimuli,var):
            #draw practice instructions, and do sub practice
            for txt,aud,stim in zip(inst,audio,stimuli):
                run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option',var)

        run_3_practice(inst_set,aud_set,stim_set,var)
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt')
            if repeat_or_continue=='repeat':
                run_3_practice(inst_set,aud_set,stim_repeat)
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    