
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

    win = visual.Window(
                            color=(0, 0, 0), 
                            fullscr=True, 
                            # monitor=mon, 
                            units='pix', 
                            screen=screen, 
                            viewScale=viewScale
                        )

    myMouse = event.Mouse(visible=False, win=win)

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
            data['x'].append(myMouse.getPos()[0])
            data['y'].append(myMouse.getPos()[1])
            data['t'].append(core.getTime())    

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