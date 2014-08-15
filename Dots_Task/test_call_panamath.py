from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
import random
from LDRH_panamath_final_obj import Dots_Game

#store info about the experiment session
expName='LDRH Task'#from the Builder filename that created this script
expInfo={'participant':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('LDRH data'):
    os.makedirs('LDRH data') #if this we will get error
filename='LDRH data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#setup the Window
win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb')

#set up handler to look after randomisation of conditions etc
level_now = 15
n_level=data.TrialHandler(nReps = level_now, method=u'random', 
    extraInfo=expInfo, originPath=None,
    trialList=[None], seed=None)
thisN_level=n_level.trialList[0]#so we can initialise stimuli with some values
#abbreviate parameter names if possible (e.g. rgb=thisN_level.rgb)
if thisN_level!=None:
    for paramName in thisN_level.keys():
        exec(paramName+'=thisN_level.'+paramName)

#initialize game
game = Dots_Game(win)

for thisN_level in n_level:
    game.run_game(win, thisN_level, n_level)