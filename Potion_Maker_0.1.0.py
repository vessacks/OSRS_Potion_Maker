#Potion maker

from doctest import script_from_examples
from msilib.schema import Feature
import cv2 as cv
from cv2 import threshold
from cv2 import _InputArray_STD_BOOL_VECTOR
import numpy as np
import os
from windmouse import wind_mouse
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action

#initialize the window capture class
wincap = WindowCapture('RuneLite - Vessacks')


#initialize vision class
herb_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\herb.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_COLOR)
vial_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\vial.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_COLOR)
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_COLOR)
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\in_bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_COLOR)
bank_dump_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\bank_dump.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_COLOR)


#initialize action class
herb_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\herb.png')
vial_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\vial.png') 
bank_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\bank.png') 
bank_dump_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\potion maker\\image library\\bank_dump.png') 

#notes
#1. take new bank_vision image
#2. make sure the herb vision and vial vision are the herbs and vials you want
#3. make sure your bank tab contains the herb and vial you want, and that they are not the tab thumbnail image
#4. make sure your bank withdraw x is set to 14 and your withdraw is set to x

#parameters
BANK_THRESHOLD = .85
IN_BANK_THRESHOLD = .9
OUT_BANK_THRESHOLD = .85
BANK_DUMP_THRESHOLD = .9
HERB_THRESHOLD = .9
VIAL_THRESHOLD = .9

#some functions
def speed():
    speed = np.random.normal(.7,.3)
    while speed > .85 or speed < .6:
        speed = np.random.normal(.75,.08)
    return speed


def tick_dropper(odds=70):
    if np.random.randint(0,odds) == 1:
        
        drop = np.random.uniform(.6,4)
        print('tick dropper! sleeping %s' %drop)
        time.sleep(drop)
    return

def wait():
    wait = (.1 + abs(np.random.normal(0,.05)))
    return wait

s_or_c = input('please enter \'s\' to run in seconds, or \'c\' to run for counts and press enter | ')

if s_or_c == 'c':
    stop_count = input('please enter the number of counts to run for | ')

elif s_or_c == 's':
    stop_seconds = input('please enter the number of seconds to run for | ')

else:
    print('somethings wrong with s_or_c. exitting')
    exit()

