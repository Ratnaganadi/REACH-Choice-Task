from psychopy import visual, core, data, event, logging, gui, sound
import os

class practice_functions:

    def run_instructions(self, win, task):
        "Display the instructions for the game."
        aud_inst_path = 'Audio/Instructions/'
        
        instructions = visual.MovieStim(win=win,filename = aud_inst_path + task + '_instructions.mp4', size = [1100, 700], flipHoriz = False) #[1500,850]
        audio_inst = sound.Sound(aud_inst_path + task + '_instructions.wav')

        #display instructions and wait
        audio_inst.play()
        if event.getKeys(keyList=['escape']): return 'QUIT'
        
        while instructions._player.time <= int(instructions.duration):
            key = evet.getKeys()
            instructions.draw()
            win.flip()
            if key and key==['escape']: return 'QUIT'
        win.flip()

    def run_practice_functions(self, win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task):
        "Run practice"
        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,score_cond,var):
            key = evet.getKeys()
            if text_cue:
                if option=='repeat_option':
                    self.repeat.draw()
                    self.cont.draw()
                text_cue.draw()
                if aud_cue: aud_cue.play()
                win.flip() #display instructions
                if key and key==['escape']: return 'QUIT'

                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]): 
                        if aud_cue: aud_cue.stop()
                        if option and option=='repeat_option':
                            if self.repeat.contains(self.mouse): return 'repeat'
                            elif self.cont.contains(self.mouse): return 'continue'
                        cont=True
                    if key and key==['escape']:
                        if aud_cue: aud_cue.stop()
                        return 'QUIT'
            else: win.flip()

            print 'with_practice', with_practice
            if with_practice:
                if self.run_game(win, "", stim_condition,var)=='QUIT': 
                    print 'QUITing practice...'
                    return 'QUIT'
                print 'run practice' #run one practice trial

        def run_3_practice(inst_set,aud_set,stim_set,score_cond,var):
            #run practice iterations
            for inst, audio, stims, cond in zip(inst_set,aud_set,stim_set,score_cond):
                option = [None]*(len(cond)-1) + ['repeat_option']
                for txt,aud,stim,score,opt in zip(inst,audio,stims,cond,option):
                    with_practice = True
                    if option=='repeat_option': with_practice = False
                    test = run_sub_practice(self,win,txt,aud,stim,with_practice,opt,score,var)
                    it test: return test

        if task!='spatial':
            instructions,audio,stimuli,score_conditions = [inst_set],[aud_set],[stim_set],[score_cond]
        elif task=='spatial':
            instructions,audio,stimuli,score_conditions = inst_set,aud_set,stim_set,score_cond

        go_to_choice = False
        while not go_to_choice:
            repeat_check = run_3_practice(instructions,audio,stimuli,score_conditions,var)
            if repeat_check=='repeat':
                if task=='spatial':
                    isntructions,audio,stimuli,score_conditions = [inst_set[3]],[aud_set[2]],[stim_set[2]],[score_cond[2]]
                print 'repeating practice...'
            elif repeat_check=='continue':
                print 'continue from practice to task...'
                go_to_choice = True
            elif repeat_check=='QUIT': 
                return 'QUIT'
                break

