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

class NobuOnContext:
    def __init__(self, hwnd, app):
        self.hwnd = hwnd
        self.app = app
        self.rect = win32gui.GetWindowRect(hwnd)
        self.img_dict = nbut.nobu_load_img()
    
    def getRect(self):
        return self.rect


class CombatState:
    def __init__(self,nb_context, state=nbut.NOBUON_IDLE_STATE):
        self.curState = state
        self.nextState = nbut.NOBUON_IDLE_STATE
        self.context = nb_context
    
    def checkInCombatState(self):
        rect = self.context.getRect()
        while True:
            if nbut.nobu_is_in_combat(rect):               
                return True
            time.sleep(0.1)
    
    def checkEndCombatState(self):
        rect = self.context.getRect()
        while True:
            if nbut.nobu_is_out_combat(rect):
                t1 = time.time()
                while (time.time() - t1) < 2: #keep checking in 0.5 sec
                    time.sleep(0.2)
                    if not nbut.nobu_is_out_combat(rect):
                        return False
                
                return True
            time.sleep(0.2)

        


