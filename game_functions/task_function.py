from psychopy import sys, visual, core, data, event, logging, gui, sound
import os, random
from random import shuffle

class task_functions:
    #initialize variables, fixation cross and mouse
    def __init__(self, win):
        self.trialClock=core.Clock()
        image_path = 'Images/Tasks/'
        self.fixation=visual.TextStim(win, ori=0, font=u'Arial', pos=[0, 0], color=u'white',text=u'+')
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()
        self.double_click = False
        self.double_time = None
        self.double_time2 = None
        self.double_time3 = None

    def quit_check(self,win):
        ## QUIT check ##
        #get key inputs
        key = event.getKeys()

        #check for 'QUIT' from the keyboard
        if key==['escape'] or key==['period']*3: return 'QUIT'

        #check for 'QUIT' from the clicker (triple click)
        if self.double_time and not self.double_time2 and self.trialClock.getTime()-self.double_time>=1: self.double_click, self.double_time = False, None
        elif self.double_time2 and not self.double_time3 and self.trialClock.getTime()-self.double_time2>=1: self.double_click, self.double_time, self.double_time2 = False, None, None
        
        if self.double_click==False and key==['period']:
            self.double_click = 'maybe'
            self.double_time = self.trialClock.getTime()
        elif self.double_click=='maybe' and key==['period']:
            self.double_time2 = self.trialClock.getTime()
            if self.double_time2 - self.double_time >1: self.double_click, self.double_time, self.double_time2 = False, None, None
            elif self.double_time2 - self.double_time<=1:self.double_click = 'yes'
        elif self.double_click=='yes' and key==['period']:
            self.double_time3 = self.trialClock.getTime()
            if self.double_time3-self.double_time2>1: self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None
            elif self.double_time3-self.double_time2<=1: 
                return 'QUIT'


    def fixation_function(self,win):
        ## Fixation cross with pause, play, repeat (for the whole task) ##

        #initialize variables#
        thisResp=None #denotes if we continue, repeat, or pause the task
        pause=False #pause variable
        # self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None #double click variable

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
            if self.double_time and not self.double_time2 and self.trialClock.getTime()-self.double_time>=1: 
                self.double_click, self.double_time = False, None
            elif self.double_time2 and not self.double_time3 and self.trialClock.getTime()-self.double_time2>=1: 
                self.double_click, self.double_time, self.double_time2 = False, None, None
            
            #pausing if pressed once, quit if pressed three times
            if self.double_click==False and (key==['period'] or key==['down']):
                thisResp, pause = None, True
                self.double_click = 'maybe'
                self.double_time = self.trialClock.getTime()
            elif self.double_click=='maybe' and key==['period']:
                self.double_time2 = self.trialClock.getTime()
                if self.double_time2 - self.double_time >1: 
                    self.double_click, self.double_time, self.double_time2 = False, None, None
                elif self.double_time2 - self.double_time<=1:
                    self.double_click = 'yes'
            elif self.double_click=='yes' and key==['period']:
                self.double_time3 = self.trialClock.getTime()
                if self.double_time3-self.double_time2>1: 
                    self.double_click, self.double_time, self.double_time2, self.double_time3 = False, None, None, None
                elif self.double_time3-self.double_time2<=1:
                    return 'QUIT'
            choice_time=self.trialClock.getTime()-start_time
        
        #if fixation cross is over, then continue to trial
        if self.trialClock.getTime()-start_time>1.5:
            if thisResp!='repeat_task': thisResp='continue_task'

        #return thisResp (continue, repeat, quit) to run_trial method
        if thisResp!=None: return thisResp

