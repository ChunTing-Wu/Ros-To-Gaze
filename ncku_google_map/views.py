from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import socket
import time
import json
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'index.html',{})



@csrf_exempt
def GETGPS(request):
    #global test

    UDP_IP = '127.0.0.1'
    UDP_PORT = 12347
    TEMPTIME = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP,UDP_PORT))
    lat_data = 0
    lon_data = 0
    while TEMPTIME < 10:
        data, addr = sock.recvfrom(1024)
        data_dict = json.loads(data.decode('utf-8'))
        lat_data = data_dict.get("latitude")
        lon_data = data_dict.get("longitude")
        TEMPTIME += 1
    sock.close()

#    return HttpResponse(JsonResponse({"lat": obj["latitude"],"lon":obj["longitude"]}))
    return HttpResponse(JsonResponse({"lat": lat_data,"lon": lon_data}))


