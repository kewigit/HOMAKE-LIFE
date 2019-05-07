# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"../lib/x64") #LeapMotionのライブラリのパス 'Leap.dll' 'Leap.lib' 'LeapPython.pyd'
import Leap                     #LeapMotionのライブラリ2 'Leap.py'
import time
import socket

#s.connect(( 'OO' ,port))の 'OO' 部分
host = "192.168.1.241"                                      #お使いのサーバーのホスト名を入れます
port = 5556                                                 #クライアントと同じPORTをしてあげます
hostname = 'yaniks'


#socket通信の接続と'cc'というメッセージ送信
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #こいつここにおいてるけどmainの中とかで使えるのならばそっちのがいいかもしれない
s.connect((host,port))                                      #上に同じく     [socket通信]
class pptxListener(Leap.Listener):
    
    eid =1                                                  #関数の外で宣言している為に他の場所で使う場合self. /カウントダウン、アップのセッティング用
    cnt =0                                                  #送信処理を入れるための変数。SWIPEで
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
        baseX =0                        
        deltaX = nowx - baseX
        
         
        def countup():
            self.eid += 1
            print "RIGHT:",self.eid                  #コンソールにRIGHTの文字とeidの中に入っている数字が出力されます。
            s.sendall(str("1"))
            time.sleep(2)                            #高速で何回も行われないように挟んでます。
        def countdown():            
            self.eid -= 1
            print "LEFT:",self.eid                   #コンソールにLEFTの文字とeidの中に入っている数字が出力されます。
            s.sendall(str("2"))
            time.sleep(2)                            #高速で何回も行われないように挟んでます。
        
        for gesture in frame.gestures():
            
            #カウント処理、左右でサークルジェスチャを行う事でカウントアップ、ダウンを行う。
            if deltaX > 60 and self.cnt == 0:                #左右の方向を確認、右に60以上の座標の場合に判定
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    countup()
            
            if deltaX < -60 and self.cnt == 0:               #左右の方向を確認、左に60以上の座標の場合に判定
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    countdown()

            #送信処理、サークルジェスチャで現在のeidの中身をStrでRaspberryPiへ送信。
            #cntが1になることで送信モードへ移行し、その後左右のサークルジェスチャで送信、キャンセルを行う
            if deltaX < 60 and deltaX > -60 and self.cnt == 0:
                if gesture.type == Leap.Gesture.TYPE_SWIPE:  #SWIPEのジェスチャが検出されたら 
                    print"ENTER?",self.eid
                    self.cnt += 1                            
                    time.sleep(2)
            if  self.cnt == 1 and deltaX < -60:
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    print "YES",self.eid
                    s.sendall(str(self.eid))                 #eidの中身をsocketでサーバープログラムへぽいちょしてます。
                    self.cnt -= 1
                    time.sleep(2)                            #高速で何回も行われないように挟んでます。 
            
            if  self.cnt == 1 and deltaX > 60:
                if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                    print "NO",self.eid
                    self.cnt -= 1
                    time.sleep(2)                            #高速で何回も行われないように挟んでます。 


            #エラー対策、0以下で6にします、7以上で1にします。
            if self.eid < 1:
                self.eid = 6
                print"LOOP",self.eid
                for i in range(6):
                    s.sendall(str("1"))
                time.sleep(1)
            if self.eid > 6:
                self.eid = 1
                print"LOOP",self.eid
                for i in range(6):
                    s.sendall(str("2"))
                time.sleep(1)

def main():
    listener = pptxListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit...."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)    #leapmotionを閉じてます
        s.close()                               #socketを閉じてる
if __name__=="__main__":
    main()