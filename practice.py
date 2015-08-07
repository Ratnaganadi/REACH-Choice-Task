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

        def run_comp_check(task):
            #phonology or music
            # check if they know same/different correspond to which button
            # then if syllables/tones are the same or different > then which button

            #image path
            image_path = 'Images/Tasks/'
            aud_prac_path = 'Audio/practice/{}_'.format(task)
            #mouse
            self.mouse = event.Mouse(win=win)
            self.mouse.getPos()
            #clock
            self.trialClock = core.Clock()

            #text stimuli
            q_stim_same = visual.TextStim(win, name='same', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'If the stimuli are EXACTLY THE SAME like this...')
            q_stim_different = visual.TextStim(win, name='different', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'If the stimuli are NOT EXACTLY THE SAME like this...')
            q_which_button = visual.TextStim(win, name='q_touch', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'which of these button do you touch?')
            q_same = visual.TextStim(win, name='q_same', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'If the stimuli are EXACTLY THE SAME, which button do you touch?')
            ans_happy_correct = visual.TextStim(win, name='ans_happy_correct', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'That is correct. If the made up words are EXACTLY THE SAME, touch the HAPPY FACE button.')
            ans_happy_incorrect = visual.TextStim(win, name='ans_happy_incorrect', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'That is not correct. If the made words are EXACTLY THE SAME, touch the HAPPY FACE button, not the sad face button.')
            q_different = visual.TextStim(win, name='q_different', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'If the stimuli are NOT EXACTLY THE SAME, which button do you touch?')
            ans_sad_correct = visual.TextStim(win, name='ans_sad_correct', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'That is correct. If the made up words are NOT EXACTLY THE SAME, touch the SAD FACE button.')
            ans_sad_incorrect = visual.TextStim(win, name='ans_sad_incorrect', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'That is not correct. If the made words are NOT EXACTLY THE SAME, touch the SAD FACE button, not the happy face button.')
            
            #image stimuli
            happy_button = visual.ImageStim(win, name='happy', image=image_path + '/happy_button.png', pos=[-260, -200], size=[200,200])
            sad_button = visual.ImageStim(win, name='sad', image=image_path + '/sad_button.png', pos=[260, -200],size=[200,200])
            check = visual.ImageStim(win=win, name='green_check', units=u'pix', image=image_path + '/green_check2.png', mask=None, ori=0, pos=[0,0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1, texRes=128, interpolate=True, depth=-4.0)
            cross = visual.ImageStim(win=win, name='red_x', units=u'pix', image=image_path + '/red_x.png', mask=None, ori=0, pos=[0, 0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1, texRes=128, interpolate=True, depth=-4.0)

            #dictionaries
            stimlist = {'phonology': 'made up words','music': 'melodies'}

            anslist = {
                'happy': {'correct': ans_happy_correct, 'incorrect': ans_happy_incorrect},
                'sad': {'correct': ans_sad_correct, 'incorrect': ans_sad_incorrect}
                }

            # def draw_play_phonemes(audio,wait_time):
            #     # This function draw stimuli screen, play audio file 
            #     # and make sure audio plays until the end before the next audio files play

            #     #draw initial speaker before phoneme plays
            #     self.speaker.draw()
            #     win.flip()
            #     core.wait(wait_time)
            #     self.speaker_playing.draw()
            #     win.flip()
                
            #     #play phoneme
            #     audio.play()

            #     #make sure the audio plays until the end of audio duration while checking for 'QUIT'
            #     start_time = self.trialClock.getTime()
            #     # double_click, double_time, double_time2, double_time3 = False, None, None, None
            #     while self.trialClock.getTime() < start_time + audio.getDuration():
            #         if self.tf.quit_check(win)=='QUIT': return 'QUIT'            


            def ask_question1(q,task):
                #change 'stimuli' to specific 'stimuli type' for question text
                qtext = str(q.text).replace('stimuli',stimlist[task])
                q.setText(qtext)
                happy_button.setSize([210,210])
                sad_button.setSize([210,210])

                #draw question and buttons
                q.draw()
                happy_button.draw()
                sad_button.draw()
                win.flip()

                #get response
                thisResp, text, button_correct, button_incorrect, change_button, check_pos, cross_pos = None, None, None, None, None, None, None
                while text==None:
                    ## QUIT check ##
                    if self.tf.quit_check(win)=='QUIT': return 'QUIT'

                    if str(q.text)==str(q_same.text): button_correct, button_incorrect, check_pos,cross_pos = happy_button, sad_button, [-260,0], [260,0]
                    elif str(q.text)==str(q_different.text): button_correct, button_incorrect, check_pos,cross_pos = sad_button, happy_button, [260,0], [-260,0]

                    if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                        if button_correct.contains(self.mouse): thisResp = 'correct'; button_correct.setSize([250,250])
                        elif button_incorrect.contains(self.mouse): thisResp = 'incorrect'
                    
                    if button_correct or check or cross:
                        check.setPos(check_pos)
                        cross.setPos(cross_pos)
                        if thisResp: text = anslist[str(button_correct.name)][thisResp]
                

                if thisResp=='correct':
                    check.draw()
                    time_limit = 3.5
                elif thisResp=='incorrect':
                    time_limit = 5
                    cross.draw()

                text.draw()
                happy_button.draw()
                sad_button.draw()
                
                win.flip()

                start_time = self.trialClock.getTime()
                while self.trialClock.getTime() <= start_time + time_limit:
                    ## QUIT check ##
                    if self.tf.quit_check(win)=='QUIT': return 'QUIT'

                    if self.trialClock.getTime()>= start_time+2 and thisResp=='incorrect':
                        button_correct.setSize([250,250])
                        check.draw()

                        text.draw()
                        happy_button.draw()
                        sad_button.draw()

                        win.flip()

                    
                win.flip()
                core.wait(1)

                return thisResp

            # def ask_question2(q_stim,task):

            #     #prepare stimuli to play
            #     same_dif = str(q_stim.name)
            #     stim1 = sound.Sound(audio_prac_path + same_dif + '1.wav')
            #     stim2 = sound.Sound(audio_prac_path + same_dif + '2.wav')

            #     #fix question text
            #     qtext = str(q.text).replace('stimuli',stimlist[task])
            #     q.setText(qtext)

            #     #draw stimuli
            #     q_stim.draw()
            #     win.flip()

            #     #wait for 0.5s
            #     start_time = self.trialClock.getTime()
            #     while self.trialClock.getTime() <= start_time + 0.5:
            #         if self.tf.quit_check(win)=='QUIT': return 'QUIT'

            #     #play stimuli
            #     while thisResp==None:
            #         ## QUIT check ##
            #         if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                    
            #         ## display stimuli, target, foil and trial components##
            #         #display appropriate images in appropriate order for the task
            #         for stim in [stim[same_dif][0],stim[same_dif][1]]:
            #             if draw_play_phonemes(stim,1)=='QUIT': return 'QUIT'

            #         thisResp = ask_question1(q_which_button, task)

            #     return thisResp


            # ans1, ans2 = None, None
            for question in [q_same,q_different]:
                ans1=None
                print question.text
                while ans1!='correct':
                    ans1 = ask_question1(question,task)
                    print 'ans',ans1
                    if ans1=='QUIT': return 'QUIT'

            # for questions in [q_stim_same,q_stim_dif]:
            #     while ans2!='correct': 
            #         ans2 = ask_question2(questions,task)
            #         if ans2=='QUIT': return 'QUIT'


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
                output_streak = self.run_game(win, "", stim_condition,var)
                print 'run practice' #run one practice trial
                if output_streak=='QUIT': return 'QUIT'
                elif output_streak: return output_streak['score']


        def run_3_practice(inst_set,aud_set,stim_set,score_cond,var):
            #run practice iterations
            output_streak = []
            i=0
            for inst, audio, stims, cond in zip(inst_set,aud_set,stim_set,score_cond):
                v = var
                option = [None]*(len(cond)-2) + ['repeat_option','after_repeat_option']
                if task=='spatial':
                    v = var[i]; i+=1
                    if not v: option = [None]*len(cond)
                
                for txt,aud,stim,score,opt in zip(inst,audio,stims,cond,option):
                    with_practice = True
                    if opt=='repeat_option' or opt=='after_repeat_option': with_practice = False
                    print '**', opt, with_practice,cond,v
                    test = run_sub_practice(self,win,txt,aud,stim,with_practice,opt,score,v)
                    if test:
                        if isinstance(test,int) or len(test)==1: output_streak.append(float(test))
                        elif len(test)>1 and test!='cont': return test
                success_rate = float(sum(output_streak)/len(output_streak))
                if success_rate<0.8 and task in ['phonology','music']:
                    if run_comp_check(task)=='QUIT': return 'QUIT'
        
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