class questionnaire:
    def __init__(self,win):
        self.trialClock=core.Clock()
        # image_choice_path = 'icons/'
        image_choice_path = 'Images/Choice/'
        image_q_path = 'Images/questionnaire/'

        #mouse
        self.mouse = event.Mouse(win=win)
        self.mouse.getPos()

        #game logo
        self.star_icon = visual.ImageStim(win=win, name='star', image = image_choice_path + 'stars.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
        self.phonology_icon = visual.ImageStim(win=win, name='phonology', image = image_choice_path + 'phonology2.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
        self.math_icon = visual.ImageStim(win=win, name='math', image = image_choice_path + 'math.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
        self.music_icon = visual.ImageStim(win=win, name='music', image = image_choice_path + 'music.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)
        self.reading_icon = visual.ImageStim(win=win, name='reading', image = image_choice_path + 'reading.png', units = 'pix', ori = 0, pos = [0,0], size = [126, 120], opacity = 1, mask =None, interpolate = True)
        self.dots_icon = visual.ImageStim(win=win, name='dots', image = image_choice_path + 'panamath.png', units = 'pix', ori = 0, pos = [0,0], size = [120, 120], opacity = 1, mask =None, interpolate = True)

        #smile icon
        self.smile1 = visual.ImageStim(win=win, name='smile1', image = image_q_path + 'smile1.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.smile2 = visual.ImageStim(win=win, name='smile2', image = image_q_path + 'smile2.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.smile3 = visual.ImageStim(win=win, name='smile3', image = image_q_path + 'smile3.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.smile4 = visual.ImageStim(win=win, name='smile4', image = image_q_path + 'smile4.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.smile5 = visual.ImageStim(win=win, name='smile5', image = image_q_path + 'smile5.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.smile6 = visual.ImageStim(win=win, name='smile6', image = image_q_path + 'smile6.png', units = 'pix', ori = 0, pos = [0,0], size = [100, 100], opacity = 1, mask =None, interpolate = True)
        self.line = visual.Line(win, units='pix', start=[0,0], end=[0,0], lineWidth = 5)
        
        #questions
        self.q_favorite_task = visual.TextStim(win, name='favorite_game', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Which one of these games\n    do you like the most?')
        self.q_why_most_favorite = visual.TextStim(win, name='why_most_favorite', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Why did you like this game the most?')
        self.q_why_least_favorite = visual.TextStim(win, name='why_least_favorite', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Why did you like this game the least?')
        self.q_easiest_task = visual.TextStim(win, name='easiest_game', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Which one of the games below is the easiest?')
        self.q_why_easiest = visual.TextStim(win, name='why_easiest', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Why is this game the easiest?')
        self.q_why_hardest = visual.TextStim(win, name='why_hardest', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'Why is this game the hardest?')
        self.q_like_reading = visual.TextStim(win, name='rank_reading', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'How much do you like reading?')
        self.q_like_math = visual.TextStim(win, name='rank_math', ori=0, font=u'Arial', height=32, pos=[0, 150], color=u'white',text=u'How much do you like math?')
        self.why_instruction = visual.TextStim(win, ori=0, font=u'Arial', height=20, pos=[0, -100], color=u'white',text=u"(Start typing when you are ready)")
        
        #next button
        self.button = visual.ImageStim(win=win, name='next_button', image = image_q_path + 'general_button.png', units = 'pix', ori = 0, pos = [0,-300], size = [120, 60], opacity = 1, mask =None, interpolate = True)
        self.next = visual.TextStim(win, ori=0, font=u'Arial', height = 32, pos=[0, -300], color=u'white',text=u'NEXT')
        self.next_instructions = visual.TextStim(win, ori=0, font=u'Arial', height = 22, pos=[0, -250], color=u'white',text=u"(Click 'NEXT' to confirm your answer)")
        self.tf = task_functions(win)

    def run_questionnaire(self,win):

        def rank_games(txt, icons):

            thisResp = None

            w = 700
            y = 0
            xpos = [-140*(len(icons)-1)/2 + 140*i for i in range(0, len(icons))]
            # xpos = [-w/2 + (w*i)/len(icons) for i in range(0, len(icons)+1)]
            xypos = [[x,y] for x in xpos]
            shuffle(xypos)

            # self.trialClock.reset()
            for icon, pos in zip(icons, xypos):
                icon.setPos(pos)
                icon.draw()

            if txt: txt.draw()
            win.flip()
            core.wait(0.5)

            #get mouse position
            self.mouse.getPos()

            while thisResp==None:
                # key = event.getKeys()
                # if key: print 'key',key
                
                if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
                    if self.star_icon in icons and self.star_icon.contains(self.mouse): thisResp = str(self.star_icon.name)
                    if self.phonology_icon in icons and self.phonology_icon.contains(self.mouse): thisResp = str(self.phonology_icon.name)
                    if self.math_icon in icons and self.math_icon.contains(self.mouse): thisResp = str(self.math_icon.name)
                    if self.music_icon in icons and self.music_icon.contains(self.mouse): thisResp = str(self.music_icon.name)
                    if self.reading_icon in icons and self.reading_icon.contains(self.mouse): thisResp = str(self.reading_icon.name)
                    if self.dots_icon in icons and self.dots_icon.contains(self.mouse): thisResp = str(self.dots_icon.name)


            return thisResp


        def ask_why(thisIcon, whyText):
            print 'ask', str(whyText.text)

            txt=''
            thisResp = None
            symbols = {'space': ' ', 'comma': ',', 'period': '.', 'apostrophe':"'", 'return':'\n'}
            thisIcon.setPos([0,0])
            #until return pressed, listen for letter keys & add to text string
            # while event.getKeys(keyList=['return'])==[]:

            #get mouse position
            self.mouse.getPos()
            
            while thisResp==None:
                thisIcon.draw()
                whyText.draw()
                self.why_instruction.draw()
                self.button.draw()
                self.next.draw()

                if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])) and self.button.contains(self.mouse): 
                    if txt!='': thisResp = 'next'

                letterlist=event.getKeys(keyList=['escape','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','backspace','space','comma','period','apostrophe','return'])
                for l in letterlist:
                    #if key isn't backspace, add key pressed to the string
                    if l=='backspace': txt=txt[:-1]
                    elif l=='escape': return 'QUIT'
                    else:
                        if l in symbols.keys(): l = symbols[l]
                        txt+=l

                #continually redraw text onscreen until return pressed
                response = visual.TextStim(win, units = 'pix', font=u'Arial', height=28, pos=[0,-160], color=u'white', text=txt)
                response.draw()

                # if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                win.flip()
            event.clearEvents()
            print txt
            return txt

        def run_rank_games(thisquestion,thiswhy1,thiswhy2):

            icon_dict = {
                'star': self.star_icon,
                'phonology': self.phonology_icon,
                'math': self.math_icon,
                'music': self.music_icon,
                'reading': self.reading_icon,
                'dots': self.dots_icon}
            icon_list = [self.star_icon, self.phonology_icon, self.math_icon, self.music_icon, self.reading_icon, self.dots_icon]

            thisRank = []
            thisWhy = []
            for i in range(0, len(icon_list)):
                print [x.name for x in icon_list]
                thisText, whyTxt, task, ans = None, None, None, None
                if len(icon_list)!=1:
                    ans = rank_games(thisquestion, icon_list)
                    print ans,
                    if ans=='QUIT': return 'QUIT'
                    elif ans: 
                        print 'removed'
                        thisRank.append(ans)
                        icon_list.remove(icon_dict[ans])

                elif len(icon_list)==1: 
                    whyTxt = thiswhy2
                    task = str(icon_list[-1].name)
                if i==0: 
                    whyTxt = thiswhy1
                    task = ans

                if whyTxt:
                    thisText = str(whyTxt.text).replace('this game','the {} game'.format(task.upper()))
                    whyTxt.setText(thisText)
                    ans_why = ask_why(icon_dict[task],whyTxt)
                    if ans_why=='QUIT': return 'QUIT'
                    elif ans_why: thisWhy.extend(ans_why)

            return [thisRank, thisWhy]

        def rank16_icons(thisquestion):
            w = 700
            y = 0
            icons = [self.smile1, self.smile2, self.smile3, self.smile4, self.smile5, self.smile6]
            xypos = [[(-140*(len(icons)-1)/2 + 140*i), y] for i in range(0, len(icons))]
            self.line.setStart(xypos[0])
            self.line.setEnd(xypos[-1])
            # xypos = [[x,y] for x in xpos]

            thisList = []
            for q in thisquestion:
                

                # core.wait(0.5)
                thisResp, ans = None, None
                self.mouse.getPos()
                while thisResp==None:
                    q.draw()
                    self.button.draw()
                    self.next.draw()
                    self.next_instructions.draw()

                    # self.line.draw()
                    for icon,pos in zip(icons,xypos):
                        icon.setPos(pos)
                        icon.draw()

                    if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                    if self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0]):
                        if self.smile1.contains(self.mouse): 
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 1; self.smile1.setSize([120,120])
                        elif self.smile2.contains(self.mouse):
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 2; self.smile2.setSize([120,120])
                        elif self.smile3.contains(self.mouse):
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 3; self.smile3.setSize([120,120])
                        elif self.smile4.contains(self.mouse):
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 4; self.smile4.setSize([120,120])
                        elif self.smile5.contains(self.mouse):
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 5; self.smile5.setSize([120,120])
                        elif self.smile6.contains(self.mouse):
                            if ans: icons[ans-1].setSize([100,100])
                            ans = 6; self.smile6.setSize([120,120])

                        if ans and self.button.contains(self.mouse):
                            icons[ans-1].setSize([100,100])
                            thisResp = ans
                    win.flip()
                if thisResp: thisList.extend(str(thisResp))

            return thisList


        print 'rank_games'

        #prepare output dictionary
        output = {}
        #rank games - most to least favorite and easiest to hardest
        for q,qwhy1,qwhy2 in zip([self.q_favorite_task, self.q_easiest_task],[self.q_why_most_favorite,self.q_why_easiest],[self.q_why_least_favorite,self.q_why_hardest]):
            answers = run_rank_games(q,qwhy1,qwhy2)
            if answers=='QUIT': return 'QUIT'
            else:
                output[str(q.name)] = answers[0]
                output[str(qwhy1.name)] = answers[1][0]
                output[str(qwhy2.name)] = answers[1][1]

        #rank reading and math
        answers2 = rank16_icons([self.q_like_reading, self.q_like_math])
        if answers2=='QUIT': return 'QUIT'
        elif answers2: 
            output['rank_reading'] = answers2[0]
            output['rank_math'] = answers2[1]

        core.wait(0.5)
        
        

                    








