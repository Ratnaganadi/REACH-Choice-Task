from psychopy import visual, core, data, event, logging, gui, sound
import os

class practice_functions:

    def run_instructions(self, win, task):
        "Display the instructions for the game."
        aud_inst_path = 'Audio/Instructions/'
        
        if task=='choice': sz = [1500,850]
        else: sz = [1250,700]
        instructions = visual.MovieStim(win=win,filename = aud_inst_path + task + '_instructions.mp4', size = sz, flipHoriz = False) #[1500,850]
        audio_inst = sound.Sound(aud_inst_path + task + '_instructions.wav')
        
        #display instructions and wait
        audio_inst.play()
        
        trialClock = core.Clock()
        double_click, double_time, double_time2, double_time3 = False, None, None, None
        while instructions._player.time <= int(instructions.duration):
            key = event.getKeys()
            instructions.draw()
            win.flip()
            if key==['escape']: 
                if audio_inst: audio_inst.stop()
                print 'QUITing {} instructions...'.format(task)
                return 'QUIT'
            
            #check for triple click
            if double_time and trialClock.getTime()-double_time>=1: double_click, double_time = False, None
            elif double_time2 and trialClock.getTime()-double_time2>=1: double_click, doublet_time, double_time2 = False, None, None
            
            if double_click==False and key==['period']:
                double_click = 'maybe'
                double_time = trialClock.getTime()
            elif double_click=='maybe' and key==['period']:
                double_time2 = trialClock.getTime()
                if double_time2 - double_time >1: double_click, double_time, double_time2 = False, None, None
                elif double_time2 - double_time<=1:double_click = 'yes'
            elif double_click=='yes' and key==['period']:
                double_time3 = trialClock.getTime()
                if double_time3-double_time2>1: double_click, double_time, double_time2, double_time3 = False, None, None, None
                elif double_time3-double_time2<=1: return 'QUIT'
        win.flip()

    def run_practice_functions(self, win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task):
        "Run practice"
        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,with_practice,option,score_cond,var):
            if text_cue:
                text_cue.draw()
                if aud_cue: aud_cue.play()
                
                win.flip() #display instructions
                
                #check for a touch
                cont=False
                trialClock = core.Clock()
                double_click, double_time, double_time2, double_time3 = False, None, None, None
                self.mouse.getPos()
                while cont==False:
                    key = event.getKeys()
                    if not option and (key==['pagedown'] or key==['right'] or self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                        if aud_cue: aud_cue.stop()
                        cont = True
                    if option=='after_repeat_option' and (key==['pagedown'] or key==['right'] or self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                        if aud_cue: aud_cue.stop()
                        return 'continue'
                    if option=='repeat_option':
                        if key==['pagedown'] or key==['right']:
                            if aud_cue: aud_cue.stop()
                            return 'cont'
                        elif key==['pageup'] or key==['left']:
                            if aud_cue: aud_cue.stop()
                            return 'repeat'
                    if key==['escape']:
                        if aud_cue: aud_cue.stop()
                        return 'QUIT'
                    
                    #check for triple click
                    if double_time and trialClock.getTime()-double_time>=1: double_click, double_time = False, None
                    elif double_time2 and trialClock.getTime()-double_time2>=1: double_click, doublet_time, double_time2 = False, None, None
                    
                    if double_click==False and key==['period']:
                        double_click = 'maybe'
                        double_time = trialClock.getTime()
                    elif double_click=='maybe' and key==['period']:
                        double_time2 = trialClock.getTime()
                        if double_time2 - double_time >1: double_click, double_time, double_time2 = False, None, None
                        elif double_time2 - double_time<=1:double_click = 'yes'
                    elif double_click=='yes' and key==['period']:
                        double_time3 = trialClock.getTime()
                        if double_time3-double_time2>1: double_click, double_time, double_time2, double_time3 = False, None, None, None
                        elif double_time3-double_time2<=1: return 'QUIT'
                        
            else: win.flip()
            print '**',option, with_practice, stim_condition, var
            if with_practice:
                if self.run_game(win, "", stim_condition,var)=='QUIT': return 'QUIT'
                print 'run practice' #run one practice trial

        def run_3_practice(inst_set,aud_set,stim_set,score_cond,var):
            #run practice iterations
            i=0
            for inst, audio, stims, cond in zip(inst_set,aud_set,stim_set,score_cond):
                v = var
                option = [None]*(len(cond)-2) + ['repeat_option','after_repeat_option']
                if task=='spatial':
                    v = var[i]; i+=1
                    if not v: option = [None]*len(cond)
                
                for txt,aud,stim,score,opt in zip(inst,audio,stims,cond,option):
                    print 'STAR TASK'
                    print 'txt',txt
                    print 'aud',aud
                    print 'stim',stim
                    print 'score',score
                    print 'opt'
                    with_practice = True
                    if opt=='repeat_option' or opt=='after_repeat_option': with_practice = False
                    print '**', opt, with_practice,cond,v
                    test = run_sub_practice(self,win,txt,aud,stim,with_practice,opt,score,v)
                    if test and test!='cont': return test
        
        instructions,audio,stimuli,score_conditions,vars = [inst_set],[aud_set],[stim_set],[score_cond],var
        if task=='spatial': instructions,audio,stimuli,score_conditions = inst_set[:-1],aud_set,stim_set,score_cond
        
        
        practice_cue = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="")
        go_to_choice = False
        while not go_to_choice:
            repeat_check = run_3_practice(instructions,audio,stimuli,score_conditions,vars)
            if repeat_check=='repeat':
                if task=='spatial':
                    instructions,audio,stimuli,score_conditions,vars = [inst_set[-1]],[aud_set[-1]],[stim_set[-1]],[score_cond[-1]], [var[-1]]
                print 'repeating practice...'
            elif repeat_check=='continue':
                print 'continue from practice to task...'
                go_to_choice = True
            elif repeat_check=='QUIT': 
                print 'QUITing practice...'
                return 'QUIT'

