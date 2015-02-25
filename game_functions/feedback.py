from psychopy import core, visual, gui, data, misc, event, sound
import os

class fb:
    
    def __init__(self, win):
        "Initialize the stimuli and iteration numbers, and import conditions"
        #get dir for importing conditions
        self.fn = os.path.dirname(__file__)
        #file paths
        image_path = 'Images/Tasks/'
        audio_path = 'Audio/General/'

        self.trialClock=core.Clock()
        
        #initialize check and x
        self.green_check=visual.ImageStim(win=win, name='green_check', units=u'pix', image=image_path + '/green_check2.png', mask=None, ori=0, pos=[0,0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1, texRes=128, interpolate=True, depth=-4.0)
        self.red_x=visual.ImageStim(win=win, name='red_x', units=u'pix', image=image_path + '/red_x.png', mask=None, ori=0, pos=[0, 0], size=[128, 128], color=[1,1,1], colorSpace=u'rgb', opacity=1, texRes=128, interpolate=True, depth=-4.0)
        
        self.ding=sound.Sound(value = audio_path + '/Ping.wav')
        self.ding.setVolume(0.15)
        self.honk=sound.Sound(value=audio_path+'/Basso.wav')
        self.honk.setVolume(0.15)

        
    def present_fb(self, win, score, objects):
        """Display the feeback for the game. Requires the window, the score, 
            and a list of the objects already on the screen to be presented with the feedback."""
        #determine fb
        if score: 
            fb = self.green_check
            sound = self.ding
        else: 
            fb = self.red_x
            sound = self.honk
        
        #check if objects is a list
        if type(objects)!=list:
            print 'objects passed to feedback must be a list; instead got {}'.format(type(objects))
            core.quit()
        #display objects and feedback
        for object in objects:
            object.draw()
        fb.draw()
        win.flip()
        sound.play()
        
        
        #wait 2 seconds
        start_time=self.trialClock.getTime()
        timer=0
        while timer<1:
            timer= self.trialClock.getTime() - start_time
            these_keys=event.getKeys(keyList=['escape'])
            if 'escape' in these_keys: core.quit()
        