from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os, random, math
from random import shuffle
from LDRH_spatial_obj import Star_Game

#store info about the experiment session
expName='LDRH Task'; expInfo={'participant':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr(); expInfo['expName']=expName
fileName = expInfo['participant'] + expInfo['date']
#dataFile = open('LDRH spatial data/' + fileName+'.txt', 'w')
#dataFile.write('Level>Answer\n')

win = visual.Window(size=(1100, 700), allowGUI=True, monitor=u'testMonitor', color=[-1,-1,-1], colorSpace=u'rgb', units=u'pix') #Window

#create the staircase handler
staircase = data.StairHandler(startVal = 100,
                          stepType = 'db', stepSizes=[10,5,2,1],#[8,4,4,2,2,1,1], #reduce step size every two reversals
                          minVal=0, maxVal=350, nUp=1, nDown=1,  #will home in on the 80% threshold
                          nTrials = 10)

#initialize game
game = Spatial_Game(win)

#step through staircase to find threshold
for thisIncrement in staircase: 
    game.run_game(win, thisIncrement, staircase)
#record the resulting threshold level of the training
thresh = staircase._nextIntensity

#run one iteration of game at threshold:
game.run_game(win, thresh, None)