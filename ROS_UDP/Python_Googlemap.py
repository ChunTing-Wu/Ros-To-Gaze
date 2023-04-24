import rospy
from sensor_msgs.msg import NavSatFix
import queue
import websocket
import json
import threading
import signal
import time
import os
class RosThread(threading.Thread):
    def callback(self, data):
        """
        callback for current pose
        """
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
            ws_thread.queue.put({'data': json_data})
    def run(self):
        """
        main loop
        """
        role_name = rospy.get_param('/role_name', 'ego_vehicle')
        rospy.Subscriber('/carla/{}/gnss'.format(role_name), NavSatFix, self.callback)
        rospy.spin()


class WebSocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ws = None
        self.queue = queue.Queue()
        print("init queue")
    def run(self):
        """
        main loop
        """
        self.ws = websocket.WebSocketApp("ws://localhost:8764", on_open=self.on_open)
        print("websocket start")
        self.ws.run_forever()
        print("run_forever")

    def on_open(self, ws):
        """
        WebSocket on open callback
        """
        print("start on open")
        try:
            while True:
                if not self.queue.empty():
                    msg = self.queue.get()
                    json_data = json.dumps({'data': msg['data']})
                    self.ws.send(json_data)
                    print(json_data)
                time.sleep(0.001)
        except KeyboardInterrupt:
            print("Key Interrupt")


def handler_int():
    exit()

if __name__ == '__main__':
    #ip = '127.0.0.1'
    #port = 12347
    signal.signal(signal.SIGINT,handler_int)
    try:
        rospy.init_node('convert_odometry_to_pose', anonymous=True)
        ros_thread = RosThread()
        ws_thread = WebSocketThread()

        ros_thread.start()
        ws_thread.start()
        ros_thread.join(1000)
        ws_thread.join(1000)

    except KeyboardInterrupt:
        print("GET INTERRUPT")
        pass
    finally:
        print('\ndone.')
        