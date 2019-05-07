#coding UTF-8

#----------IMPORT----------
import create
import time
import serial
import sys
sys.path.insert(0,"../lib/x86")
import Leap
#----------CONNECT----------
ROOMBA_PORT="COM5"
robot = create.Create(ROOMBA_PORT)
#----------SETUP&MODECHANGE----------
robot.toSafeMode()
#----------PROGRAM---------
#-class-

class LeaproombaListener(Leap.Listener):
    @classmethod
    def on_connect(self,controller):
        print "Connected"
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #print "Frame id: %d, timestamp: %d" % (frame.id, frame.timestamp)
        hands = frame.hands
        hand = hands[0] # first hand
        
        
        print("XPOS",hand.palm_position[0]) # Te no zahyou wo kakunou siteru   
        print("ZPOS",hand.palm_position[2])
        nowx = hand.palm_position[0]
        nowz = hand.palm_position[2]

        baseX =0                            # roomba mainsyori
        baseZ =0
        deltaX = nowx - baseX
        deltaZ = nowz - baseZ
        if abs(deltaX) > abs(deltaZ):
            robot.go(0,-deltaX)
        else:
            robot.go(-deltaZ)
        time.sleep(0.1)
        
#--------------MAIN-------------------#
if __name__ == '__main__':
    listener = LeaproombaListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:

        controller.remove_listener(listener)
        robot.close()