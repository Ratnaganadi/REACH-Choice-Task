from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy, os, sys, tempfile, wave
from os.path import join
from math import floor
from random import randint, choice, shuffle
from game_functions import task_function, feedback
from practice import practice_functions

#touchscreen or not
touchscreen = True

class Phonology_Game(practice_functions):

    def __init__(self, win, conditions):

        #file paths for importing conditions, images and audio
        self.dir = os.path.dirname(__file__)
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'
        aud_practice_path = 'Audio/Practice/'
        aud_inst_path = 'Audio/Instructions/'
        self.phonologystim_dir = 'Audio/Stimuli/Phonology/'
        #get tempdir for phoneme generated on the go
        self.temp_dir = tempfile.gettempdir()


        ## initialize trial components ##

        #time components and time constrains for trial
        self.trialClock = core.Clock()
        self.t_initialspeaker = 1
        self.t_stimgap = 1
        self.timer_limit = 12

        #trial condition
        self.trialList=conditions

        #mouse
        self.mouse=event.Mouse(win=win)
        self.mouse.getPos()

        #start feedback
        self.fb=feedback.fb(win)
        self.tf=task_function.task_functions(win)

        #create a dictionary to keep track of how many times you've displayed each difficulty level
        self.iteration = {}
        for question in range(len(self.trialList)):
            self.iteration[question] = 0

        #list to keep track of history of answers
        self.answer_history = []


        ## initialize text, audio & image stimuli ##

        #practice instructions texts
        self.practice_cue1 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Touch anywhere to begin.")
        self.practice_cue2 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Let's do some more.")
        self.practice_cue3 = visual.TextStim(win, units=u'pix', wrapWidth=700, pos=[0,0],height=28,text="Touch anywhere to begin.")

        #audio files for practice and instructions
        self.practice_aud1 = sound.Sound(aud_practice_path + 'practice_cue1.wav')
        self.practice_aud3 = sound.Sound(aud_practice_path + 'practice_cue3.wav')

        #create stimuli images & buttons
        self.speaker = visual.ImageStim(win=win, name='speaker',image=image_path +'/speaker.png', mask = None, units=u'pix',ori=0, pos=[0,200], size=[115,115])
        self.speaker_playing = visual.ImageStim(win=win, name='speaker',units=u'pix',image=image_path +'/speaker_playing_white.png', mask = None,ori=0, pos=[45,200], size=[220,155])
        self.same_button = visual.ImageStim(win, image=image_path + '/happy_button.png', pos=[-260, -200])
        self.different_button = visual.ImageStim(win, image=image_path + '/sad_button.png', pos=[260, -200])


    def run_practice(self, win, task, grade):
        "Run practice"

        #instruction texts
        inst_set=[self.practice_cue1,None,None,self.practice_cue2, self.practice_cue3]
        
        #instruction audio
        aud_set=[self.practice_aud1,None,None]+[None]*2
        
        #stimuli set for practice
        stim_set = [4,3,1]+[None]*2
        
        #stimuli for repeated practice (currently the same as the initial stimuli set)
        stim_repeat = stim_set
        
        #variable, needed for some task's trial
        var = ''
        
        #score condition, whether we want to constrain trial to be correct or incorrect
        score_cond = [None]*5
        
        return self.run_practice_functions(win, grade, inst_set, aud_set, stim_set, stim_repeat, score_cond, var, task)

    def concat_wavs(self, infiles, outfile):
        data=[]
        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        output = wave.open(outfile, 'w')
        output.setparams(data[0][0])
        for i in range(len(infiles)):
            output.writeframes(data[i][1])
        output.close()


    def run_game(self, win, grade, thisIncrement, var):
        "Run one iteration of the game with self.trialList as conditions."
        return self.run_trial(win, thisIncrement, var)

    def run_trial(self, win, thisIncrement, var):
        "Run one iteration of the game."

        ## initialize functions ##

        def get_stims(stim):
            # This function join stimuli strings, join audio file corresponding to those strings, 
            # return audio, length and raw audio stimuli

            #get phoneme strings and join the string
            phonemes = [stim[x:x+2] for x in [0,2,4]]
            stim_files = [join(self.phonologystim_dir, phoneme.upper()+'.wav') for phoneme in phonemes]
            fn = join(self.temp_dir,'%s.wav'%stim)

            #concat/join audio file of phonemes
            self.concat_wavs(stim_files, fn)

            #turn sound into useable audio format for psychopy, return audio, length and raw stim
            audio = sound.Sound(value=fn)
            audio_length = audio.getDuration()
            return [audio,audio_length,stim]

            #remove audio file from memory
            os.remove(fn)
        
        def draw_play_phonemes(audio,wait_time):
            # This function draw stimuli screen, play audio file 
            # and make sure audio plays until the end before the next audio files play

            #draw initial speaker before phoneme plays
            self.speaker.draw()
            win.flip()
            core.wait(wait_time)
            self.speaker_playing.draw()
            win.flip()
            
            #play phoneme
            audio.play()

            #make sure the audio plays until the end of audio duration while checking for 'QUIT'
            start_time = self.trialClock.getTime()
            # double_click, double_time, double_time2, double_time3 = False, None, None, None
            while self.trialClock.getTime() < start_time + audio.getDuration():
                if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                

        ## get difficulty index ## 
        # normally, the difficulty level would be the diff from staircasing -1, because difficulty is ordered in the stimuli file
        try:
            diff = len(self.trialList)-thisIncrement
            index = diff-1

            #double check. if 'difficulty'!=diff, look for matching index for difficulty
            #for each index (=question) in trialList, check if the 'difficulty' value matches the difficulty from staircasing
            #assign index as the 'index' we use if match is found
            if self.trialList[index]['Difficulty']!=diff:
                for question in range(len(self.trialList)):
                    if int(self.trialList[question]['Difficulty']) == (len(self.trialList)-thisIncrement):
                        index = question
        except: 
            print 'ERROR: index set to zero. Could not get index for', thisIncrement, 'in', range(len(self.trialList))
            index = 0


        ## check iteration ##
        #ensure iteration does not exceed length of available trials:
        if self.iteration[index] > len(self.trialList[index]['Stim1'])-1:
            self.iteration[index] = 0

        #check history to make sure we don't get more than three identical answers in a row; modify iteration if needed
        count=0 #give up after 50 tries
        while len(self.answer_history)>=3 and len(set(self.answer_history[-3:]))==1 and self.trialList[index]['Correct Response'][self.iteration[index]]==self.answer_history[-1] and count<50:
            if self.iteration[index] == len(self.trialList[index]['Stim1'])-1:
                self.iteration[index] = 0
            else:
                self.iteration[index] += 1
            count+=1


        ## get trial variables ##
        #using index and iteration info above

        #difficulty level
        difficulty = self.trialList[index]['Difficulty']

        #stimuli content
        stimA = self.trialList[index]['Stim1'][self.iteration[index]]
        stimB = self.trialList[index]['Stim2'][self.iteration[index]]
        
        #content and foil
        target_content = self.trialList[index]['Correct Response'][self.iteration[index]]
        contents = ['same','different']
        contents.remove(target_content)
        foil_content = contents[0]
        print 'thisIncrement: {} | Difficulty: {} |'.format(thisIncrement, difficulty),
        # print 'thisIncrement: {} | Difficulty: {} | {} {} {} | '.format(thisIncrement, difficulty, stimA, stimB, target_content),

        #update answer_history
        self.answer_history.append(target_content)


        ## prepare stimuli, target & foil ##

        #getstim() returns [audio,audio_length,raw audio]
        audioA = get_stims(stimA) 
        audioB = get_stims(stimB)

        #shuffle audio stimuli order
        audio_order = [audioA,audioB]
        shuffle(audio_order)

        #prepare stimuli variable from get_stims() for trial
        stim1 = audio_order[0][0]
        stim2 = audio_order[1][0]
        raw_stim1 = audio_order[0][2]
        raw_stim2 = audio_order[1][2]
        
        #target & foil position
        pos = {'same':['left',self.same_button], 'different':['right',self.different_button]}
        target_pos = pos[target_content][0]
        foil_pos = pos[foil_content][0]
        self.target_button = pos[target_content][1]
        self.foil_button = pos[foil_content][1]

        
        ## trial ##

        ## fixation ##
        # displayed at the beginning of each trial.
        # here, experimenter has the option to pause the task temporarily, or repeat the whole subtask in special cases

        #check task_status from fixation function
        task_status = self.tf.fixation_function(win)

        #if 'QUIT' or 'repeat' returned, return task status to main choice code
        if task_status in ['QUIT','repeat_task']: return task_status

        ## if 'continue', proceed to trial ## 
        elif task_status=='continue_task':
            
            ## initialize variable ##
                
            #for output and triple click check
            choice_time, score, thisResp, thisResp_pos = 0, None, None, None
            
            #reset trialClock
            self.trialClock.reset()

            while thisResp==None:

                ## QUIT check ##
                if self.tf.quit_check(win)=='QUIT': return 'QUIT'
                
                ## display stimuli, target, foil and trial components##
                #display appropriate images in appropriate order for the task
                for stim,wait in zip([stim1,stim2],[self.t_initialspeaker,self.t_stimgap]):
                    if draw_play_phonemes(stim,wait)=='QUIT': return 'QUIT'
                self.speaker.draw()
                self.target_button.draw()
                self.foil_button.draw()
                win.flip()


                ## check response ##

                #start timer for response
                start_time=self.trialClock.getTime()
                self.mouse.getPos() #called to prevent last movement of mouse from triggering click

                #check for response when time is within time limit
                while choice_time<=self.timer_limit:
                    if (self.mouse.mouseMoved() or (self.mouse.getPressed()==[1,0,0])):
                        if self.target_button.contains(self.mouse): score,thisResp,thisResp_pos = (1,target_content,target_pos)
                        elif self.foil_button.contains(self.mouse): score,thisResp,thisResp_pos = (0,foil_content,foil_pos)
                    #calculate reaction time
                    choice_time=self.trialClock.getTime()-start_time

                
                ## time out ##
                #if participant does not respond by time limit
                if self.trialClock.getTime()-start_time>self.timer_limit:
                    score,thisResp,thisResp_pos,choice_time = (0,'timed_out','timed_out','timed_out')
                    print 'TIME OUT |',
            

            ## feedback ##
            self.fb.present_fb(win,score,[self.speaker,self.target_button,self.foil_button])

            
            ## data output dictionary ##
            thresh = ['D3_PA-GA_KA-BA','D2_both_BA-TA_GA-TA_PA-DA_KA-DA','D1_POA__PA-TA_KA-TA_BA-DA_GA-DA','D2_POA_TA-DA_PA-KA_BA-GA_TA-DA','D1_VOT_PA-BA_KA-GA']
            threshold_var = thresh[difficulty-1]

            output = {
                'threshold_var': threshold_var,
                'level': difficulty,
                'score': score,
                'resp_time': choice_time,
                'stim1': raw_stim1,
                'stim2': raw_stim2,
                'resp': thisResp,
                'resp_pos': thisResp_pos,
                'target': target_content,
                'target_pos': target_pos,
            }
            #output aditional information taken from stimuli file
            output_header = ['phoneme_difference','POA_steps','VOT_steps','VOT_or_POA','phoneme_dif_pos','phoneme_dist']
            stim_header = ['Phoneme Difference','POA_steps','VOT_steps','VOT_or_POA','Difference Position','Distance']
            for out_col,stim_col in zip(output_header,stim_header):
                output.update({out_col:self.trialList[index][stim_col][self.iteration[index]]})
            

            ## update iteration of current difficulty ##
            if self.iteration[index] == len(self.trialList[index]['Stim1'])-1:
                self.iteration[index] = 0
            else:
                self.iteration[index] += 1
            return output
            