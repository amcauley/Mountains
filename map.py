import random
from params import *
import tile

class Map:
    '''The map class manages sets of tiles as the top level class '''
    def __init__(self, nx, ny, seed = None):
        self.nx = nx #number of tiles in x dimension
        self.ny = ny #number of tiles in y dimension
        
        #tile (x,y) will be indexed as self.tiles[x][y]
        self.tiles = []
        
        if(seed == None):
            self.seed = str(random.randint(0,PARAM_MAX_SEED_VAL))
        else:
            self.seed = seed
        
        for x in range(0,nx):
            self.tiles.append([])
            for y in range(0,ny):
                random.seed(int(self.seed)+nx*y+x)
                
                '''determine max number of mtns, rivers, etc. for this tile based on its global location'''
                if y >= 70*self.ny/100:      #lower 30% of map
                    maxMtns = 0
                    maxRivers = 0
                elif y >= 30*self.ny/100:    #middle of map
                    maxMtns = 1
                    maxRivers = 1
                else:                        #top 30%
                    maxMtns = 2
                    maxRivers = 1
                
                if(y == self.ny-1):
                    tileType = "ocean"
                elif(y == self.ny-2):
                    tileType = "beach"
                else:    
                    tileType = "generic"
                
                '''create the tile'''
                if(PARAM_DEBUG_EN_GENERAL):
                    print("Tile "+str((x,y))+", maxMtns "+str(maxMtns)+", maxRivers "+str(maxRivers))
                self.tiles[x].append(tile.Tile(x,y,tileType,maxMtns,maxRivers,str(random.randint(0,PARAM_MAX_SEED_VAL))))
                
        self.mtnsPerTile = {}        
                
    def preDrawMtns(self):
        '''Iterate through tiles and generate any pre-draw info needed for mtns that need to be exported to 
        other tiles (due to extending into their region)'''
        self.mtnsPerTile = {}
        tileMtnsPerTile = {}
        
        for y in range(0,self.ny):
            for x in range(0,self.nx):
                '''predraw mtns'''
                
                if(self.tiles[x][y].tileType == "ocean"):
                    continue
                
                tileMtnsPerTile = self.tiles[x][y].preDrawMtnReport()
                            
                for tileX in tileMtnsPerTile:
                    if(tileX not in self.mtnsPerTile):
                        self.mtnsPerTile[tileX] = {}
                    for tileY in tileMtnsPerTile[tileX]:
                        if(tileY not in self.mtnsPerTile[tileX]):
                                self.mtnsPerTile[tileX][tileY] = []
                        self.mtnsPerTile[tileX][tileY].extend(tileMtnsPerTile[tileX][tileY])
                        
                        if(PARAM_DEBUG_EN_MTNS):
                            for mtnReport in tileMtnsPerTile[tileX][tileY]:
                                print("Adding MtnReport to Map tile ("+str(tileX)+","+str(tileY)+"): peak ("+\
                                        str(mtnReport.x)+","+str(mtnReport.y)+","+str(mtnReport.h)+")") 

    def preDrawRivers(self):                                    
        '''Iterate through tiles and generate any pre-draw river info'''
        riverEntryPerTile = {}
        
        for y in range(0,self.ny):
            for x in range(0,self.nx):
                '''predraw rivers'''
                
                if(self.tiles[x][y].tileType == "ocean"):
                    continue
                
                entryPtsXY = []
                if(x in riverEntryPerTile):
                    if(y in riverEntryPerTile[x]):
                        entryPtsXY = riverEntryPerTile[x][y]
                mtnsInput = []
                if(x in self.mtnsPerTile):
                    if(y in self.mtnsPerTile[x]):
                        mtnsInput = self.mtnsPerTile[x][y]
                tileRiversPerTile = self.tiles[x][y].preDrawRiverReport(entryPtsXY, mtnsInput)

                ''' add this tile's river output to the map-wide list, will be used as input for other river tiles'''
                #TODO: generalize this for rivers extending to adjacent, not just below tiles
                for exitX in tileRiversPerTile:
                    for exitY in tileRiversPerTile[exitX]:
                        if(exitY == (y+1)*self.tiles[0][0].tDim):
                            if x not in riverEntryPerTile:
                                riverEntryPerTile[x] = {}
                            if y+1 not in riverEntryPerTile[x]:
                                riverEntryPerTile[x][y+1] = []
                            riverEntryPerTile[x][y+1].append((exitX,exitY))

    def preDrawBeaches(self):
        '''pass beach info between tiles. Currently only supports a single horizontal row of beach tiles, will add more 
        support later. '''
        for tileY in range(0,self.ny):
            if(self.tiles[0][tileY].tileType == "beach"):
                inputXY = [0,tileY*self.tiles[0][0].tDim+random.randint(0,self.tiles[0][0].tDim-1)]
                for tileX in range(0,self.nx):
                    thisBeach = self.tiles[tileX][tileY]
                    assert thisBeach.tileType == "beach"
                    if(PARAM_DEBUG_EN_BEACHES):
                        print("beach xy input to tile "+str((tileX,tileY))+": "+str(inputXY))
                    inputXY = thisBeach.preDrawBeachReport(inputXY)
                        
                            
    def drawMap(self, filename):
        '''draw the entire map - output to file'''
    
        '''No Need for now since testMap.py will call these'''  
        #self.preDrawMtns()
        #self.preDrawBeaches()
        #self.preDrawRivers()       
    
        f = open(filename,'w')
    
        if(PARAM_DEBUG_EN_MTNS):
            print("Printing map to "+filename)
    
        f.write(str(self.nx*self.tiles[0][0].tDim)+" x "+str(self.ny*self.tiles[0][0].tDim))
        f.write(", map seed "+str(self.seed))
        f.write('\n'+'-'*(self.nx*self.tiles[0][0].tDim*PARAM_MAP_PRINT_WIDTH+2)+'\n')
    
        for tileY in range(0,self.ny):
            for y in range(tileY*self.tiles[0][0].tDim,tileY*self.tiles[0][0].tDim+self.tiles[0][0].tDim):
                f.write('|')    
                for tileX in range(0,self.nx):

                    if(PARAM_DEBUG_EN_MTNS):
                        print("printing row "+str(y)+" of tile ("+str(tileX)+","+str(tileY)+")")
                
                    drawMtns = []
                    if(tileX in self.mtnsPerTile):
                        if(tileY in self.mtnsPerTile[tileX]):
                            drawMtns = self.mtnsPerTile[tileX][tileY]
                
                    for x in range(tileX*self.tiles[0][0].tDim,tileX*self.tiles[0][0].tDim+self.tiles[0][0].tDim):
                        xyStr = self.tiles[tileX][tileY].drawXY(x,y,drawMtns)
                        f.write(xyStr)
                        
                f.write('|\n')        
        
        f.write('-'*(self.nx*self.tiles[0][0].tDim*PARAM_MAP_PRINT_WIDTH+2))
        f.close()
    
    
    
    