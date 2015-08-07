
class posterior_matching:
    def __init__(self,startval,minval,maxval,axis):
        #these are the info for the specific task
        # startval = the starting level
        # minval = the lowest level possible in the task
        # maxval = the highest level possible int he task
        #for math task
        # - the total_axis will be indicated as 4
        # - the startval, minval, maxval will be a list of 4 values in this order [addition, substraction, multiplication, division]
        self.startval = startval
        self.minval = minval
        self.maxval = maxval
        self.axis = axis
        
        
    def addData(score):
        #this is where I'm passing the score to you. the score is either 1 or 0
        #for math task
        # - a list of 4 values will be returned, which correspond to this order [addidion, substraction, multiplication, division]
        # - the score of the current operation will either be 1 or 0, whill the score of the other operation currently not give will be None
        print 'addData() still in progress'
        
    def next():
        #please return the next level
        print 'next() still in progress'