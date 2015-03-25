from psychopy import visual, core, data, event, logging, gui, sound
import os

class practice_functions:

    def run_instructions(self, win, task):
        "Display the instructions for the game."
        aud_inst_path = 'Audio/Instructions/'
        
        instructions = visual.MovieStim(win=win,filename = aud_inst_path + task + '_instructions.mp4', size = [1500,850], flipHoriz = True)
        audio_inst = sound.Sound(aud_inst_path + task + '_instructions.wav')

        #display instructions and wait
        audio_inst.play()
        if event.getKeys(keyList=['escape']): return 'QUIT'
        while instructions._player.time <= int(instructions.duration):
            instructions.draw()
            win.flip()
        win.flip()

    def run_practice_functions(self, win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,score_cond,var):
            if text_cue:
                if option=='repeat_option':
                    self.repeat.draw()
                    self.cont.draw()
                text_cue.draw()
                if aud_cue: aud_cue.play()
                win.flip() #display instructions

                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]): 
                        if aud_cue: aud_cue.stop()
                        if option and option=='repeat_option':
                            if self.repeat.contains(self.mouse): return 'repeat'
                            elif self.cont.contains(self.mouse): return 'continue'
                        # else: cont==True
                        cont=True
                    if 'escape' in event.getKeys(): 
                        if aud_cue: aud_cue.stop()
                        return 'QUIT'
                        # break
            else: win.flip()

            print 'with_practice', with_practice
            if with_practice:
                if self.run_game(win, "", stim_condition,var)=='QUIT': 
                    print 'QUITing practice...'
                    return 'QUIT'
                print 'run practice' #run one practice trial

        def run_3_practice(inst_set,aud_set,score_cond,var):
            #run practice iterations
            for inst, audio, stimuli, cond in zip(inst_set,aud_set,score_cond):
                for txt,aud,stim,score in zip(inst,audio,stimuli,cond):
                    if run_sub_practice(self,win,txt,aud,stim,with_practice=True,'no_repeat_option',score,var)=='QUIT': return 'QUIT'
            # return run_sub_practice(self,win,
                # self.practice_cue3,
            # self.practice_aud3,
            # stim = None,
            # with_practice = False,
            # 'repeat_opt',
            # score = None,
            # var)

        if task!='spatial':
            isntructions=[inst_set]
            audio=[aud_set]
            score_conditions=[score_cond]
        elif task=='spatial'
        
        go_to_choice = False
        while not go_to_choice:
            repeat_check = run_3_practice(instructions,
                # audio,
            # score_conditions,var)
            if repeat_check=='repeat':
                if task=='spatial':
                    instructions = [inst_set[3]]
                    audio = [aud_set[3]]
                    score_conditions = [score_cond[3]]
                print 'repeating practice...'
            elif repeat_check=='continue':
                print 'continue from practice to task...'
                go_to_choice==True
            elif repeat_check=='QUIT': 
                return 'QUIT'
                break


            # if option=='no_repeat_option':
            #     if text_cue!=None:
            #         text_cue.draw()
            #         if aud_cue: aud_cue.play()
            #         win.flip() #display instructions

            #         #wait 1 seconds before checking for touch
            #         start_time = self.trialClock.getTime()
            #         while start_time+1 > self.trialClock.getTime():
            #             if 'escape' in event.getKeys(): return 'QUIT'

            #         #check for a touch
            #         cont=False
            #         self.mouse.getPos()
            #         while cont==False:
            #             if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]): 
            #             	if aud_cue: aud_cue.stop()
            #             	cont=True
            #             if 'escape' in event.getKeys(): 
            #             	if aud_cue: aud_cue.stop()
            #             	return 'QUIT'
            #     else: win.flip()

            # elif option=='repeat_opt':
            #     self.repeat.draw()
            #     self.cont.draw()
            #     text_cue.draw()
            #     aud_cue.play()
            #     win.flip() #display instructions

            #     #wait 1 seconds before checking for touch
            #     start_time = self.trialClock.getTime()
            #     while start_time+1 > self.trialClock.getTime():
            #         if 'escape' in event.getKeys(): aud_cue.stop(); return 'QUIT'

            #     #check for a touch
            #     cont=False
            #     self.mouse.getPos()
            #     while cont==False:
            #         if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
            #             if self.repeat.contains(self.mouse): #self.mouse.mouseMoved()
            #                 if aud_cue: aud_cue.stop()
            #                 return 'repeat'
            #                 break
            #             elif self.cont.contains(self.mouse):
            #                 if aud_cue: aud_cue.stop()
            #                 return 'continue'
            #                 break
            #         if 'escape' in event.getKeys():
            #         	if aud_cue: aud_cue.stop()
            #         	return 'QUIT'

            # print 'with_practice', with_practice
            # if with_practice==True:
            #     output = self.run_game(win, "", stim_condition,var)
            #     print 'run practice' #run first practice trial

            #     if score_cond:
            #         while output['score']!=score_cond:
            #             self.try_again.draw()
            #             win.flip()
            #             #wait a second before accepting touch
            #             start_time=self.trialClock.getTime()
            #             while start_time+1>self.trialClock.getTime():
            #                 if 'escape' in event.getKeys(): return 'QUIT'
            #             #wait for a touch
            #             self.mouse.getPos()
            #             cont=False
            #             while cont==False:
            #                 if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]): cont=True
            #                 if 'escape' in event.getKeys(): return 'QUIT'
            #             output = self.run_game(win, "", stim_condition,var)

        # def run_3_practice(inst,audio,stimuli,score_cond,var):
        #     #draw practice instructions, and do sub practice
        #     for txt,aud,stim,score in zip(inst,audio,stimuli,score_cond):
        #         if run_sub_practice(self,win,txt,aud,stim,True,'no_repeat_option',score,var)=='QUIT': 
        #             return 'QUIT'
        #             break


        # for inst, aud, stim, cond in zip(inst_set,aud_set,score_cond):
        #     if run_3_practice(inst,aud,stim,cond,var)=='QUIT':


        # if var=='star_task':
        #     run_3_practice(inst_set[0],aud_set[0],stim_set[0],score_cond[0],var)
        #     run_3_practice(inst_set[1],aud_set[1],stim_set[1],score_cond[1],var)
        #     run_3_practice(inst_set[2],aud_set[2],stim_set[2],score_cond[2],var)
        # else: run_3_practice(inst_set,aud_set,stim_set,score_cond,var)

        # go_to_choice=False
        # while go_to_choice==False:
        #     repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,False,'repeat_opt',var,score_cond)
        #     if repeat_or_continue=='repeat':
        #         if var=='star_task': run_3_practice(inst_set[3],aud_set[3],stim_repeat,score_cond[3],var)
        #         else: run_3_practice(inst_set,aud_set,stim_repeat,score_cond,var)
        #     elif repeat_or_continue=='continue':
        #         print 'continue2'
        #         go_to_choice=True
        #     if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'
