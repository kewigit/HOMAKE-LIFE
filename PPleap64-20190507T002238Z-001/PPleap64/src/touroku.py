#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
sys.path.insert(0,"../lib/x64") #LeapMotionのライブラリのパス 'Leap.dll' 'Leap.lib' 'LeapPython.pyd'
import Leap                     #LeapMotionのライブラリ2 'Leap.py'
import time
import socket
 
#Pygame Setup
SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("HOMAKE*LIFE") #タイトル

# フォントの作成
sysfont = pygame.font.SysFont(None, 50)
titlefont = pygame.font.SysFont(None, 80)
#title = sysfont.render("HOMAKE*LIFE",True,(0,0,0))


#s.connect(( 'OO' ,port))の 'OO' 部分
host = "192.168.1.241" #お使いのサーバーのホスト名を入れます
port = 5556 #クライアントと同じPORTをしてあげます
hostname = 'yaniks'


#socket通信の接続と'cc'というメッセージ送信
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #こいつここにおいてるけどmainの中とかで使えるのならばそっちのがいいかもしれない
#s.connect((host,port))                                  #上に同じく     [socket通信]
#s.sendall('cc')                                         #ひとまずのSocket通信の接続確認用

class pptxListener(Leap.Listener):
    
    eid =1 #関数の外で宣言している為に他の場所で使う場合self. /カウントダウン、アップのセッティング用
    cnt =0 #送信処理を入れるための変数。SWIPEで
    def on_connect(self,controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE) #サークルジェスチャをアクティブに
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)  #スワイプジェスチャをアクティブに
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    def on_frame(self,controler):
        frame = controler.frame()
        hands = frame.hands
        hand = hands[0]
        #手の座標のX,Z軸を取得し、格納してます。
        nowx = hand.palm_position[0]
        nowz = hand.palm_position[2]
        baseX =0                            
        baseZ =0
        deltaX = nowx - baseX
        deltaZ = nowz - baseZ
        if deltaX > 60:
            
            xpos = sysfont.render("RIGHT",True,(0,0,0))
        if deltaX < -60:
            xpos = sysfont.render("LEFT",True,(0,0,0))
        if deltaX > -60 and deltaX < 60:
            xpos = sysfont.render("CENTER",True,(0,0,0))
        if deltaX == 0:
            xpos = sysfont.render("NO HAND",True,(0,0,0))
        
        screen.fill((255,255,255))
        count = sysfont.render(str(self.eid),True,(0,0,0))
        screen.blit(xpos,(10,10))
        screen.blit(count,(300,200))
        pygame.display.update()
        
        pygame.event.poll()
        for gesture in frame.gestures():
            
            #カウント処理、左右でサークルジェスチャを行う事でカウントアップ、ダウンを行う。
            if deltaX > 60 and self.cnt == 0: #左右の方向を確認、右に60以上の座標の場合に判定
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    self.eid += 1
                    print "RIGHT:",self.eid #コンソールにRIGHTの文字とeidの中に入っている数字が出力されます。
                    screen.blit(xpos,(300,300))
                    time.sleep(1)       #高速で何回も行われないように挟んでます。
            if deltaX < -60 and self.cnt == 0: #左右の方向を確認、左に60以上の座標の場合に判定
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    self.eid -= 1
                    print "LEFT:",self.eid #コンソールにLEFTの文字とeidの中に入っている数字が出力されます。
                    time.sleep(1)       #高速で何回も行われないように挟んでます。
            
            #送信処理、サークルジェスチャで現在のeidの中身をStrでRaspberryPiへ送信。
            #cntが1になることで送信モードへ移行し、その後左右のサークルジェスチャで送信、キャンセルを行う
            if deltaX < 60 and deltaX > -60 and self.cnt == 0:
                if gesture.type == Leap.Gesture.TYPE_SWIPE: #SWIPEのジェスチャが検出されたら 
                    print"ENTER?",self.eid
                    self.cnt += 1                            
                    time.sleep(1)
            if  self.cnt == 1 and deltaX < -60:
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    print "YES",self.eid
                    #s.sendall(str(self.eid)) #eidの中身をsocketでサーバープログラムへぽいちょしてます。
                    self.cnt -= 1
                    time.sleep(1)       #高速で何回も行われないように挟んでます。 
            
            if  self.cnt == 1 and deltaX > 60:
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    print "NO",self.eid
                    self.cnt -= 1
                    time.sleep(1)       #高速で何回も行われないように挟んでます。 


            #if gesture.type == Leap.Gesture.TYPE_KEY_TAP: #KET_TAPのジェスチャが検出されたら 
            #    print"TOUROKU"
            #    s.sendall(str('reg')) #登録モード用
            #    time.sleep(2)

            #エラー対策、0以下で6にします、7以上で1にします。
            if self.eid < 1:
                self.eid = 6
                print"LOOP",self.eid
                    
            if self.eid > 6:
                self.eid = 1
                print"LOOP",self.eid
        

def main():
    screen.fill((255,255,255))
    #screen.blit(title,(200,50))
    pygame.display.update()
    
    listener = pptxListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit...."
    for event in pygame.event.get():
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
                pygame.quit()
                sys.exit()
                controller.remove_listener(listener)    #leapmotionを閉じてます
                #s.close()                               #socketを閉じてる
                sys.exit()
if __name__=="__main__":
    main()
