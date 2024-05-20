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
import nobutool_utils as nbut
from nobutool_class import *
import tkinter as tk
import threading
from PIL import Image
import pytesseract
from math import ceil
from PyQt5.QtWidgets import QApplication
import datetime

nobu_hWndDict ={}



#win32con.VK_RETURN
'''
def nobu_send_key(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key)
'''
def get_curHwnd(name):
    curHwnd = 0
    for key in nobu_hWndDict:
       if key.find("NO:1") != -1 or key.find(name) != -1:
          print("Found "+key)
          curHwnd = nobu_hWndDict.get(key)
          break
    return curHwnd

def find_window_list(targetclass): 
  hWndList = []
  win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList) 
  for hwnd in hWndList:
    clsname = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if (clsname == targetclass):  #调整目标窗口到坐标(600,300),大小设置为(600,600)
      #win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600,300,600,600, win32con.SWP_SHOWWINDOW)
        nobu_hWndDict.setdefault(title, hwnd)

def get_window_rect(handle):
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    width = right - left
    height = bottom - top
    return width, height   

def nobu_manufacture_click(context):
   isStop = False
   img = "./img/材料不夠.png"
   #rect = win32gui.GetWindowRect(context.get_curHwnd())

   while not isStop :
    pos = nbut.nobu_imagesearch(context.getRect(), img, 0.8)
    if pos[0] != -1:
        print("Find img. x: %d y: %d" % (pos[0], pos[1]))
        #nobu_click_pos(pos, "left", 5)
        isStop = True
    else:
        nbut.nobu_send_key(context.get_curHwnd(),context.getApp(), "ENTER")
    time.sleep(0.1)

def thread_imgsearch(winrect, image,event, precision=0.8):
    while True:
        time.sleep(0.3)
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
        if max_val >= precision:
            event.set()
            imgLoc = list(max_loc)
            imgLoc[0] += winrect[0]
            imgLoc[1] += winrect[1]
            print("thread_imgsearch Found: "+image)
            break
    

        #return imgLoc #返回圖片座標

def nobu_thread_sendkey(hwnd, key:str, combo_key:str, holdTime=5):
   while True:
      nbut.nobu_send_combokey(nb_context.getHwnd(), "a","VK_SHIFT", 2)
      
      
'''
 while True:
      pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/北.png")
      pos1 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/北1.png")
      pos2 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/北2.png")
      pos3 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/西.png")
      pos4 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/西1.png")
      pos5 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/西2.png")
      if pos[0] !=-1:
         print("找到北")
      if pos1[0] !=-1:
         print("找到北1")
      if pos2[0] !=-1:
         print("找到北2")
      if pos3[0] !=-1:
         print("找到西")
      if pos4[0] !=-1:
         print("找到西1")
      if pos4[0] !=-1:
         print("找到西2")
      
       
   nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"a", 0.05)
   time.sleep(0.2)
      
'''
def nobu_test_func(nb_context):
   isStop = False
   
   curMode = 0

   cb_state = CombatState(nb_context)
   nb_context.setRun(False)

   clickList = nobu_select_floor_func(nb_context, 502)
   nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
   nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"j", 0.2)

   for i in range(clickList[0]):
      nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
      time.sleep(0.5)

   #nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"k", 0.2)
   #nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"k", 0.2)
   for i in range(clickList[1]+2):
      nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"k", 0.2)
      time.sleep(0.5)
   
   nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
   pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/進入冥宮對話.png")
   if pos[0] != -1:
      print("找到進入冥宮對話")
   else:
      print("沒找到進入冥宮對話")
   
   #選取進入冥宮
   nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"j", 0.2)
   nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
      

def nobu_select_floor_func(nb_context, targetFloor=0):

   nb_context.setRun(False)
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   print("-->nobu_select_floor_func")

   keyList = ['k','ENTER','ENTER','i','i']
   for i in keyList:
      nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),i, 0.2)
      time.sleep(0.2)

