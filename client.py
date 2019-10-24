import asyncio
import websockets
import cv2
import time
from PIL import Image
from io import BytesIO
import base64
#import RPi.GPIO as GPIO
from time import sleep
#from picamera.array import PiRGBArray
#from picamera import PiCamera

#host = "172.16.130.37"
host = "172.16.62.250"
port = 8089
cam=cv2.VideoCapture(0)
data= ""
cam.set(3,800);
cam.set(4, 600);
async def hello():
    uri = "ws://{}:{}".format(host, port)
    print("hello")
    async with websockets.connect(uri) as websocket:
        ret,frame=cam.read()
        #cv2.resize(frame, (80,60))
        cv2.imwrite("demo.png",frame)
        with open("demo.png","rb") as image_file:
            data = base64.b64encode(frame)
        await websocket.send(data)
        
        greeting = await websocket.recv()
    camera.release()
    cv2.destroyAllWindows()


while True:
    asyncio.get_event_loop().run_until_complete(hello())
