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
from enum import Enum, auto

class NobuOnState(Enum):
    NOBUON_MOVE_ENTER_STATE = auto()
    NOBUON_INCOMBAT_STATE = auto()
    NOBUON_ENDCOMBAT_STATE = auto()
    NOBUON_NEXTFLOOR_STATE = auto()
    NOBUON_MOVE_STATE = auto()
    NOBUON_EXIT_DUNG_STATE = auto()
    NOBUON_CHOOSE_FLOOR_STATE = auto()
    NOBUON_FIND_ENTERANCE_STATE = auto()

class NobuOnContext:
    def __init__(self, hwnd, app, run=True):
        self.hwnd = hwnd
        self.app = app
        self.rect = win32gui.GetWindowRect(hwnd)
        self.img_dict = nbut.nobu_load_img()

    def getRect(self):
        return self.rect

    def getHwnd(self):
        return self.hwnd

    def getApp(self):
        return self.app

    def setRun(self, run):
        self.run = run

    def getRun(self):
        return self.run

class CombatState:
    def __init__(self,nb_context, state=nbut.NOBUON_IDLE_STATE):
        self.curState = state
        self.nextState = nbut.NOBUON_IDLE_STATE
        self.context = nb_context
    def checkInCombatState(self):
        rect = self.context.getRect()
        time.sleep(0.1)
        return nbut.nobu_is_in_combat(rect)

    def checkEndCombatState(self):
        rect = self.context.getRect()
        if nbut.nobu_is_out_combat(rect):
            t1 = time.time()
            while (time.time() - t1) < 2: #keep checking in 0.5 sec
                time.sleep(0.2)
                if not nbut.nobu_is_out_combat(rect):
                    return False
            
            return True
        else:
            return False

    def checkMoveToNextFloor(self):
        rect = self.context.getRect()
        time.sleep(0.2)
        pos= nbut.nobu_imagesearch(rect, "./img/是否移動下一層.png")
        if pos[0]!=-1:
            return True
        else:
            return False

    def loopCheckInCombatState(self):
        rect = self.context.getRect()
        while True:
            if nbut.nobu_is_in_combat(rect):               
                return True
            time.sleep(0.1)

    def loopCheckEndCombatState(self):
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

    def loopCheckMoveToNextFloor(self):
        rect = self.context.getRect()
        while True:
            if nbut.nobu_imagesearch(rect, "進入下一層圖片"):               
                return True
            time.sleep(0.2)

        


