import random
from params import *
import mtn
import rivers

class Tile:
    '''Tile class to combine mountains, rivers, etc.'''
    
    tDim = PARAM_TILE_SIZE #size of tiles is a property of the class
    
    def __init__(self, x, y, tileType, maxMtns, maxRivers, seed = None):
        self.mtnList = [];
        self.rivers = []
        
        self.x = x
        self.y = y
        self.minH = 0
        self.maxH = 10
        
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
            for m in range(0,random.randint(0,maxMtns)):
                mx = self.x*self.tDim + random.randint(0,self.tDim-1)
                my = self.y*self.tDim + random.randint(0,self.tDim-1)
                mh = random.randint(0,PARAM_MTN_MAX_HEIGHT)
                
                '''skip duplicate x,y peak locations'''
                if((mx,my) in xyTuples):
                    continue

                self.mtnList.append(mtn.Mtn(mx, my, mh, str(random.randint(0,PARAM_MAX_SEED_VAL))))
            
            '''river info for this tile (all "individual" rivers are part of a single per-tile rivers object'''
            self.rivers.append(rivers.Rivers((self.x*self.tDim,self.y*self.tDim), random.randint(0,maxRivers),\
                               str(random.randint(0,PARAM_MAX_SEED_VAL))))
        
        '''nothing special for ocean type yet'''
        #else:   #tileType = "ocean"
            
            
    def point2TileDist2(self, thisX, thisY, tileX, tileY):
        ''' compute distance squared between this tile's global (x,y) and the closest point
        on tile (tileX, tileY) '''
        
        xDist2 = 0
        if(self.x > tileX):
            xDist2 = (thisX - (tileX*self.tDim+self.tDim-1))**2
        elif(self.x < tileX):
            xDist2 = (thisX - tileX*self.tDim)**2    
        
        yDist2 = 0
        if(self.y > tileY):
            yDist2 = (thisY - (tileY*self.tDim+self.tDim-1))**2
        elif(self.y < tileY):
            yDist2 = (thisY - tileY*self.tDim)**2    
            
        if(PARAM_DEBUG_EN_MTNS):
            print("("+str(thisX)+","+str(thisY)+") dist2 to tile ("+str(tileX)+","+str(tileY)+") = "+str(xDist2+yDist2))    
            
        return xDist2 + yDist2
        
    def preDrawMtnReport(self):
        '''Report which tiles the mtns in this tile extend into (including this tile itself)'''
        mtnExport = {}
        for m in range(0,len(self.mtnList)):
            cenX = self.mtnList[m].x
            cenY = self.mtnList[m].y
            radius = self.mtnList[m].h
            
            #TODO: Replace hard-coded tile/map size with a constant
            for tileX in range(int((cenX-radius)/self.tDim), int((cenX+radius)/self.tDim+1)):
                for tileY in range(int((cenY-radius)/self.tDim), int((cenY+radius)/self.tDim+1)):
                    if(tileX >= 0 and tileX < PARAM_MAP_SIZE_X and tileY >= 0 and tileY < PARAM_MAP_SIZE_Y):
                        if(self.point2TileDist2(cenX, cenY, tileX, tileY) < radius**2):
                            if((tileX) not in mtnExport):
                                mtnExport[tileX] = {}
                            if((tileY) not in mtnExport[tileX]):
                                mtnExport[tileX][tileY] = []
                            mtnExport[tileX][tileY].append(mtn.Mtn(cenX, cenY, radius))
                            
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
        
        
    def draw(self, drawMtns):
        '''Currently "drawing" the tile just means print it out in glorious ASCII'''
    
        if(PARAM_DEBUG_EN_MTNS):
            print("Tile ("+str(self.x)+","+str(self.y)+"), seed "+str(self.seed))
        
        for y in range(self.y*self.tDim,self.y*self.tDim+self.tDim):
            for x in range(self.x*self.tDim,self.x*self.tDim+self.tDim):
            
                if(self.tileType == "ocean"):
                    altStr = " "*(PARAM_MAP_PRINT_WIDTH-1)+"W"
                    
                else:    
                    altTot = 0
                    for m in drawMtns:                
                        altPk = m.altAtXY(x,y)
                        if(altPk > 0):
                            altTot += altPk
                        
                    altStr = " "*PARAM_MAP_PRINT_WIDTH
                    if(altTot > 0):
                        altStr = str(altTot)
                        if(len(altStr) < PARAM_MAP_PRINT_WIDTH):
                            altStr = " "*(PARAM_MAP_PRINT_WIDTH-len(altStr))+altStr[-len(altStr):]
                        elif(len(altStr) > PARAM_MAP_PRINT_WIDTH):
                            altStr = altStr[-PARAM_MAP_PRINT_WIDTH:]
                            
                    '''rivers take precedence over mtns for initial testing'''
                    #TODO: address case of multiple rivers per tile
                    for r in self.rivers:
                        if(x in r.xyPts):
                            if(y in r.xyPts[x]):
                                altStr = " "*(PARAM_MAP_PRINT_WIDTH-1)+"*"
                        
                print(altStr, end="")
                
            print("\n")
                    