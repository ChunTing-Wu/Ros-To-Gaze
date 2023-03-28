#!/usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
"""
receive nav_msgs::Odometry and publish geometry_msgs::PoseStamped
"""
import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import NavSatFix

import json
import socket

ip = '127.0.0.1'
port = 12347
socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def callback(data):
    """
    callback for current pose
    """
    global ip, port, socket_udp
    latitude = data.latitude
    longitude = data.longitude

    data = {
    "latitude": latitude,
    "longitude": longitude
    }
    json_data = json.dumps(data)
    socket_udp.sendto(json_data, (ip, port))
    
    print(json_data)


def convert_odometry_to_pose():
    """
    main loop
    """
    global socket_udp
    rospy.init_node('convert_odometry_to_pose', anonymous=True)
    role_name = rospy.get_param('/role_name', 'ego_vehicle')
    rospy.Subscriber('/carla/{}/gnss'.format(role_name), NavSatFix, callback)
    rospy.spin()
    socket_udp.close()


if __name__ == '__main__':
    convert_odometry_to_pose()
