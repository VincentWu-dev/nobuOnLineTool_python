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
from pywinauto.keyboard import send_keys
from nobutool_class import *
#from PIL import Image
import pytesseract

NOBUON_CLASS_NAME = "Nobunaga Online Game MainFrame"
NOBUON_TITLE_NAME = "Nobunaga Online HD Tc"
NOTEPAD_PLUS_TITLE_NAME = "*新文件 4 - Notepad++"
NOTEPAD_PLUS_CLASS_NAME = "Notepad++"
'''
NOBUON_IDLE_STATE = 0
NOBUON_INCOMBAT_STATE = 1
NOBUON_ENDCOMBAT_STATE = 2
NOBUON_MOVE_STATE = 3
NOBUON_EXIT_DUNG_STATE = 4
NOBUON_CHOOSE_FLOOR_STATE = 5
NOBUON_FIND_ENTERANCE_STATE = 6
'''

def nobu_click_pos(pos, action, offset, clicks=1, interval=1):
    pyautogui.moveTo(pos[0]+offset, pos[1]+offset, duration=0.1)
    pyautogui.click(button=action, clicks=clicks, interval=interval)

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
    #print("nobu_imagesearch time consume: "+str(time.time() - time1))
    if max_val < precision:
        return [-1,-1]
    imgLoc = list(max_loc)
    imgLoc[0] += winrect[0]
    imgLoc[1] += winrect[1]

    return imgLoc #返回圖片座標

def nobu_send_combokey(hwnd, key:str, combo_key:str, holdTime=5):
    print("%s %s" % (key, combo_key))
    kbDown = "{%s down}" % (key)
    kbUp = "{%s up}" % (key)
    combokbDown = "{%s down}" % (combo_key)
    combokbUp = "{%s up}" % (combo_key)

    time1 = time.time()

    print("[%s] [%s]" % (kbDown, kbUp))
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    send_keys(combokbDown)
    send_keys(kbDown)
    time.sleep(holdTime)
    send_keys(combokbUp)
    send_keys(kbUp)

def nobu_send_key(hwnd, app, key: str,holdTime=0.1, combo_key=""):
    kbDown = "{%s down}" % (key)
    kbUp = "{%s up}" % (key)
    
    time1 = time.time()
    print("[%s] [%s]" % (kbDown, kbUp))
    try:
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w down}')
        
        if combo_key != "":
            comkbDown = "{%s down}" % (combo_key)
            print("[%s]" %(comkbDown))
            app.window(handle=hwnd).send_keystrokes(comkbDown)
        app.window(handle=hwnd).send_keystrokes(kbDown)
        time.sleep(holdTime)
        if combo_key != "":
            comkbUp = "{%s up}" % (combo_key)
            print("[%s]" %(comkbUp))
            app.window(handle=hwnd).send_keystrokes(comkbUp)
        app.window(handle=hwnd).send_keystrokes(kbUp)
    except:
        print("send_keystrokes error catch!!")
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w up}')
    #print("time consume: "+str(time.time() - time1))

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

def nobu_loop_turn(nb_context,turn_dir:str, direction: str):
    imgList = list()
    for i in range(0,3):
        imgList.append("./img/"+direction+str(i)+".png")
    print(imgList)

    loopRun = True
    while loopRun:
      nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),turn_dir, 0.05)  
      for i in range(0,3):
        pos = nbut.nobu_imagesearch(nb_context.getRect(), imgList[i])
        if pos[0] != -1:
            print("找到"+imgList[i])
            loopRun = False
            break;
      time.sleep(0.3)


#TO DO: Load all image in ./img/
def nobu_load_img():
    print("-->nobu_load_img")

#數字OCR
def nobu_digi_ocr_func(imgPath):
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   print("-->nobu_digi_ocr_func")

   rawImg = cv2.imread(imgPath)
   height,width,deep= rawImg.shape
   gray = cv2.cvtColor(rawImg, cv2.COLOR_BGR2GRAY)
   dst = np.zeros((height, width, 1), np.uint8)
   for i in range(0,height):
       for j in range(0,width):
            grayPixel = gray[i,j]
            dst[i,j] = 255-grayPixel

   ret, binary = cv2.threshold(gray, 0 ,255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)

   #img = Image.open('./img/floor_shot.png')
   text = pytesseract.image_to_string(binary, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
   return text

def nobu_statusCheck_reset(nb_context, heroTeamSet=0):
    #TODO呼叫英傑組合確認人數

    pos = nobu_imagesearch(nb_context.getRect(), "./img/隊友人數.png", 0.95)
    if pos[0]!=-1:
        print("重新呼叫英傑組合")

    #TODO轉向正北前進
    nbut.nobu_loop_turn(nb_context,"a", "北")