#check do we have maxfloor

   maxFloor = nb_context.getMaxFloor()
   if maxFloor == 0:
      nb_context.setRun(True)
   
   while nb_context.getRun() :
        pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/層.png")
        if pos !=-1:
            print("找到層: %d %d" %(pos[0],pos[1]))
            
        #left, top, right, bottom = win32gui.GetWindowRect(nb_context.getHwnd())
        myScreenshot = pyautogui.screenshot(region=(pos[0]+30,pos[1], 40,25))
        myScreenshot.save("./img/floor_shot.png")
        text = nbut.nobu_digi_ocr_func("./img/floor_shot.png")
        if text !="":
            print("text: "+text)
            maxFloor = int(text)
            if maxFloor != 0:
                nb_context.setRun(False)
                nb_context.setMaxFloor(maxFloor)

   clickList=list()
   #targetFloor = 502 #502 504 507 509
   remainder = maxFloor%30 #餘數
   clicks = ceil(targetFloor/30) #上一頁按的次數 一次30. 無條件進位
   clickList.append(clicks)
   mvDown=(30*clicks+remainder)-targetFloor
   clickList.append(mvDown)

   for i in clickList:
      print([i])

   print("%d %d" % (maxFloor, remainder))
   return clickList

def nobu_template_func(nb_context):
   isStop = False
   keyEnter = "ENTER"

   #rect = win32gui.GetWindowRect(curHwnd)
   curMode = 0

   cb_state = CombatState(nb_context)
   event_a = threading.Event()   # 註冊 event_a
   event_b = threading.Event()  
   a = threading.Thread(target=thread_imgsearch,args=(nb_context.getRect(), "./img/夢幻城入口2.png", event_a))
   b = threading.Thread(target=thread_imgsearch,args=(nb_context.getRect(), "./img/夢幻城入口.png", event_b))
   #a.start()
   #b.start()
   
   nb_context.setRun(True)
   curMode = NobuOnState.NOBUON_FIND_ENTERANCE_STATE
   #curMode = NobuOnState.NOBUON_CHOOSE_FLOOR_STATE
   
   time1 = time.time()

   nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"v")
   nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"d", 0.2)

   #nbut.nobu_test_send_key(nb_context.getHwnd(), nb_context.getApp(),"a", 5)
   #nbut.nobu_send_combokey(nb_context.getHwnd(), "a","VK_SHIFT"m 5)
   while True:
      match curMode:
        case NobuOnState.NOBUON_FIND_ENTERANCE_STATE:
            if time.time() - time1 > 5:
                nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"d", 0.2)
                time1 = time.time()
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"l", 0.2)
            time.sleep(0.5)
            pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/醫生.png")

            
            if pos[0] != -1:
                print("Found 醫生")
                curMode = NobuOnState.NOBUON_MOVE_ENTER_STATE
                time1 = time.time()
                
        case NobuOnState.NOBUON_MOVE_ENTER_STATE:
            for i in range(0,2):
                nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.5)
                time.sleep(0.2)
            
            time.sleep(3)
            nbut.nobu_loop_turn(nb_context,"a", "北")
            time.sleep(1)
            nbut.nobu_send_combokey(nb_context.getHwnd(), "a", "VK_SHIFT", holdTime=4.8)
            #nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"w", 1)
            
            
            '''
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"a", 1.3)
            time.sleep(1)
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"w", 1)
            time.sleep(1)
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"d", 0.8)
            time.sleep(0.5)
            '''
            
            searchRun = True
            while searchRun:
               pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/冥宮入場選單.png")
               if pos[0] != -1:
                  print("找到冥宮入場選單")
                  searchRun = False
                  curMode = NobuOnState.NOBUON_CHOOSE_FLOOR_STATE
               else:
                  nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"w", 1)
            #nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"v")
        #k>enter>search 最底層>click>
        case NobuOnState.NOBUON_CHOOSE_FLOOR_STATE:
            print("-->NOBUON_CHOOSE_FLOOR_STATE")
            clickList = nobu_select_floor_func(nb_context, 502)
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"j", 0.2)

            
            #
            for i in range(clickList[0]):
                nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
                time.sleep(0.5)

            for i in range(clickList[1]+2):
                nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"k", 0.2)
                time.sleep(0.5)
            
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
            pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/進入冥宮對話.png")
            if pos[0] != -1:
                print("找到進入冥宮對話")
            else:
                print("沒找到進入冥宮對話")
            
            #選取進入冥宮
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"j", 0.2)
            nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER", 0.2)
            break


         
        case _:
         break
         
      time.sleep(0.3)      