#potion loop
count = 0
start_time = time.time()
while True:
    #look for the bank
    print('looking for bank...')
    loop_start = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        bank_allPoints, bank_bestPoint, bank_confidence = bank_vision.find(screenshot, threshold = BANK_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        if bank_confidence > BANK_THRESHOLD:
            print('found bank | confidence %s | clicking and breaking bank search loop' %round(bank_confidence,3))
            bank_screenpoint = wincap.get_screen_position(bank_bestPoint)
            tick_dropper()
            bank_clickpoint = bank_action.click(bank_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
            break
        if time.time() - loop_start > 35:
            print('PROBLEM(!) bank searched %ss, found nothing | Exit...' %(time.time() - loop_start))
            exit()


    #check we're in bank
    print('checking for in_bank')
    loop_start = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        in_bank_allPoints, in_bank_bestPoint, in_bank_confidence = in_bank_vision.find(screenshot, threshold = IN_BANK_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        if in_bank_confidence > IN_BANK_THRESHOLD:
            print('found in_bank | confidence %s | breaking in_bank search loop' %round(in_bank_confidence,3))
            break
        if time.time() - loop_start > 35:
            print('PROBLEM(!) in_bank searched %ss, found nothing | Exit...' %(time.time() - loop_start))   
            exit()

    #look for bank dump and click
    print('looking for bank_dump')
    loop_start = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        bank_dump_allPoints, bank_dump_bestPoint, bank_dump_confidence = bank_dump_vision.find(screenshot, threshold = BANK_DUMP_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        if bank_dump_confidence > BANK_DUMP_THRESHOLD:
            print('found bank_dump | confidence %s | clicking and breaking bank_dump search loop' %round(bank_dump_confidence,3))
            bank_dump_screenpoint = wincap.get_screen_position(bank_dump_bestPoint)
            tick_dropper()
            bank_dump_clickpoint = bank_dump_action.click(bank_dump_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
            break
        if time.time() - loop_start > 35:
            print('PROBLEM(!) bank_dump searched %ss, found nothing | Exit...' %(time.time() - loop_start))
            exit()

    #decide whether to grab vialions or herbs first
    vial_or_herb = np.random.randint(0,2)
    if vial_or_herb == 1:
        print('rolled a 1, getting herbs first')
        print('looking for herb')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            herb_allPoints, herb_bestPoint, herb_confidence = herb_vision.find(screenshot, threshold = HERB_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if herb_confidence > HERB_THRESHOLD:
                print('found herb | confidence %s | clicking and breaking herb search loop' %round(herb_confidence,3))
                herb_screenpoint = wincap.get_screen_position(herb_bestPoint)
                tick_dropper()
                herb_clickpoint = herb_action.click(herb_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) herb searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()

        print('looking for vial')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            vial_allPoints, vial_bestPoint, vial_confidence = vial_vision.find(screenshot, threshold = VIAL_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if vial_confidence > VIAL_THRESHOLD:
                print('found vial | confidence %s | clicking and breaking vial search loop' %round(vial_confidence,3))
                vial_screenpoint = wincap.get_screen_position(vial_bestPoint)
                tick_dropper()
                vial_clickpoint = vial_action.click(vial_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) vial searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()


    if vial_or_herb == 0:
        print('rolled a 0, getting vials first')
        
        print('looking for vial')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            vial_allPoints, vial_bestPoint, vial_confidence = vial_vision.find(screenshot, threshold = VIAL_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if vial_confidence > VIAL_THRESHOLD:
                print('found vial | confidence %s | clicking and breaking vial search loop' %round(vial_confidence,3))
                vial_screenpoint = wincap.get_screen_position(vial_bestPoint)
                tick_dropper()
                vial_clickpoint = vial_action.click(vial_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) vial searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()

        print('looking for herb')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            herb_allPoints, herb_bestPoint, herb_confidence = herb_vision.find(screenshot, threshold = HERB_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if herb_confidence > HERB_THRESHOLD:
                print('found herb | confidence %s | clicking and breaking herb search loop' %round(herb_confidence,3))
                herb_screenpoint = wincap.get_screen_position(herb_bestPoint)
                tick_dropper()
                herb_clickpoint = herb_action.click(herb_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) herb searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()


    if vial_or_herb != 1 and vial_or_herb != 0:
        print('the vial or herb roller is fucked up. do something about it. exitting')
        exit()

    #escape bank
    print('exiting bank w. esc')
    tick_dropper()
    pyautogui.keyDown('esc')
    time.sleep(.15 + abs(np.random.normal(.1,.05)))
    tick_dropper()
    pyautogui.keyUp('esc')
    time.sleep(.15 + abs(np.random.normal(.1,.05)))

    #wait to be outside bank
    print('checking for NOT in_bank')
    loop_start = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        in_bank_allPoints, in_bank_bestPoint, in_bank_confidence = in_bank_vision.find(screenshot, threshold = OUT_BANK_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        if in_bank_confidence < OUT_BANK_THRESHOLD:
            print('NOT in_bank | confidence %s | breaking OUT_bank search loop' %round(in_bank_confidence,3))
            break
        if time.time() - loop_start > 35:
            print('PROBLEM(!) NOT in_bank searched %ss, found NOT nothing | Exit...' %(time.time() - loop_start))   
            exit()
    
    #click the herbs and vial to use
    if vial_or_herb == 1:
        print('Potmaking | rolled a 1 earlier, clicking herbs first')
        print('looking for herb')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            herb_allPoints, herb_bestPoint, herb_confidence = herb_vision.find(screenshot, threshold = HERB_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if herb_confidence > HERB_THRESHOLD:
                print('found herb | confidence %s | clicking and breaking herb search loop' %round(herb_confidence,3))
                herb_screenpoint = wincap.get_screen_position(herb_bestPoint)
                tick_dropper()
                herb_clickpoint = herb_action.click(herb_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) herb searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()

        print('looking for vial')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            vial_allPoints, vial_bestPoint, vial_confidence = vial_vision.find(screenshot, threshold = VIAL_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if vial_confidence > VIAL_THRESHOLD:
                print('found vial | confidence %s | clicking and breaking vial search loop' %round(vial_confidence,3))
                vial_screenpoint = wincap.get_screen_position(vial_bestPoint)
                tick_dropper()
                vial_clickpoint = vial_action.click(vial_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) vial searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()
    
    if vial_or_herb == 0:
        print('Potmaking | rolled a 0 earlier, getting vials first')
        
        print('looking for vial')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            vial_allPoints, vial_bestPoint, vial_confidence = vial_vision.find(screenshot, threshold = VIAL_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if vial_confidence > VIAL_THRESHOLD:
                print('found vial | confidence %s | clicking and breaking vial search loop' %round(vial_confidence,3))
                vial_screenpoint = wincap.get_screen_position(vial_bestPoint)
                tick_dropper()
                vial_clickpoint = vial_action.click(vial_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) vial searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()

        print('looking for herb')
        loop_start = time.time()
        while True:
            screenshot = wincap.get_screenshot()
            herb_allPoints, herb_bestPoint, herb_confidence = herb_vision.find(screenshot, threshold = HERB_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()
            if herb_confidence > HERB_THRESHOLD:
                print('found herb | confidence %s | clicking and breaking herb search loop' %round(herb_confidence,3))
                herb_screenpoint = wincap.get_screen_position(herb_bestPoint)
                tick_dropper()
                herb_clickpoint = herb_action.click(herb_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
                break
            if time.time() - loop_start > 35:
                print('PROBLEM(!) herb searched %ss, found nothing | Exit...' %(time.time() - loop_start))
                exit()

    time.sleep(.15+ abs(np.random.normal(0,.07)))

    #press space to initiate pot make
    print('pressing space to initiate potmaking')
    tick_dropper()
    pyautogui.keyDown('space')
    time.sleep(.15 + abs(np.random.normal(.1,.05)))
    tick_dropper()
    pyautogui.keyUp('space')
    time.sleep(.15 + abs(np.random.normal(.1,.05)))

    

    #wait until all pots are made
    print('waiting until I see no herbs')
    loop_start = time.time()
    while True:
        screenshot = wincap.get_screenshot()
        herb_allPoints, herb_bestPoint, herb_confidence = herb_vision.find(screenshot, threshold = HERB_THRESHOLD, debug_mode= 'rectangles', return_mode= 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        if len(herb_allPoints) == 0:
            print('I see %ss herbs | confidence %s | breaking zero herb search loop' %(len(herb_allPoints),round(herb_confidence,3)))
            herb_screenpoint = wincap.get_screen_position(herb_bestPoint)
            tick_dropper()
            herb_clickpoint = herb_action.click(herb_screenpoint, speed = speed(), wait=wait(), tick_dropper_odds= 100)
            break
        if time.time() - loop_start > 60:
            print('PROBLEM(!) zero-herb searched %ss, still seeing herbs | Exit...' %(time.time() - loop_start))
            exit()

    #debugging
    count = count +1
    run_time = time.time() - start_time

    if s_or_c == 's': 
        if run_time > stop_seconds:
            print('timer is up | ran for %s | exitting...' % round(run_time,3))
        print('loop complete | run_time %ss | count %s | time remaining %ss' %( round(run_time,3), count, (stop_seconds - run_time) ))

    if s_or_c == 'c':
        if stop_count > count:
            print('counter is up | ran for %s counts | exitting...' %(count))
        print('loop complete | run_time %ss | count %s | counts remaining %ss' %( round(run_time,3), count, (stop_count - count) ))
        
 
### everything below this line is scrap. 

# 1. run in classic fixed


