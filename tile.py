import random
from params import *
import mtn
import rivers
import beach

class Tile:
    '''Tile class to combine mountains, rivers, etc.'''
    
    tDim = PARAM_TILE_SIZE #size of tiles is a property of the class
    
    def __init__(self, x, y, tileType, mtnInfo, riverInfo, seed = None):
        self.mtnList = [];
        self.rivers = []
        
        self.x = x
        self.y = y
        
        maxMtns = mtnInfo[0]
        mtnProb = mtnInfo[1]
        
        if(seed == None):
            self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
        else:
            self.seed = seed
            
        '''if necessary, pad seed to full 10 digits'''
        self.seed = '0'*(10-len(self.seed)) + self.seed

        self.tileType = tileType
        
        if(PARAM_DEBUG_EN_GENERAL):
            print("tile "+str((x,y))+" init: "+tileType+", seed: "+str(self.seed))
        
        
        if(tileType == "generic"):
            xyTuples = []
            for m in range(0,maxMtns):
                '''decide if we will randomly generate this mountain or not'''
                if(random.random() > mtnProb):
                    continue
                mx = self.x*self.tDim + random.randint(0,self.tDim-1)
                my = self.y*self.tDim + random.randint(0,self.tDim-1)
                mh = random.randint(0,PARAM_MTN_MAX_HEIGHT)
                
                '''skip duplicate x,y peak locations'''
                if((mx,my) in xyTuples):
                    continue

                self.mtnList.append(mtn.Mtn(mx, my, mh, str(random.randint(0,PARAM_MAX_SEED_VAL))))
            
            '''river info for this tile (all "individual" rivers are part of a single per-tile rivers object'''
            self.rivers.append(rivers.Rivers((self.x*self.tDim,self.y*self.tDim), riverInfo,\
                               str(random.randint(0,PARAM_MAX_SEED_VAL))))
        
        elif (tileType == "beach"):
            self.beach = beach.Beach((self.x*self.tDim,self.y*self.tDim), str(random.randint(0,PARAM_MAX_SEED_VAL)))
            self.rivers.append(rivers.Rivers((self.x*self.tDim,self.y*self.tDim), riverInfo,\
                               str(random.randint(0,PARAM_MAX_SEED_VAL))))
            
    def getClosestXY(self, thisX, thisY, tileX, tileY):
        ''' Get closest x,y location in tileX, tileY to input point thisX, thisY  '''
        
        x = thisX
        if(self.x > tileX):
            x = tileX*self.tDim+self.tDim-1
        elif(self.x < tileX):
            x = tileX*self.tDim  
        
        y = thisY
        if(self.y > tileY):
            y = tileY*self.tDim+self.tDim-1
        elif(self.y < tileY):
            y = tileY*self.tDim    
            
        if(PARAM_DEBUG_EN_MTNS):
            print("("+str(thisX)+","+str(thisY)+") closest pt in tile ("+str(tileX)+","+str(tileY)+") = "+str(x+y))    
            
        return [x,y]
        
    def preDrawMtnReport(self):
        '''Report which tiles the mtns in this tile extend into (including this tile itself)'''
        mtnExport = {}
        for m in range(0,len(self.mtnList)):
            thisMtn = self.mtnList[m]
            cenX = thisMtn.x
            cenY = thisMtn.y
            sx = thisMtn.sx #x slope
            sy = thisMtn.sy #y slope
            '''Figure out maximum range of this mtn based on it's hight and the global max slope possible'''
            radius = int(thisMtn.h/PARAM_MTN_MAX_SLOPE)+1   #+1 to prevent rounding/division problems
            
            for tileX in range(int((cenX-radius)/self.tDim), int((cenX+radius)/self.tDim+1)):
                for tileY in range(int((cenY-radius)/self.tDim), int((cenY+radius)/self.tDim+1)):
                    if(tileX >= 0 and tileX < PARAM_MAP_SIZE_X and tileY >= 0 and tileY < PARAM_MAP_SIZE_Y):
                        closestXY = self.getClosestXY(cenX, cenY, tileX, tileY)
                        if(thisMtn.altAtXY(closestXY[0],closestXY[1]) > 0):
                            if((tileX) not in mtnExport):
                                mtnExport[tileX] = {}
                            if((tileY) not in mtnExport[tileX]):
                                mtnExport[tileX][tileY] = []
                            mtnExport[tileX][tileY].append(thisMtn)
                            
                            if(PARAM_DEBUG_EN_MTNS):
                                print("Adding Mtn to tile ("+str(tileX)+","+str(tileY)+"): peak ("+\
                                        str(cenX)+","+str(cenY)+","+str(radius)+")") 
        return mtnExport

    def preDrawRiverReport(self, entryPtsXY, mtnList):
        '''Create dictionary of river exit points, which will be used as input points to other tiles'''
        
        if(PARAM_DEBUG_EN_RIVERS):
            print("predraw river report for tile ("+str(self.x)+","+str(self.y)+")")
        
        riverExport = {}
        for r in self.rivers:
            r.preDrawRiverReport(entryPtsXY, mtnList)
            for xPt in r.exitPts:
                for yPt in r.exitPts[xPt]:
                    #TODO: only handling river propagation downyards (higher y val) right now, extend to other tile boundaries
                    if(yPt != (self.y+1)*self.tDim):
                        continue
                    ''' add the x,y pt if it isn't already in the export list'''
                    if (xPt not in riverExport):
                        riverExport[xPt] = []
                    if (yPt not in riverExport[xPt]):
                        riverExport[xPt].append(yPt)
                        
                        if(PARAM_DEBUG_EN_RIVERS):
                            print("Adding river exit pt ("+str(xPt)+","+str(yPt)+")")
            
        if(PARAM_DEBUG_EN_RIVERS):
            print("riverExport = "+str(riverExport))
            
        return riverExport
        
    def preDrawBeachReport(self, inputXY):
        self.beach.preDrawBeachReport(inputXY)
        return self.beach.exitPtXY

    def drawXY(self, x, y, drawMtns):
        '''determine the string to write ("draw") for the given map X,Y location'''
        
        baseStr = " "*(PARAM_MAP_PRINT_WIDTH-1)
        outStr = baseStr + " "
        
        if(self.tileType == "ocean"):   #ocean tiles are only water
            outStr = baseStr + "W"
            
        elif(self.tileType == "beach"):
            if (y > self.beach.xyPts[x]):
                outStr = baseStr + "W"
            else:
                outStr = baseStr +" "
                for r in self.rivers:
                    if(x in r.xyPts):
                        if(y in r.xyPts[x]):
                            outStr = baseStr + "*"
            
        elif(self.tileType == "generic"):
            altTot = 0
            for m in drawMtns:                
                altPk = m.altAtXY(x,y)
                if(altPk > 0):
                    altTot += altPk
        
            if(altTot > 0):
                altStr = str(altTot)
                if(len(altStr) < PARAM_MAP_PRINT_WIDTH):
                    outStr = " "*(PARAM_MAP_PRINT_WIDTH-len(altStr))+altStr[-len(altStr):]
                elif(len(altStr) > PARAM_MAP_PRINT_WIDTH):
                    outStr = altStr[-PARAM_MAP_PRINT_WIDTH:]
        
            for r in self.rivers:
                if(x in r.xyPts):
                    if(y in r.xyPts[x]):
                        outStr = baseStr + "*" 
        
        if(PARAM_DEBUG_EN_GENERAL):
            print(str((x,y))+" tileType "+str(self.tileType)+" outStr '"+outStr+"'")
        
        return outStr
        
        
    def draw(self, drawMtns):
        '''Currently "drawing" the tile just means print it out in glorious ASCII'''
        
        if(PARAM_DEBUG_EN_GENERAL):
            print("Tile ("+str(self.x)+","+str(self.y)+"), seed "+str(self.seed))
        
        for y in range(self.y*self.tDim,self.y*self.tDim+self.tDim):
            for x in range(self.x*self.tDim,self.x*self.tDim+self.tDim):
                xyStr = self.drawXY(x,y,drawMtns)
                print(xyStr, end="")
                
            print("\n")
            
            
                    