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
import datetime

dg_dream1_mode=(NobuOnState.NOBUON_MOVE_ENTER_STATE, NobuOnState.NOBUON_INCOMBAT_STATE, NobuOnState.NOBUON_ENDCOMBAT_STATE, NobuOnState.NOBUON_NEXTFLOOR_STATE, NobuOnState.NOBUON_CHECK_MEMBER_STATE)
dg_dream1_floor_mode=(NobuOnState.NOBUON_FIND_ENTERANCE_STATE, NobuOnState.NOBUON_MOVE_STATE,NobuOnState.NOBUON_CHOOSE_FLOOR_STATE, NobuOnState.NOBUON_INCOMBAT_STATE,
                         NobuOnState.NOBUON_ENDCOMBAT_STATE, NobuOnState.NOBUON_EXIT_DUNG_STATE)
dg_auto_combat_mode=(NobuOnState.NOBUON_MOVE_STATE, NobuOnState.NOBUON_INCOMBAT_STATE,NobuOnState.NOBUON_ENDCOMBAT_STATE)

def nobu_war_artillery_func(nb_context):
   #rect = win32gui.GetWindowRect(curHwnd)
   nb_context.setRun(True)

   cb_state = CombatState(nb_context)
   img = "合戰砲擊強度.png"
      
   mode_idx = 0
   timeWD = time.time()

   while nb_context.getRun():
    pos = nbut.nobu_imagesearch(nb_context.getRect(), img, 0.8)
    if pos[0] != -1:
        print("Find img. x: %d y: %d" % (pos[0], pos[1]))
        #nobu_click_pos(pos, "left", 5)
        nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(),"ENTER")
        time.sleep(5)
    else:
        nbut.nobu_send_key(nb_context.getHwnd(),nb_context.getApp(), "F8")
        time.sleep(1)

#冥宮
'''
1. #w->enter->check in combat
2. Y->3. N->1
3. check end combat. Y->4
4. w->enter->check move to next floor
'''
def nobu_dg_dream1_func(nb_context, floor=0):
   #rect = win32gui.GetWindowRect(curHwnd)
   nb_context.setRun(True)

   cb_state = CombatState(nb_context)
   curHwnd = nb_context.getHwnd()
   curApp = nb_context.getApp()
   dg_mode = dg_dream1_mode
   if floor > 0: dg_mode = dg_dream1_floor_mode
   
   mode_idx = 0
   curMode = dg_mode[mode_idx]
   timeWD = time.time()

   while nb_context.getRun():
    match curMode:
        case NobuOnState.NOBUON_FIND_ENTERANCE_STATE:
            print("NOBUON_FIND_ENTERANCE_STATE")
            mode_idx+=1
            curMode = dg_mode[mode_idx]
            time.sleep(0.5)

        case NobuOnState.NOBUON_MOVE_ENTER_STATE:
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            nbut.nobu_send_key(curHwnd,curApp,"w",0.3)
            #print("NOBUON_MOVE_ENTER_STATE: time diff: "+str(time.time()-timeWD))
            if time.time()-timeWD > 8*60:
               print("NOBUON_MOVE_ENTER_STATE: 可能掛點，開始檢查隊友人數與狀態回復")
               #nb_context.setRun(False)
               curMode = NobuOnState.NOBUON_CHECK_MEMBER_STATE
               now = datetime.datetime.now()
               dateTime = now.strftime("%Y-%m-%d, %H:%M:%S")
               print(dateTime)
               #nbut.nobu_statusCheck_reset(nb_context, 0)
               #mode_idx = 0
               #curMode = dg_mode[mode_idx]

            if cb_state.checkInCombatState():
              print("Combat IN!!")
              timeWD = time.time()
              mode_idx+=1
              curMode = dg_mode[mode_idx]

        case NobuOnState.NOBUON_INCOMBAT_STATE:
          #print("NOBUON_INCOMBAT_STATE")
          if cb_state.checkEndCombatState():
            print("Combat END!!")
            mode_idx+=1
            curMode = dg_mode[mode_idx]
        case NobuOnState.NOBUON_ENDCOMBAT_STATE:
            if cb_state.checkInCombatState():
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            else:
                mode_idx+=1
                curMode = dg_mode[mode_idx]
        case NobuOnState.NOBUON_NEXTFLOOR_STATE:
            #print("NOBUON_NEXTFLOOR_STATE")
            time.sleep(0.5)      
            nbut.nobu_send_key(curHwnd,curApp,"w", 0.2)
            nbut.nobu_send_key(curHwnd,curApp,"ENTER")

            if time.time()-timeWD > 8*60:
               print("NOBUON_NEXTFLOOR_STATE: 可能掛點，開始檢查隊友人數與狀態回復")
               now = datetime.datetime.now()
               dateTime = now.strftime("%Y-%m-%d, %H:%M:%S")
               print(dateTime)
               curMode = NobuOnState.NOBUON_CHECK_MEMBER_STATE

            if cb_state.checkMoveToNextFloor():
                time.sleep(1)
                nbut.nobu_send_key(curHwnd,curApp,"j")
                #time.sleep(1)
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
                mode_idx=0
                curMode = dg_mode[mode_idx]
                time.sleep(3) #進入下一層delay 3秒
                #選擇確定->enter
        case NobuOnState.NOBUON_CHECK_MEMBER_STATE:
            print("NOBUON_CHECK_MEMBER_STATE: 重生與檢查英傑人數並叫出設定")
            nb_context.setRun(False)
        case _:
          break
    time.sleep(0.4)

def nobu_auto_combat_func(nb_context, combat_action=()):
   #rect = win32gui.GetWindowRect(curHwnd)
   nb_context.setRun(True)

   cb_state = CombatState(nb_context)
   curHwnd = nb_context.getHwnd()
   curApp = nb_context.getApp()
   dg_mode=dg_auto_combat_mode
   
   
   mode_idx = 0
   curMode = dg_mode[mode_idx]
   timeWD = time.time()

   while nb_context.getRun():
      match curMode:
         case NobuOnState.NOBUON_MOVE_STATE:
            if cb_state.checkInCombatState():
              print("Combat IN!!")
              time.sleep(3)
              for i in combat_action:
                 print("Key: "+i)
                 nbut.nobu_send_key(curHwnd,curApp, i)
                 time.sleep(0.2)
              mode_idx+=1
              curMode = dg_mode[mode_idx]

         case NobuOnState.NOBUON_INCOMBAT_STATE:
            if cb_state.checkEndCombatState_test():
                print("Combat END!!")
                mode_idx+=1
                curMode = dg_mode[mode_idx]
         case NobuOnState.NOBUON_ENDCOMBAT_STATE:
            if cb_state.checkInCombatState():
                nbut.nobu_send_key(curHwnd,curApp,"ENTER")
            else:
                mode_idx=0
                curMode = dg_mode[mode_idx]
         case _:
            break
      time.sleep(0.4)

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