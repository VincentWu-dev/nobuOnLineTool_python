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


nobu_hWndDict ={}



#win32con.VK_RETURN
'''
def nobu_send_key(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key)
'''

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

def nobu_click_pos(pos, action, offset):
    pyautogui.moveTo(pos[0]+offset, pos[1]+offset, duration=0.1)
    pyautogui.click(button=action)

def nobu_manufacture_click(curHwnd, curApp):
   isStop = False
   img = "./img/材料不夠.png"
   #img = "./img/not_enough.png"
   rect = win32gui.GetWindowRect(curHwnd)
   
   while not isStop :
    pos = nbut.nobu_imagesearch(rect, img, 0.8)
    if pos[0] != -1:
        print("Find img. x: %d y: %d" % (pos[0], pos[1]))
        #nobu_click_pos(pos, "left", 5)
        isStop = True
    else:
        nbut.nobu_send_key(curHwnd, curApp, "ENTER")
    time.sleep(0.1)

def nobu_template_func(curHwnd, curApp):
   isStop = False
   keyEnter = "ENTER"

   #img = "./img/材料不夠.png"
   #img = "./img/not_enough.png"
   rect = win32gui.GetWindowRect(curHwnd)
   curMode = 0
   
   while True:
    match curMode:
        case 0:
          if nbut.nobu_is_in_combat(rect):
            print("Combat IN!!")
            curMode = 1
          
        case 1:
          if nbut.nobu_is_out_combat(rect):
            print("Combat OUT!!")
            curMode = 2
          
        case _:
          break
    time.sleep(0.3)
      
if __name__ == '__main__':
    argv = sys.argv
    cmd = -1
    curHwnd = 0
    curApp = 0
    if (len(argv)>1):
        cmd = int(argv[1])
        print("cmd: %d" % cmd)

    find_window_list(nbut.NOBUON_CLASS_NAME)
    for key in nobu_hWndDict:
       if key.find("NO:1") != -1 or key.find("Nobunaga Online HD Tc") != -1:
          print("Found "+key)
          curHwnd = nobu_hWndDict.get(key)
          break
    
    #hwnd = win32gui.FindWindow(nbut.NOBUON_CLASS_NAME, None)
    print("hwnd: %x" %(curHwnd))
    proc_id = pywinauto.application.process_from_module("nobolHD.bng")
    curApp = pywinauto.Application().connect(handle = curHwnd)
    
    match cmd:
        case 0:
            nobu_manufacture_click(curHwnd, curApp)
        case 1:
            nobu_template_func(curHwnd, curApp)
        case _:
            print("No cmd to run")


    
    
