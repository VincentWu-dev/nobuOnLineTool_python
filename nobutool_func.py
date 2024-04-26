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

dg_dream1_mode=(NobuOnState.NOBUON_MOVE_ENTER_STATE, NobuOnState.NOBUON_INCOMBAT_STATE, NobuOnState.NOBUON_ENDCOMBAT_STATE, NobuOnState.NOBUON_NEXTFLOOR_STATE)
dg_dream1_floor_mode=(NOBUON_FIND_ENTERANCE_STATE, NobuOnState.NOBUON_MOVE_STATE,NOBUON_CHOOSE_FLOOR_STATE, NobuOnState.NOBUON_INCOMBAT_STATE,
                         NobuOnState.NOBUON_ENDCOMBAT_STATE, NobuOnState.NOBUON_EXIT_DUNG_STATE)
#冥宮
'''
1. #w->enter->check in combat
2. Y->3. N->1
3. check end combat. Y->4
4. w->enter->check move to next floor
'''
def nobu_dg_dream1_func(nb_context, floor=0):
   #rect = win32gui.GetWindowRect(curHwnd)
   nb_context.setStop(True)

   cb_state = CombatState(nb_context)
   curHwnd = nb_context.getHwnd()
   curApp = nb_context.getApp()
   dg_mode = dg_dream1_mode
   if floor > 0:
    dg_mode = dg_dream1_floor_mode

    mode_idx = 0
    curMode = dg_mode[mode_idx]

   while nb_context.getRun():
    match curMode:
        case NobuOnState.NOBUON_FIND_ENTERANCE_STATE:
            print("NOBUON_FIND_ENTERANCE_STATE")
            curMode = dg_mode[mode_idx+=1]

        case NobuOnState.NOBUON_MOVE_ENTER_STATE:
            nbut.nobu_send_key(curHwnd,curApp,"w",0.3)
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            if cb_state.checkInCombatState():
              print("Combat IN!!")
              curMode = dg_mode[mode_idx+=1]

        case NobuOnState.NOBUON_INCOMBAT_STATE:
          if cb_state.checkEndCombatState():
            print("Combat END!!")
            curMode = NobuOnState.NOBUON_ENDCOMBAT_STATE
        case NobuOnState.NOBUON_ENDCOMBAT_STATE:
            if cb_state.checkInCombatState():
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            else:
                curMode = dg_mode[mode_idx+=1]
        case NobuOnState.NOBUON_NEXTFLOOR_STATE:
            print("NOBUON_NEXTFLOOR_STATE")
            nbut.nobu_send_key(curHwnd,curApp,"w", 0.3)
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            if cb_state.checkMoveToNextFloor():
                time.sleep(1)
                nbut.nobu_send_key(curHwnd,curApp,"j")
                #time.sleep(1)
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
                curMode = dg_mode[mode_idx+=1]
                #選擇確定->enter
        case _:
          break
    time.sleep(0.2)