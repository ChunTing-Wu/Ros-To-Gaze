import rospy
import queue
import websocket
import json
import threading
import signal
import time
import os

from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu

#define HOST_IP
#define PORT

HOST_IP = "140.116.245.172"
PORT = "8764"
kill_thread = False


# DEMO
class Another_Thread(threading.Thread):
    datalimit = 0

    def Another_callback(self, data):
        global ws_thread

        data = {
        "YOUR DATA":   data.linear_acceleration.z  }
        json_data = json.dumps(data)
        self.datalimit = self.datalimit + 1
        if ws_thread:
            # Put JSON data to the queue of WebSocket thread
            if(self.datalimit > 5):
                ws_thread.queue.put({'YOUR DATA': json_data})
                self.datalimit = 0

    def run(self):
        """
        YOUR rostopic
        """
        rospy.Subscriber('/carla/ego_vehicle/imu', Imu, self.Another_callback)
        rospy.spin()

class GPS_Thread(threading.Thread):
    for_gps_demo = 0
    def gps_callback(self, data):
        global ws_thread

        latitude = data.latitude
        longitude = data.longitude

        data = {
        "latitude": latitude,
        "longitude": longitude
        }
        json_data = json.dumps(data)

        if ws_thread:
            # Put JSON data to the queue of WebSocket thread
            self.for_gps_demo = self.for_gps_demo + 1
            if(self.for_gps_demo > 5):
                ws_thread.queue.put({'gps_data': json_data})
                self.for_gps_demo = 0

    def run(self):
        """
        main loop
        """

        rospy.Subscriber('/carla/ego_vehicle/gnss', NavSatFix, self.gps_callback)
        rospy.spin()




class WebSocketThread(threading.Thread):
    global HOST_IP, PORT, kill_thread
    def __init__(self):
        threading.Thread.__init__(self)
        self.ws = None
        self.queue = queue.Queue()
        print("init queue")
    def run(self):
        try:
            """
            main loop
            """
            ws_link = "ws://" + HOST_IP + ":" + PORT
            self.ws = websocket.WebSocketApp(ws_link, on_open=self.on_open)
            print("websocket start")
            self.ws.run_forever()
        except Exception as e:
            print("WebSocket connection error:", e)

    def on_open(self, ws):
        """
        WebSocket callback
        """
        print("start on open")
        try:
            while not kill_thread:
                if not self.queue.empty():
                    msg = self.queue.get()
                    json_data = json.dumps({'data': msg})
                    self.ws.send(json_data)
                    #print(json_data)
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("Key Interrupt")
def handler_int(sig, stackframe):
    exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT,handler_int)

    try:
        rospy.init_node('asrlab', anonymous=True,disable_signals=False)
        ros_thread = GPS_Thread()
        ws_thread = WebSocketThread()
        another_Thread = Another_Thread()


        ros_thread.daemon = True
        ws_thread.daemon = True
        another_Thread.daemon = True

        ros_thread.start()
        ws_thread.start()
        another_Thread.start()
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("GET INTERRUPT")
        pass
    finally:
        rospy.signal_shutdown('Shutdown signal received')
        kill_thread = True
        print('\ndone.')