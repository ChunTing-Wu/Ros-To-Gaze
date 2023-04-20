import rospy
from sensor_msgs.msg import NavSatFix
import queue
import websocket
import json
import threading

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
        self.ws = websocket.WebSocketApp("ws://localhost:8765", on_open=self.on_open)
        print("websocket start")
        self.ws.run_forever()
        print("run_forever")

    def on_open(self, ws):
        """
        WebSocket on open callback
        """
        print("start on open")
        while True:
            if not self.queue.empty():
                msg = self.queue.get()
                json_data = json.dumps({'data': msg['data']})
                self.ws.send(json_data)
                print(json_data)

    def stop(self):
        """
        Stop WebSocket thread
        """
        self.ws.close()
        print("close")

if __name__ == '__main__':
    global ws_thread
    #ip = '127.0.0.1'
    #port = 12347

    rospy.init_node('convert_odometry_to_pose', anonymous=True)
    ros_thread = RosThread()
    ws_thread = WebSocketThread()

    ros_thread.start()
    ws_thread.start()
    ros_thread.join()
    ws_thread.join()