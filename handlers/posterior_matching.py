import numpy as np
import ctypes
import math

from psychopy.data import StairHandler

class PosteriorMatchingIRL(StairHandler):
    def __init__(self,startVal, minVal=None, maxVal=None, axis=1, cuda=False, *args, **kwargs):

        StairHandler.__init__(self, startVal, minVal=minVal, maxVal=maxVal)
        #these are the info for the specific task
        # startVal = the starting level
        # minVal = the lowest level possible in the task
        # maxVal = the highest level possible int he task
        #for math task
        # - the axis will be indicated as 4
        # - the startVal, minVal, maxVal will be a list of 4 Values in this order [addition, substraction, multiplication, division]
        self.axis = axis

        self.pConstant = 1

        self.cuda = cuda

        self.initializePosterior()


    #makes 1-dimensional assumption as well
    def initializePosterior(self):
        self.pR = np.ones(shape=((self.maxVal - self.minVal + 1) * self.axis))

        #normalization; if this is done first, the first call to next() will return uniform median
        self.pR = self.pR / np.sum(self.pR)
        self.calculateNextIntensity()

    def addResponse(self, result, intensity=None):
        """Add a 1 or 0 to signify a correct/detected or incorrect/missed trial
        This is essential to advance the staircase to a new intensity level!
        Supplying an `intensity` value here indicates that you did not use the
        recommended intensity in your last trial and the staircase will
        replace its recorded value with the one you supplied here.
        """
        self.data.append(result)

        #if needed replace the existing intensity with this custom one
        if intensity!=None:
            self.intensities.pop()
            self.intensities.append(intensity)

        self.updatePosterior(result, intensity=intensity)

        #add the current data to experiment if poss
        if self.getExp() != None: #update the experiment handler too
            self.getExp().addData(self.name+".response", result)

        self.calculateNextIntensity()


    def addData(self, result):
        #this is where I'm passing the result to you. the result is either 1 or 0
        #for math task
        # - a list of 4 Values will be returned, which correspond to this order [addidion, substraction, multiplication, division]
        # - the result of the current operation will either be 1 or 0, whill the result of the other operation currently not give will be None

        self.addResponse(result)


    def updatePosterior(self, y, intensity=None): 

        if not intensity:
            intensity = self.intensities[-1]

        #Just a placeholder for when/if we get GPU stuff working.  When we get ADMM+S-map working, it will probably replace this section
        if self.cuda == True:

            #Here we will give the algorithm to the GPU for calculation of high dimensional posterior
            #We will have to give the kernel the following information:
            #self.pR, copy should be fine
            #y, so the kernel knows how to construct pY_W
            #Then...the kernel will update self.pR (or the copy of it), and we will have to retrieve it at the end of the call
            theDll = ctypes.CDLL("D://NIL//CudaIRL//CudaIRL//Debug//CudaIRL.dll")
            func = theDll['updatePosterior']

            #get all the data ready in ctypes format for call to C++ code
            pRp = (ctypes.c_float * len(self.pR.flatten()))(*self.pR.flatten())
            yP = (ctypes.c_float * len(y))(*y)
            qCatP = (ctypes.c_float * len(self.qCategories))(*self.qCategories)
            qLevelsP = (ctypes.c_float * len(self.qLevels))(*self.qLevels)

            # print 'y: ', y
            #print 'qCategories: ', self.qCategories
            # print 'qLevels: ', self.qLevels


            #Prototype: func(data, int numCategories, int numLevels, int* y, int* qCategories, int* qLevels, int demoSize,float pConstant)
            func(pRp, ctypes.c_int(self.numCategories), ctypes.c_int(self.numLevels), yP, qCatP, qLevelsP, ctypes.c_int(self.qLevels.shape[0]), ctypes.c_float(self.pConstant))

            #NEED THIS LINE TO GRAB POSTERIOR
            self.pR = np.frombuffer(pRp, ctypes.c_float)

            #hardcoding for 4-dimensional application here (e.g. math application)
            self.pR = self.pR.reshape(self.numLevels, self.numLevels, self.numLevels, self.numLevels)


            #this line can stay here for now, but will be using cuda accumulate-reduce technique in the future to speed it up
            self.pR = self.pR / np.sum(self.pR)

        #############1-dimensional assumption#######################
        else:

            for i in range(0, self.pR.shape[0]):

                #we calculate P(Y|W) for ever W we visit
                pY_W = 1
                curW = i

                #THIS IS HACKED FOR 1-D APPLICATION
                #It was the easiest way to accommodate the interface to the education system
                #Assumptions:
                #-y is 1-dimensional, and every iteration has only 1 response pertaining to the given axis
                #-the posterior self.pR is also 1-dimensional (i.e. only pertains to 1 subject at a time)

                pSuccess = np.exp(self.pConstant * (intensity - curW))
                pSuccess = pSuccess / (1 + pSuccess)
                if y == 0:
                    pY_W = pY_W * (1 - pSuccess)
                else:
                    pY_W = pY_W * pSuccess

                self.pR[i] = self.pR[i] * pY_W

            self.pR = self.pR / np.sum(self.pR)
	    
    #Selects the new qLevel given the current posterior
    #For the cuda case, we just select the first occurence max of the distribution
    #For the 1-dimensional assumption, we can select the median, so we are in line with Posterior Matching
    def calculateNextIntensity(self):

        skillLevel, maxMass = None, None

        if self.cuda == True:
            #using just the first occurrence max of the distribution for now
            skillLevel = np.zeros(shape=(self.numCategories))

            maxIndex = np.argmax(self.pR)
            maxMass = np.max(self.pR)

            for i in range(0, self.numCategories):
                skillLevel[i] = math.floor((maxIndex / math.pow(self.numLevels, self.numCategories - i - 1))) % self.numLevels

        ##################1 dimensional assumption###################
        #Pick the median (or one above the median anyway); proven optimal by Posterior Matching
        else:
            skillLevel = self.maxVal
            currentMass = 0.0

            for i in range(0, self.pR.shape[0])[::-1]:
                currentMass = currentMass + self.pR[i]
                if currentMass > 0.5:
                    skillLevel = i
                    # Check for 95% probability mass on a particular discrete value.
                    if self.pR[i] >= 0.95:
                        print "Found it!"
                        self.finished = True
                    break

        self._nextIntensity = skillLevel
