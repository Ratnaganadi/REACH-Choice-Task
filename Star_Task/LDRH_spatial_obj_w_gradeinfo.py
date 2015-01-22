from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui, sound
from random import shuffle, choice
import numpy as np
from numpy.random import random, randint, normal, shuffle
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
import time, os, sys, math, random#, xlwt
if __name__ != '__main__': from Feedback import feedback

touchscreen = True

class Star_Game():

    def __init__(self, win):
        self.fn = os.path.dirname(__file__)
        self.trialClock=core.Clock()

        #file paths
        self.image_path = 'Images/Tasks/'
        self.audio_path = 'Audio/General/'
        self.aud_practice_path = 'Audio/Practice/'
        self.aud_inst_path = 'Audio/Instructions/'

        #create practice instructions
        self.practice_instructions1 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 1: administrator demonstrates to child')
        self.practice_instructions2 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 2: administrator walks through trials with child')
        self.practice_instructions3 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text='Practice set 3: child completes trials on his/her own')
        self.practice_instructions4 = visual.TextStim(win, units='pix', pos=[0,0], height=20, text="Let's do some more practice")
        self.try_again = visual.TextStim(win, units='pix', pos=[0,0], height=20, text="Let's try that again.")

        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="  Let's do some practice.\n\nTouch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text='Touch anywhere to do some more practice.')
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Are you ready to begin?")

        #initializing audio files for practice and instructions
        self.practice_aud1 = sound.Sound(self.aud_practice_path + 'practice_cue1.wav')
        self.practice_aud2 = sound.Sound(self.aud_practice_path + 'practice_cue2.wav')
        self.practice_aud3 = sound.Sound(self.aud_practice_path + 'practice_cue3.wav')
        self.star_inst1 = sound.Sound(self.aud_inst_path + 'star_inst1.wav')
        self.star_inst2 = sound.Sound(self.aud_inst_path + 'star_inst2.wav')
        self.star_inst3 = sound.Sound(self.aud_inst_path + 'star_inst3.wav')

        #instructions
        self.instructions = visual.MovieStim(win=win,filename = self.aud_inst_path + 'stars_video_instructions.mp4', size = [1500,850], flipHoriz = True)
        self.audio_inst = sound.Sound(self.aud_inst_path + 'stars_instructions.wav')

        #time constrains
        self.t_blank = 2
        self.t_twinkle = 2
        self.t_mask = 1
        self.timer_limit = 12

        #repeat and continue button
        self.repeat_button=visual.ImageStim(win=win, name='repeat_button', image= self.image_path + 'repeat.png', units=u'pix', pos=[350, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)
        self.continue_button=visual.ImageStim(win=win, name='continue_button', image= self.image_path + 'continue.png', units=u'pix', pos=[420, -300], size=[75,75], color=[1,1,1], colorSpace=u'rgb', opacity=1.0)

        #trial variables
        self.t_twinkle = 3#when the star will twinkle
        self.bintang = visual.ImageStim(win=win, name='bintang', image = self.image_path + '/star.png', units = 'pix', ori = 0, pos = [0,0], size = [60, 60], opacity = 1, mask =None, interpolate = True)#stimulus
        self.twinkle = visual.ImageStim(win=win, name='twinkle', image = self.image_path + '/twinklingstar.png', units=u'pix', ori = 0, pos = [0,0], size = [62, 62], opacity = 1, mask =None, interpolate = True)#twinkle
        self.twinkle2 = visual.ImageStim(win=win, name='twinkle2', image = self.image_path + '/twinklingstar.png', units=u'pix', ori = 0, pos = [0,0], size = [62, 62], opacity = 1, mask =None, interpolate = True)#twinklefor END routine
        self.star_selected = visual.ImageStim(win=win, name='star_selected', image = self.image_path + '/star_selected.png', units = 'pix', ori = 0, size = [60, 60])
        self.drag = visual.ImageStim(win=win, name = 'drag', image = self.image_path + '/star2.png', units = 'pix', ori = 0, pos = [0,0], size = [60, 60], opacity = 1, mask =None, interpolate = True)
        self.circledrag = visual.Circle(win, name = 'circledrag', units = u'pix', radius = 30, ori=0, pos = [0,0])
        self.circletwinkle = visual.Circle(win, name = 'circletwinkle', units = u'pix', radius = 30, ori=0, pos = [0,0])
        self.mask = visual.ImageStim(win, name='mask2', image = self.image_path + '/mask.jpg', units=u'pix', ori=0, pos=[0, 0], size=[1500,850], opacity = 1, mask =None, interpolate = True)
        self.blank=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white', text='+', height=30)
        self.mouse=event.Mouse(win=win); self.mouse.getPos()


        #start feedback
        self.fb=feedback.fb(win)

        # number of degrees to exclude for star placement-- degrees given will be excluded on each side of the cardinal directions
        self.cardinal_exclusion_range = 7

        #create possible star positions in degrees
        self.degree_possibilities = []
        for x in [45,135,225,315]: self.degree_possibilities.extend(range(x-(44-self.cardinal_exclusion_range), x+(45-self.cardinal_exclusion_range)))


    def run_instructions(self, win):
        "Display the instructions for the game."
        #display instructions and wait
        self.audio_inst.play()
        while self.instructions._player.time <= int(self.instructions.duration):
            self.instructions.draw()
            win.flip()
        win.flip()

    # def run_instructions_w_demo(self,win):


    def run_practice(self, win, grade):
        "Run practice"

        def run_sub_practice(self,win,text_cue,aud_cue,stim_condition,score,with_practice,option):
            # self.repeat_button.draw() # self.continue_button.draw()
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
                self.repeat_button.draw()
                self.continue_button.draw()
                text_cue.draw()
                if aud_cue:
                    aud_cue.play()
                win.flip() #display instructions

                #wait 1 seconds before checking for touch
                start_time = self.trialClock.getTime()
                while start_time+1 > self.trialClock.getTime():
                    if 'escape' in event.getKeys():
                        if aud_cue:
                            aud_cue.stop()
                        return 'QUIT'
                #check for a touch
                cont=False
                self.mouse.getPos()
                while cont==False:
                    if self.click():
                        if self.repeat_button.contains(self.mouse): #self.mouse.mouseMoved()
                            if aud_cue:
                                aud_cue.stop()
                            return 'repeat'
                            break
                        elif self.continue_button.contains(self.mouse):
                            if aud_cue:
                                aud_cue.stop()
                            return 'continue'
                            break
                    if 'escape' in event.getKeys():
                        if aud_cue:
                            aud_cue.stop()
                        return 'QUIT'

            print 'with_practice', with_practice

            if with_practice==True:
                output = self.run_game(win, "", stim_condition) #run first practice trial

                print 'run practice'
                while output['Score']!=score:
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
                    output = self.run_game(win, "", stim_condition)

        def run_3_practice(inst,stimuli,score_conds):
            #draw practice instructions, and do sub practice
            for txt,stim,score in zip(inst,stimuli,score_conds):
                run_sub_practice(self,win,txt,None,stim,score,True,'no_repeat_option')

        run_3_practice([self.practice_instructions1,None,None],[150,100,115],[1,0,1])
        run_3_practice([self.practice_instructions2,None],[250,200],[1,1])
        run_3_practice([self.practice_instructions3,None],[200,150],[1,1])
        go_to_choice=False
        while go_to_choice==False:
            repeat_or_continue = run_sub_practice(self,win,self.practice_cue3,self.practice_aud3,None,None,False,'repeat_opt')
            if repeat_or_continue=='repeat': run_3_practice([self.practice_instructions4,self.practice_cue2],[200,150],[1,1])
            elif repeat_or_continue=='continue':
                print 'continue2'
                go_to_choice=True
            if 'escape' in event.getKeys(): go_to_choice=True; return 'QUIT'

    def run_game(self, win, grade, thisIncrement):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement)

    def run_trial(self, win, thisIncrement):
        sz= thisIncrement
        theseKeys = ""

        t=0; self.trialClock.reset()
        frameN=-1

        r = 250
        degree = choice(self.degree_possibilities)
        radians = degree*(2*math.pi/360)
        x = r*math.cos(radians)
        y = r*math.sin(radians)
        self.bintang.setPos([x,y]); self.bintang.setSize([sz, sz])
        self.twinkle.setPos([x,y]); self.twinkle.setSize([sz, sz])
        self.twinkle2.setPos([x,y]); self.twinkle2.setSize([sz, sz])
        self.circletwinkle.setPos([x,y]); self.circletwinkle.setRadius([sz/2]); self.circletwinkle.setLineColor('#f50af2')
        self.circledrag.setPos([0,0]); self.circledrag.setRadius([sz/2]); self.circledrag.setLineColor('white')
        self.drag.setPos([0,0]); self.drag.setSize([sz, sz]); self.drag.setImage(self.image_path + '/star2.png')

        print 'degree:', degree
        print 'radians:', radians
        print 'x, y:', x, y

        drag_started=False
        score=None
        self.mouse.setVisible(0)

        t1 = self.t_blank
        t2 = self.t_blank + self.t_twinkle
        t3 = self.t_blank + self.t_twinkle + self.t_mask
        tf = self.t_blank + self.t_twinkle + self.t_mask + self.timer_limit

        while t<=tf:
            t=self.trialClock.getTime()
            if t<=t1: 
                self.blank.draw()
                print 'blankdraw'
            if t>t1 and t<=t2:
                self.bintang.draw()
                self.twinkle.setOpacity((math.sin((2*math.pi)*6*(t-2)))*0.5 + 0.5)
                self.twinkle.draw()
                print 'twinkle'
            if t>t2 and t<=t3: 
                self.mask.draw()
                print 'mask'
            win.flip()
            first_click_time = None
            second_click_time = None
            status = 'NOT_STARTED'

            #allow participant to move star and make response, then check if correct
            self.mouse.setVisible(1)
            self.mouse.getPos()
            self.drag.setImage(self.image_path + '/star2.png')
            if t>t3 and t<=tf:
                self.drag.draw()
                start_time = self.trialClock.getTime()

                if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
                    if self.drag.contains(self.mouse.getPos()):
                        status='STARTED'
                        first_click_time = t - start_time
                        self.drag.setImage(self.image_path + '/star_selected.png')

                if status == 'STARTED' and (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])) and t >= first_click_time + start_time + 0.5:
                    second_click_time = t - start_time
                    self.drag.setImage(self.image_path + '/star2.png')
                    self.drag.setPos(self.mouse.getPos())
                    x_resp = self.drag.pos[0]
                    y_resp = self.drag.pos[1]
                    distance = ((y_resp - y)**2 + (x_resp - x)**2)**(0.5)
                    score = int(distance<=sz)

                if event.getKeys(keyList=['q', 'escape']):
                    return 'QUIT'
                win.flip()
                self.circledrag.setPos(self.drag.pos)
                self.circletwinkle.setPos(self.twinkle2.pos)

                print 'dragging'

            theseKeys = event.getKeys()
            if len(theseKeys)>0:
                if theseKeys[-1] in ['q','escape']: return 'QUIT'

        if t>tf:
            if not first_click_time: first_click_time = np.nan
            score, x_resp,y_resp,distance,second_click_time = (0,np.nan,np.nan,np.nan)
            print 'done'
        
        
        win.flip()  

        #give feedback
        self.fb.present_fb(win,score,[self.twinkle2,self.circletwinkle,self.drag,self.circledrag])

        #write data #headers are ['Trial Number', 'Difficulty','Score','Resp Time','Adaptive']

        output = {
            'threshold_var': float(sz),
            'level': None,
            'score': int(score),
            'resp_time': float(second_click_time-first_click_time),
            'spatial_click1': float(first_click_time),
            'spatial_click2': float(second_click_time),
            'resp_pos': "(%f, %f)"%(x_resp, y_resp),
            'target_pos': "(%f, %f)"%(x,y),
            'resp_target_dist': float(distance),
        }
        
        print output
        return output


    #method to get clicks
    def click(self):
        if touchscreen and self.mouse.mouseMoved(): return True
        elif not touchscreen and self.mouse.getPressed()==[1,0,0]: return True
        else: return False

