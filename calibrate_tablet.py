
from psychopy import core, visual, gui, data, event
# from psychopy.tools.coordinatetools import pol2cart, cart2pol
# from psychopy.tools.mathtools import distance
# import numpy as np
# import random, datetime, os
# from glob import glob
# from itertools import compress

from psychopy.hardware import keyboard
from pyglet.window import key

# import sys, os

import pandas as pd

import time


def calibrateTablet(screen=0, viewScale=None):

    data = {'x': [], 'y': [], 't': []}

    # win = psychopy.visual.Window(size=(800, 600), 
    #                             pos=None, 
    #                             color=(0, 0, 0), 
    #                             colorSpace='rgb', 
    #                             backgroundImage=None, 
    #                             backgroundFit='cover', 
    #                             rgb=None, 
    #                             dkl=None, 
    #                             lms=None, 
    #                             fullscr=None, 
    #                             allowGUI=None, 
    #                             monitor=None, 
    #                             bitsMode=None, 
    #                             winType=None, 
    #                             units=None, 
    #                             gamma=None, 
    #                             blendMode='avg', 
    #                             screen=0, 
    #                             viewScale=None, 
    #                             viewPos=None, 
    #                             viewOri=0.0, 
    #                             waitBlanking=True, 
    #                             allowStencil=False, 
    #                             multiSample=False, 
    #                             numSamples=2, 
    #                             stereo=False, 
    #                             name='window1', 
    #                             title='PsychoPy', 
    #                             checkTiming=True, 
    #                             useFBO=False, 
    #                             useRetina=True, 
    #                             autoLog=True, 
    #                             gammaErrorPolicy='raise', 
    #                             bpc=(8, 8, 8), 
    #                             depthBits=8, 
    #                             stencilBits=8, 
    #                             backendConf=None, 
    #                             infoMsg=None)

    # win = visual.Window(
    #                         color=(0, 0, 0), 
    #                         fullscr=True, 
    #                         # monitor=mon, 
    #                         units='pix', 
    #                         screen=screen, 
    #                         viewScale=viewScale
    #                     )

    myMonitor = monitors.Monitor(name='temp',
                                 distance=100,
                                 width=43.3)
    myMonitor.setSizePix([1680,1050])

    win = visual.Window( size=[1680,1050], 
                                fullscr=True, 
                                units='cm', 
                                waitBlanking=False, 
                                viewScale=[1,-1], 
                                color=[-1,-1,-1], 
                                screen=1, 
                                monitor=myMonitor)

    # don't need this:
    xPPC = 1680/43.3
    yPPC = 1050/27.1


    # myMouse = event.Mouse(visible=False, win=win)



        # set up 'mouse' object to track reaches:
    class myMouse:

        # TABLET:
        # "size_px"    : [1680, 1050],
        # "size_cm"    : [31.1, 21.6],
        # "mapping"    : 'relative',     <-   this is not true right now

        # MONITOR:
        #   "size_px"         : [1680, 1050], 
        #   "size_cm"         : [43.3, 27.1],
        #   "viewscale"       : [1,-1],

        def __init__(self, monitor_size=[43.3, 27.1], tablet_size=[31.1, 21.6]):
            # we use a psychopy mouse object
            self.psyMouse = event.Mouse(visible = False, newPos = None, win = cfg['win'])
            self.xfactor = 43.3/31.1
            self.yfactor = 27.1/21.6

            print([self.xfactor, self.yfactor])

        def getPos(self):
            # but in addition to the position, we also return the time the position was asked for
            [X,Y] = self.psyMouse.getPos()
            st = time.time()
            X = X / self.xfactor # scale to centimeters ?
            Y = Y / self.yfactor # scale to centimeters ?

            return [X,Y,st]

    scaledMouse = myMouse(monitor_size=[43.3, 27.1], tablet_size=[31.1, 21.6])

    cursor = visual.Circle( win, 
                            radius=5, 
                            edges=96, 
                            fillColor=None, 
                            lineColor='blue', 
                            lineWidth=2,
                            pos=(0, 0))

    instructions = visual.TextStim(win, text="SPACE: toggle recording\n(blue=off; red=on)\n\nQ: quit.", pos=(0, 0), color='white', height=30)


    calibrating = True
    recording = False

    while calibrating:
        # Draw a fixation cross
        
        instructions.draw()

        cursor.pos = myMouse.getPos()
        cursor.draw()

        if recording:
            pos = scaledMouse.getPos()
            data['x'].append(pos[0])
            data['y'].append(pos[1])
            data['t'].append(pos[2])

        win.flip()
        
        # k = event.getKeys(['left', 'right', 'up', 'down' ,'escape', 'space', '1', 'q'])
        k = event.getKeys(['space', 'q'])
        if k:
            if k[0] in ['q']:
                calibrating = False
            if k[0] in ['space']:
                if recording:
                    recording = False
                    cursor.lineColor = 'blue'
                else:
                    recording = True
                    cursor.lineColor = 'red'
            

    

    win.close()


    pd.DataFrame(data).to_csv('tablet_calibration_data.csv', index=False)


if __name__ == "__main__": 
    calibrateTablet()  