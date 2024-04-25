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

#冥宮
def nobu_dg_dream1_func(nb_context):
   isStop = False
   keyEnter = "ENTER"

   #rect = win32gui.GetWindowRect(curHwnd)
   curMode = NOBUON_IDLE_STATE

   cb_state = CombatState(nb_context)
   curHwnd = nb_context.getHwnd()
   curApp = nb_context.getApp()

#w->enter->check in combat->
   while True:
    match curMode:
        case NOBUON_IDLE_STATE
            nbut.nobu_send_key(curHwnd,curApp,"w")
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")
          if cb_state.checkInCombatState():
            print("Combat IN!!")
            curMode = NOBUON_INCOMBAT_STATE
          
        case NOBUON_INCOMBAT_STATE:
          if cb_state.checkEndCombatState():
            print("Combat END!!")
            curMode = NOBUON_ENDCOMBAT_STATE
        case NOBUON_ENDCOMBAT_STATE:
            if cb_state.checkInCombatState():
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            else:
                curMode = NOBUON_MOVE_STATE
        case NOBUON_MOVE_STATE:
            print("NOBUON_MOVE_STATE")
            nbut.nobu_send_key(curHwnd,curApp,"w")
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            if cb_state.checkMoveToNextFloor():
                nbut.nobu_send_key(curHwnd,curApp,"DOWN")
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
                curMode = NOBUON_IDLE_STATE
                #選擇確定->enter
          
        case _:
          break
    time.sleep(0.3)