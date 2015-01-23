# -*- coding: utf-8 -*-
from psychopy import core, visual, gui, data, misc, event, sound
import time, numpy, os, sys
from random import shuffle
if __name__ != '__main__': from Feedback import feedback

#touchscreen? if False, uses conventional mouse
touchscreen = True

#white rectangle instead of blue button
white_rectangle = False
#dark button instead of light blue button
dark_button = False

class Math_Game:

    def __init__(self, win, conditions):
        "Initialize the stimuli and iteration numbers, and import conditions"
        #get dir for importing conditions, images and audio
        self.dir = os.path.dirname(__file__)

        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'

        self.math_dotstims_path = 'Images/Stimuli/Math_dotstims/'

        #create practice instructions
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')
        self.math_inst1 = sound.Sound(aud_inst_path + 'math_inst1.wav')
        self.math_inst2 = sound.Sound(aud_inst_path + 'math_inst2.wav')
        self.math_inst3 = sound.Sound(aud_inst_path + 'math_inst3.wav')

        #instructions
        self.instructions = visual.MovieStim(win=win,filename = aud_inst_path + 'math_instructions.mp4', size = [1500,850], flipHoriz = True)
        self.audio_inst = sound.Sound(aud_inst_path + 'math_instructions.wav')

        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image= image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image= image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #create stimuli
        self.text_stimulus = visual.TextStim(win, pos=[0,200],height=80, text='Stimulus.')
        self.dot_stimulus = visual.ImageStim(win,image=None,pos=[0,180],size=[260,260])
        self.fixation = visual.ImageStim(win, color='black', image=None, mask='circle',size=5)
        
        #for texts
        self.target = visual.TextStim(win, pos=[0,0],height=70, text='Target.')
        self.foil1 = visual.TextStim(win, pos=[0,0],height=70, text='Foil1')
        self.foil2 = visual.TextStim(win, pos=[0,0],height=70, text='Foil2')
        self.foil3 = visual.TextStim(win, pos=[0,0],height=70, text='Foil3')
        
        #for 2 & 4 buttons
        self.target_2button = visual.ImageStim(win,image= image_path + '/general_button.png')
        self.foil_2button = visual.ImageStim(win, image= image_path + '/general_button.png')
        self.target_4button = visual.ImageStim(win, image= image_path + '/general_button_4.png')#, size=[300,120])
        self.foil1_4button = visual.ImageStim(win, image= image_path + '/general_button_4.png')#, size=[300,120])
        self.foil2_4button = visual.ImageStim(win, image= image_path + '/general_button_4.png')
        self.foil3_4button = visual.ImageStim(win, image= image_path + '/general_button_4.png')

        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()

        #time constrains
        self.t_timer_limit = 12

        #start feedback
        self.fb=feedback.fb(win)

        self.trialList=conditions
        self.trialClock = core.Clock()

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for operation in ['addition','subtraction','multiplication','division']:
            self.iteration[operation] = {}
            for question in range(len(self.trialList[operation])):
                self.iteration[operation][question] = 0

    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions._player.time <= int(self.instructions.duration):
            self.instructions.draw()
            win.flip()
        win.flip()

    def run_practice(self, win, grade):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,math_operation,stim_condition,with_practice,option):
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
                output = self.run_game(win, "", math_operation, stim_condition)
                print 'run practice' #run first practice trial

        def run_3_practice(inst,audio,stimuli):
            #draw practice instructions, and do sub practice
            for txt,aud,stim in zip(inst,audio,stimuli):
                run_sub_practice(self,win,txt,aud,'addition',stim,True,'no_repeat_option')

        inst_set=[self.practice_cue1,None,None]
        aud_set=[self.practice_aud1,None,None]
        stim_set = [13,11,11]

        run_3_practice(inst_set,aud_set,stim_set)
        # run_3_practice()
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,None,False,'repeat_opt')
            if repeat_or_continue=='repeat':
                run_3_practice(inst_set,aud_set,stim_set)
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    def run_game(self, win, grade, operation, thisIncrement):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, operation, thisIncrement)

    def run_trial(self, win, operation, thisIncrement):
        "Run one iteration of the game."
        self.trialClock.reset()
        these_conditions = self.trialList[operation]
        this_iteration = self.iteration[operation]

        #set the index to the current difficulty level for indexing into the conditions file
        for question in range(len(these_conditions)):
            #'self.difficulty' increases in difficulty as numbers increase, thisIncrement increases in difficulty as numbers decrease
            if these_conditions[question]['Difficulty'] == (len(these_conditions)-thisIncrement):
                index = question
                difficulty = these_conditions[index]['Difficulty']
        print 'Difficulty is:', difficulty

        # Ensure iteration does not exceed length of available trials:
        if this_iteration[index] > len(these_conditions[index]['Stimulus'])-1:
            this_iteration[index] = 0

        #randomize the position of the target and foil
        four_xpositions = {-360:'left', -120:'mid-left', 120:'mid-right', 360:'right'}
        two_xpositions = {-260:'left', 260:'right'}
        target_string = str(these_conditions[index]['Correct'][this_iteration[index]])
        foil1_string = str(these_conditions[index]['Foil1'][this_iteration[index]])
        foil2_string = str(these_conditions[index]['Foil2'][this_iteration[index]])
        foil3_string = str(these_conditions[index]['Foil3'][this_iteration[index]])

        # self.text_2blist = [self.target,self.foil1]
        # self.text_4blist = [self.target,self.foil1,self.foil2,self.foil3]
        # self.button_2blist = [self.target_2button,self.foil_2button]
        # self.button_4blist = [self.target_4button,self.foil1_4button,self.foil2_4button,self.foil3_4button]

        if foil2_string!='' and foil3_string!='':
            foil_string = [foil1_string,foil2_string,foil3_string]
            foil_text = [self.foil1,self.foil2,self.foil3]
            foil_button = [self.foil1_4button,self.foil2_4button,self.foil3_4button]
            target_button = self.target_4button
            pos = four_xpositions
            xpositions = four_xpositions.keys()

        else:
            foil_string = [foil1_string]
            foil_text = [self.foil1]
            foil_button = [self.foil_2button]
            target_button = self.target_2button
            pos = two_xpositions
            xpositions = two_xpositions.keys()

        points = [1,0,0,0]
        shuffle(xpositions)
        object_var = zip(points,[target_string]+foil_string,[self.target]+foil_text,xpositions,[target_button]+foil_button)
        for pts,string,text,xpos,button in object_var:
            text.setText(string)
            test.setColor('white')
            text.setPos([xpos,-200])
            button.setPos([xpos,-200])

        #set the text for the stimuli
        stim_string = these_conditions[index]['Stimulus'][this_iteration[index]]

        #correct division signs if applicable
        if '*div' in stim_string: stim_string= stim_string.replace('*div',u'÷').replace('-',u'−')#stim_string[0:stim_string.index('*div')] + u'÷' + stim_string[stim_string.index('*div')+4:]
        #get image if applicable
        if '.png' in stim_string:
            self.dot_stimulus.setImage(self.math_dotstims_path+stim_string)
            self.stimulus = self.dot_stimulus
        else:
            self.text_stimulus.setText(stim_string)#[self.iteration[index]]))
            self.stimulus=self.text_stimulus

        tf = self.t_timer_limit
        score==None
        start_time = self.trialClock.getTime()
        timer = 0
        thisResp = None
        self.mouse.getPos()

        t = self.trialClock.getTime()
        while score==None:
            if t<=tf:
                self.stimulus.draw()
                self.fixation.draw()

                for text,button in zip([self.target]+foil_text,[target_button]+foil_button):
                    button.draw()
                    text.draw()
                win.flip()
                
                while thisResp==None:
                    for pts,string,text,xpos,button in object_var:
                        if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])) and button.contains(self.mouse):
                            score,thisResp,thisResp_pos = (pts,string,pos[xpos])
                            text.setColor('gold')
                    if event.getKeys(keyList=['escape']): return 'QUIT'
                    choice_time = self.trialClock.getTime()-start_time
            if t>tf: score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')

        #give feedback
        self.fb.present_fb(win,score,[self.stimulus,target_button,self.target]+[foil_button for foil_button in foil_buttons]+[foil for foil in foils]) #[self.foil1_button,self.foil2_button,self.foil3_button,self.target_button,self.foil1,self.foil2, self.foil3,self.target])

        #write data
        output = {
            'threshold_var': operation,
            'level': difficulty,
            'score': score,
            'resp_time': choice_time,
            'stim': stim_string,
            'resp': thisResp,
            'resp_pos': thisResp_pos
        }
        output_header = ['target','foil1','foil2','foil3']
        for var,string,xpos in zip(output_header,[target_string]+foil_string,xpositions):
            output[var] = string
            output[var+'_pos'] = pos[xpos]

        #update iteration of current difficulty
        if this_iteration[index] == len(these_conditions[index]['Correct'])-1: this_iteration[index] = 0
        else: this_iteration[index] += 1

        return output

    def end_game(self):
        "save files and exit game"
        #staircase has ended
