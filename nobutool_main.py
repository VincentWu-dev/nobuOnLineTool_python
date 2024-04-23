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

nobu_hWndDict ={}

def cv_imread(file_path = ""):
    file_path_gbk = file_path.encode('utf-8')        # unicode转gbk，字符串变为字节数组
    img_mat = cv2.imread(file_path_gbk.decode())  # 字节数组直接转字符串，不解码
    return img_mat

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

#win32con.VK_RETURN
def nobu_send_key(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key)


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

def testnobu_imagesearch(curHwnd, imagePath):
   left, top, right, bottom = win32gui.GetWindowRect(curHwnd)
   #ipath = unicode(imagePath, "utf8")
   im = region_grabber((left, top, 1024, 768))
   pos = imagesearcharea(imagePath, left, top, 1024, 768, 0.8, im)

   if pos[0] != -1:
        print("position : ", pos[0], pos[1])
        pyautogui.moveTo(pos[0]+left, pos[1]+top)
        return True
   else:
        print("image not found")
        return False
    

def nobu_click_pos(pos, action, offset):
    pyautogui.moveTo(pos[0]+offset, pos[1]+offset, duration=0.1)
    pyautogui.click(button=action)

def nobu_manufacture_click(curHwnd):
   isStop = False
   img = "./img/材料不夠.png"
   #img = "./img/not_enough.png"
   rect = win32gui.GetWindowRect(curHwnd)
   
   while not isStop :
    pos = nobu_imagesearch(rect, img, 0.8)
    if pos[0] != -1:
        print("Find img. x: %d y: %d" % (pos[0], pos[1]))
        #nobu_click_pos(pos, "left", 5)
        isStop = True
    else:
        nobu_send_key(curHwnd, win32con.VK_RETURN)
    time.sleep(0.1)

#send keyboard by pywinauto send_keystrokes
def nobu_template_func(hwnd,  key: str, holdTime):
    #key = ord(key.upper())
    print("hwnd: %x" %(hwnd))
    proc_id = pywinauto.application.process_from_module("nobolHD.bng")
    #testapp = pywinauto.Application().connect(process = proc_id)
    time1 = time.time()
    testapp = pywinauto.Application().connect(handle = hwnd)
    kbDown = "{%s down}" % (key)
    kbUp = "{%s up}" % (key)
    #print("[%s] [%s]" % (kbDown, kbUp))
    try:
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w down}')
        testapp.window(handle=hwnd).send_keystrokes(kbDown)
        time.sleep(holdTime)
        testapp.window(handle=hwnd).send_keystrokes(kbUp)
    except:
        print("send_keystrokes error catch!!")
    #testapp.window(title="Nobunaga Online HD Tc 10.34").send_chars('{w up}')
    print("time consume: "+str(time.time() - time1))
      
if __name__ == '__main__':
    argv = sys.argv
    cmd = -1
    if (len(argv)>1):
        cmd = int(argv[1])
        print("cmd: %d" % cmd)

    find_window_list("Nobunaga Online Game MainFrame")
    for key in nobu_hWndDict:
       if key.find("NO:1") != -1 or key.find("Nobunaga Online HD Tc") != -1:
          print("Found "+key)
          curHwnd = nobu_hWndDict.get(key)
          break
    
    match cmd:
        case 0:
            nobu_manufacture_click(curHwnd)
        case 1:
            nobu_template_func(curHwnd, "w", 0.5)
        case _:
            print("No cmd to run")


    
    
