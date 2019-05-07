# -*- coding:utf-8 -*-

import sys
sys.path.insert(0,"../lib/x64") #LeapMotionのライブラリのパス 'Leap.dll' 'Leap.lib' 'LeapPython.pyd'
import Leap                     #LeapMotionのライブラリ2 'Leap.py'
import time
import socket

#s.connect(( 'OO' ,port))の 'OO' 部分
host =  '192.168.1.241'
#"192.168.1.129" #お使いのサーバーのホスト名を入れます
port = 5556 #クライアントと同じPORTをしてあげます
hostname = 'yaniks'

#socket通信の接続と'cc'というメッセージ送信
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #こいつここにおいてるけどmainの中とかで使えるのならばそっちのがいいかもしれない
s.connect((host,port))                                  #上に同じく     [socket通信]
s.sendall('1')                                         #ひとまずのSocket通信の接続確認用

class pptxListener(Leap.Listener):
    def on_connect(self,controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE) #サークルジェスチャをアクティブに
        #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)  #スワイプジェスチャをアクティブに
        #controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        #controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
    def on_frame(self,controler):
        cid = 0
        frame = controler.frame()
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE: #CIRCLEのジェスチャが検出されたら
                cid = 1
                print "CICRLE:",cid #コンソールにCIRCLEの文字とcidの中に入っている数字が出力されます。
                s.sendall(str(cid)) #cidの中身をsocketでサーバープログラムへぽいちょしてます。
                time.sleep(2)       #高速で何回も行われないように挟んでます。
        
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
