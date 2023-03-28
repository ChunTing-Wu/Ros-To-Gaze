# Ros-To-Gaze
Using ROS to send data via UDP and updating the information to Gaze on Google Maps

# Prerequisite
* Install Autoware.AI, because we need to use the "NavSatFix" message format.
* Install the Python Django framework to display geographical messages on Google Maps.
* This demo requires Python 3.8 or higher version.
* Using pip command to install Django below
```shell=
    pip install django
```
# How to use
```shell=
python manage.py runserver 8001
```

# Self-reminder
* START alienware env
```shell=
conda env list
conda activate "Python3 env"
```
* Install django-admin
```shell=
django-admin startproject ncku_gnss_demo
```