'''
   while nb_context.getRun():
        nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"d", 0.1)
        time.sleep(0.3)
        pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/北.png")
        #pos1 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/北1.png")
        pos2 = nbut.nobu_imagesearch(nb_context.getRect(), "./img/光球南.png")
        if (pos[0] !=-1): print("Found 北")
        if (pos2[0] !=-1):
            print("Found 南")
            while True:
                nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"w", 0.3)
                nbut.nobu_send_key(nb_context.getHwnd(), nb_context.getApp(),"ENTER")
                time.sleep(0.2)
                pos = nbut.nobu_imagesearch(nb_context.getRect(), "./img/冥宮退場.png")
                if pos[0] !=-1:
                    print("找到冥宮退場.png")
                    nb_context.setRun(False) 
                    break
            
   '''
#ccnt = 0

def nobu_test1_func(nb_context):
   isStop = False
   
   curMode = 0

   cb_state = CombatState(nb_context)
   nb_context.setRun(False)

   while nb_context.getRun():
      pos = nbut.nobu_imagesearch(nb_context.getRect(),"./img/隊伍6人.png", 0.8)
      if pos[0]!=-1:
         print("找到 隊伍6人1.png")
         time.sleep(0.5)
         #nb_context.setRun(False)


   ccnt = 0
   app = QApplication(sys.argv)
   screen = app.primaryScreen()
   
   while True:
    time1 = time.time()
    img = screen.grabWindow(nb_context.getHwnd())
    img.save("screenshot_pyqt5_"+str(ccnt)+".png","png")
    ccnt+=1
    time.sleep(0.2)

   #img_rgb = cv2.imread("screenshot_pyqt5.png")
   #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
   #cv2.imwrite('screenshot_gray.png', img_gray)
   #print(time.time()-time1)
   #img.save("screenshot_pyqt5.jpg")

   
if __name__ == '__main__':
    argv = sys.argv
    cmd = -1
    curHwnd = 0
    curApp = 0
    if (len(argv)>1):
        cmd = int(argv[1])
        print("cmd: %d" % cmd)

    find_window_list(nbut.NOBUON_CLASS_NAME)
    curHwnd = get_curHwnd(nbut.NOBUON_TITLE_NAME)

    #find_window_list(nbut.NOTEPAD_PLUS_CLASS_NAME)
    #curHwnd = get_curHwnd(nbut.NOTEPAD_PLUS_TITLE_NAME)
    #hwnd = win32gui.FindWindow(nbut.NOBUON_CLASS_NAME, None)
    now = datetime.datetime.now()
    print("hwnd: %x" %(curHwnd))
    dateTime = now.strftime("%Y-%m-%d, %H:%M:%S")
    print(dateTime)
    #proc_id = pywinauto.application.process_from_module("nobolHD.bng")
    curApp = pywinauto.Application().connect(handle = curHwnd)
    nb_context = NobuOnContext(curHwnd, curApp)
    
    #root = tk.Tk()
    #root.title('nobutool')        # 設定標題
    #root.iconbitmap('favicon.ico')  # 設定 icon ( 格式限定 .ico )

    # 如果是 Mac 使用下面這行，可以使用 gif 或 png
    # root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='icon.gif'))
    #root.mainloop()

    match cmd:
        case 0:
            nobu_manufacture_click(nb_context)
        case 1:
            nobu_template_func(nb_context)
        case 2:
            nobu_test_func(nb_context)
        case 3:
            nobu_test1_func(nb_context)
        case _:
            print("No cmd to run")
