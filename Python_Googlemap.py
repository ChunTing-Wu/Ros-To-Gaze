import rospy
import queue
import websocket
import json
import threading
import signal
import time
import os


from sensor_msgs.msg import NavSatFix

#define HOST_IP
#define PORT

HOST_IP = "140.116.245.172"
PORT = "8764"

kill_thread = False


# message
class RosThread(threading.Thread):
    ros_subscriber = None
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
            ws_thread.queue.put({'gps_data': json_data})

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
        gnss_times = 0
        try:
            while not kill_thread:
                if not self.queue.empty():
                    msg = self.queue.get()
                    json_data = json.dumps({'data': msg})
                    gnss_times = gnss_times + 1
                    if gnss_times > 5:
                        self.ws.send(json_data)
                        gnss_times = 0
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
        ros_thread = RosThread()
        ws_thread = WebSocketThread()

        ros_thread.daemon = True
        ws_thread.daemon = True
        ros_thread.start()
        ws_thread.start()

        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        print("GET INTERRUPT")
        pass
    finally:
        rospy.signal_shutdown('Shutdown signal received')
        kill_thread = True
        print('\ndone.')