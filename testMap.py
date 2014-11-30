from params import *
import tile
import map

def testMap():
    x = 0
    y = 0
    testMap = map.Map(PARAM_MAP_SIZE_X, PARAM_MAP_SIZE_Y, PARAM_MAP_SEED)
    
    cmd = 0
    
    '''
    NOTE: Following graphics x,y convention:
       +----------------->X
       |
       |
       |
       v Y
    '''
       
    testMap.preDrawMtns()
    testMap.preDrawBeaches()
    testMap.preDrawRivers()
      
    while(True):
        testTile = testMap.tiles[x][y]
        
        if(PARAM_DEBUG_EN_MTNS):
            for m in testTile.mtnList:
                print("Local mtn @ local coords ("+str(m.x)+","+str(m.y)+","+str(m.h)+")")
        
        tileMtns = []
        if(x in testMap.mtnsPerTile):
            if(y in testMap.mtnsPerTile[x]):
                tileMtns = testMap.mtnsPerTile[x][y]
                if(PARAM_DEBUG_EN_MTNS):
                    for m in testMap.mtnsPerTile[x][y]:
                        print("Mtn found:("+str(m.x)+","+str(m.y)+","+str(m.h)+")")                                            
                        
        testTile.draw(tileMtns)
        
        cmd = input("w/a/s/d or q: ")
        if(cmd == 'w'):
            if(y > 0):
                y-=1
            else:
                print("Map Bndry")
        elif(cmd == 'a'):
            if(x > 0):
                x-=1
            else:
                print("Map Bndry")
        elif(cmd == 's'):
            if(y < testMap.ny-1):
                y+=1
            else:
                print("Map Bndry")
        elif(cmd == 'd'):
            if(x < testMap.nx-1):
                x+=1
            else:
                print("Map Bndry")        
        elif(cmd == 'q'):
            break
        else:
            print("Invalid Cmd")
    
    '''print out the map to default output file after quitting the loop'''
    testMap.drawMap("C:\\test\\mapOutput.txt")
        
    
if __name__ == "__main__":
        testMap()