if __name__=='__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(),os.pardir)))
    from Feedback import feedback

    #store info about the experiment session
    expName='REaCh Star Task'; expInfo={'participant':''}
    dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
    if dlg.OK==False: core.quit() #user pressed cancel
    expInfo['date']=data.getDateStr(); expInfo['expName']=expName
    fileName = expInfo['participant'] + expInfo['date']
    #dataFile = open('LDRH spatial data/' + fileName+'.txt', 'w')
    #dataFile.write('Level>Answer\n')

    win = visual.Window(size=(1500, 850), allowGUI=False
    , monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix', fullscr=False) #Window
#
#    #create the staircase handler
    staircase = data.StairHandler(startVal = 130,
          stepType = 'db', stepSizes=[10,5,2,1],#[8,4,4,2,2,1,1], #reduce step size every two reversals
          minVal=0, maxVal=350, nUp=1, nDown=3,  #will home in on the 80% threshold
          nTrials = 10)

    #initialize game
    game = Star_Game(win)

    #start feedback
    fb=feedback.fb(win)

    #step through staircase to find threshold
    for thisIncrement in staircase:
        output = game.run_game(win, "", thisIncrement)

        staircase.addData(output['Score'])
    #record the resulting threshold level of the training
    thresh = staircase._nextIntensity

    #run one iteration of game at threshold:
    game.run_game(win, "", thresh)
