#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Based on templates originally (C) Jose F. Maldonado 2013, 
# retrieved from http://registry.gimp.org/node/28124
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#    - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation and/or 
#    other materials provided with the distribution.
#    - Neither the name of the author nor the names of its contributors may be used 
#    to endorse or promote products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.
#
# -------------------------------------------------------------------------------------
#
# This file is a basic example of a Python plug-in for GIMP.
#
# It can be executed by selecting the menu option: 'Filters/Test/Discolour layer v1'
# or by writing the following lines in the Python console (that can be opened with the
# menu option 'Filters/Python-Fu/Console'):
# >>> image = gimp.image_list()[0]
# >>> layer = image.layers[0]
# >>> gimp.pdb.python_fu_test_draw_map_v1(image, layer)

from gimpfu import *

def draw_map_v1(img, layer) :
    ''' Draw map file produced by mountains project (https://github.com/amcauley/Mountains) as a proper
    image instead of a text file.
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    
    filename = "C:\\test\\mapOutput.txt"
    print("Attempting to open " + filename)
    f = open(filename,'r')
    print("Success")
    
    # Indicates that the process has started.
    gimp.progress_init("Drawing map " + layer.name + "...")

    # Set up an undo group, so the operation will be undone in one step.
    pdb.gimp_image_undo_group_start(img)

    '''Consume first two lines of map, which contain the header info'''
    mapLine = f.readline()
    mapLine = f.readline()
    
    # Iterate over all the pixels and convert them to gray.
    try:
        for y in range(layer.height):
            # Update the progress bar.
            gimp.progress_update(float(y) / float(layer.height))

            mapLine = f.readline()
            print("mapLine for line "+str(y)+": "+mapLine)
            
            for x in range(layer.width):
                # Get the pixel and verify that is an RGB value.
                pixel = layer.get_pixel(x,y)

                #print("Existing val @ "+str((x,y))+" is "+str(pixel))

                # Currently maps are using 3 chars per "pixel" - this should probably be an 
                # input or read directly from Mountains param file.
                xyStr = mapLine[1+3*x:1+3*(x+1)]
            
                if(len(pixel) >= 3):
                    # Determine pixel color based on map input
                    print("Pixel "+str((x,y))+" map value: "+xyStr)
                    # First remove whitespace from both ends
                    xyStr = xyStr.strip()
                    pixValR = 40
                    pixValG = 100 # Default value is green
                    pixValB = 20
                    if(xyStr.isdigit()):
                        grayVal = 30+10*int(xyStr) # Draw gray
                        if (grayVal > 200):
                            grayVal = 200
                        pixValR = pixValG = pixValB = grayVal 
                    elif(xyStr == '*'): # River
                        pixValR = pixValG = 0
                        pixValB = 255
                    elif(xyStr == 'W'): # Ocean
                        pixValR = 20
                        pixValG = 85
                        pixValB = 110
                    # Create a new tuple representing the new color, inherit alpha channel (if any)
                    newColor = (pixValR,pixValG,pixValB) + pixel[3:]
                    layer.set_pixel(x,y, newColor)
        
        # Update the layer.
        layer.update(0, 0, layer.width, layer.height)

    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
    
    # Close the undo group.
    pdb.gimp_image_undo_group_end(img)
    
    # End progress.
    pdb.gimp_progress_end()

'''Disable the rest of this file (register and main) for in-console GIMP debugging, then, in the python-fu console:
    import sys
    sys.path=[gimp.directory+'/plug-ins']+sys.path
    import test_draw_map_v1
    test_draw_map_v1.draw_map_v1(gimp.image_list()[0],gimp.image_list()[0].active_layer)
    
    To reload module: reload(test_draw_map_v1)
'''
 
'''register(
    "python_fu_test_draw_map_v1",
    "Draw Map v1",
    "Convert Mountains project text output into a proper image",
    "AAGM",
    "Open source (BSD 3-clause license)",
    "2014",
    "<Image>/Filters/Test/Draw Map v1",
    "RGB, RGB*",
    [],
    [],
    draw_map_v1)

main()
'''