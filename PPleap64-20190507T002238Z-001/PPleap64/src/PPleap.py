import sys
sys.path.insert(0,"../lib/x64")
import Leap
#import pyautogui as pa
import time
class pptxListener(Leap.Listener):
    def on_connect(self,controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    def on_frame(self,controler):
        frame = controler.frame()
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                cid = 1
                print "CICRLE:",cid
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
        controller.remove_listener(listener)
if __name__=="__main__":
    main()
