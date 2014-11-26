import random
from params import *

class Beach:
    '''Beach class defines the interface between ocean and other tiles'''
    
    tDim = PARAM_TILE_SIZE #river size - MUST MATCH TILE CLASS SIZE
    
    def __init__(self, cornerXY, numRivers, seed = None):
        '''inputs:    cornerXY    = (X,Y) pair of top left corner bounding this river set
                      seed        = usual random seed param for a class'''
        
        self.x = cornerXY[0]
        self.y = cornerXY[1]
        self.entryPtXY = None
        
        if(seed == None):
            self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
        else:
            self.seed = seed           
        
        self.xyPts = {}
        self.exitPtXY = None
        
        if(PARAM_DEBUG_EN_BEACHES):
            print("New Beach, ((x,y), seed) = ("+str((self.x,self.y))+", "+self.seed+")")
        
    def preDrawBeachReport(self, entryPtXY):
        '''generate the list of beach x,y coords (global units) in this tile
                    entryPtsXY    = (X,Y) beach entry point in global coords '''       
        
        by = entryPtXY[1]
        for bx in range(self.x,self.x+self.tDim):
            goodNextY = []
            for nextY in range(by-1,by+2):
                if (nextY <= self.y or nextY >= self.y+self.tDim):
                    continue
                goodNextY.append(nextY)
        
            #if(PARAM_DEBUG_EN_BEACHES):
                #print("beach x: "+str(bx)+" selfx: "+str(self.x)+", goodNextY: "+str(goodNextY))        

            by = random.choice(goodNextY)
            self.xyPts[bx] = by
        
        self.exitPtXY = (bx,by)
        
        if(PARAM_DEBUG_EN_BEACHES):
            print("beach preDraw report, xyPts = "+str(self.xyPts)+", exitPtXY: "+str(self.exitPtXY))
        
        