#        dataFile.close()
        staircase.saveAsPickle(fileName)#special python binary file to save all the info
        staircase.saveAsExcel(fileName)


        #give some output to user
        #print 'reversals:'
        #staircase.reversalIntensities
        return 'reversals:', staircase.reversalIntensities, 'mean of final 6 reversals = %.3f' %(numpy.average(staircase.reversalIntensities[-6:]))

        #core.quit()

    #method to get clicks
    def click(self):
        if touchscreen and self.mouse.mouseMoved(): return True
        elif not touchscreen and self.mouse.getPressed()==[1,0,0]: return True
        else: return False


if __name__=='__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
    from Feedback import feedback

    win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix') #Window

    conditions = data.importConditions('generated_math_2and4_option_stims_no_zero.xlsx')
    staircase = data.StairHandler(startVal = 20, stepType = 'lin', stepSizes=[3,3,2,2,1,1], #reduce step size every two reversals
        minVal=0, maxVal=len(conditions)-1, nUp=1, nDown=3,  #will home in on the 80% threshold
        nTrials = 10)

    #initialize game
    game = Math_Game(win, conditions)

    #start feedback
    fb=feedback.fb(win)

    #step through staircase to find threshold
    for this_increment in staircase:
        output = game.run_game(win, this_increment)
        staircase.addData(output['Score'])
    #record the resulting threshold level of the training
