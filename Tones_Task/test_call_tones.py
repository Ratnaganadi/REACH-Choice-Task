from psychopy import gui, visual, core, data, event, logging, sound, info, misc
import time, numpy
from math import floor
from random import randint
from LDRH_tones_obj import Tones_Game

#present a dialogue to change params
expInfo = {'participant':''}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
dlg = gui.DlgFromDict(expInfo, title='LDRH', fixed=['date'])
if dlg.OK:
    pass #misc.toFile('lastParams.pickle', expInfo)#save params to file for next time
else:
    core.quit()#the user hit cancel so exit

#make a text file to save data
fileName = expInfo['participant'] + dateStr
#dataFile = open('data/' + fileName+'.txt', 'w')
#dataFile.write('targetSide	oriIncrement	correct\n')

#create window and clocks
globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window([1200,800],fullscr=False,allowGUI=True, monitor='testMonitor', units='deg')

#create the staircase handler
staircase = data.StairHandler(startVal = 7,
    stepType = 'lin', stepSizes=[2,2,1,1], #reduce step size every two reversals
    minVal=0, maxVal=12,
    nUp=1, nDown=3,  #will home in on the 80% threshold
    nTrials = 8)

#initialize game
game = Tones_Game(win)

game.run_game(win, 4, None)
game.run_game(win, 3, None)
game.run_game(win, 2, None)
game.run_game(win, 1, None)

#step through staircase to find threshold
for thisIncrement in staircase: 
    game.run_game(win, thisIncrement, staircase)
#record the resulting threshold level of the training
thresh = staircase._nextIntensity

#run one iteration of game at threshold:
game.run_game(win, thresh, None)