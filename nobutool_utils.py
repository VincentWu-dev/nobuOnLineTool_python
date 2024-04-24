# -*- coding: utf-8 -*-
import pyscreeze
import cv2
import numpy as np
import pyautogui
import time
import win32api,win32gui,win32con
import sys
from python_imagesearch.imagesearch import *
import pywinauto

NOBUON_CLASS_NAME = "Nobunaga Online Game MainFrame"
NOTEPAD_PLUS_CLASS_NAME = "Notepad++"
NOBUON_TITLE_NAME = "Nobunaga Online HD Tc"
NOTEPAD_PLUS_TITLE_NAME = "*新文件 4 - Notepad++"
NOBUON_IDLE_STATE = 0
NOBUON_INCOMBAT_STATE = 1
NOBUON_WAIT_COMBAT_END_STATE = 2

def nobu_imagesearch(winrect, image, precision=0.8):
    time1 = time.time()
    im = pyautogui.screenshot(region=(winrect[0],winrect[1],1024,768))
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template= cv2.imdecode(np.fromfile(image, dtype=np.uint8), 0)
    #template = cv2.imread(image, 0)
    #template = cv_imread(image)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("time consume: "+str(time.time() - time1))
    if max_val < precision:
        return [-1,-1]
    imgLoc = list(max_loc)
    imgLoc[0] += winrect[0]
    imgLoc[1] += winrect[1]

    return imgLoc #返回圖片座標

def nobu_send_key(hwnd, app, key: str, holdTime=0.1):
    kbDown = "{%s down}" % (key)
    kbUp = "{%s up}" % (key)
    time1 = time.time()
    print("[%s] [%s]" % (kbDown, kbUp))
    try:
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w down}')
        app.window(handle=hwnd).send_keystrokes(kbDown)
        time.sleep(holdTime)
        app.window(handle=hwnd).send_keystrokes(kbUp)
    except:
        print("send_keystrokes error catch!!")
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w up}')
    print("time consume: "+str(time.time() - time1))

def nobu_is_in_combat(rect):
    print("-->nobu_is_in_combat")
    pos = nobu_imagesearch(rect, "./img/戰鬥中.png", 0.8)
    if pos[0] != -1:
        return True
    else:
        return False

def nobu_is_out_combat(rect):
    pos = nobu_imagesearch(rect, "./img/戰鬥_技能.png", 0.8)
    pos1 = nobu_imagesearch(rect, "./img/戰鬥_防禦.png", 0.8)
    if pos[0] == -1 and pos1[0] == -1:
        return True
    else:
        return False

#TO DO: Load all image in ./img/
def nobu_load_img():
    print("-->nobu_load_img")