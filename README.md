# Ros-To-Gaze
Using ROS to send data via WebSocket and updating the information to Gaze on Open Street Map


If you wanna to observe specific node, simply modify "Python_GoogleMap".


Please modify the IP address to your fixed IP in the following files:

Server:
index.html
WebSocketTest
Client:
Python_Googlemap
The default ports are as follows:

Port: 8764
WebServer: 7771
To ensure successful connection, please follow these steps:

Start the server before running the client.
If you encounter connection issues, please disable all firewalls by executing the command:
```shell=
sudo ufw disable
```
Disclaimer  :  Please note that modifying the IP address and disabling firewalls should be done cautiously, as it may have security implications.




# Server run in Python3
```shell=
pip3 install websocket
python3 WebSocketTest.py
```

The server needs to run in a Python 3.

# Client run in Python2
```shell=
pip install websocket
python 
```

The client needs to run in a Python 2 with ROS.

