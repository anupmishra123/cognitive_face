import asyncio
import websockets
import base64
import Picamera

host = "172.16.130.37"
port = 8081
data = ""
cam = picamera.Picamera()
cam.start_preview()
time.sleep(5)

async def hello():
    uri = "ws://{}:{}".format(host, port)
    print("hello")
    async with websockets.connect(uri) as websocket:
        cam.capture("demo.jpg")
        with open("demo.jpg", "rb") as image_file:
            data = base64.b64encode(image_file.read())
        await websocket.send(data)

        greeting = await websocket.recv()


while True:
    asyncio.get_event_loop().run_until_complete(hello())