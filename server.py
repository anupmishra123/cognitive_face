# import numpy as np
import cv2
import time
import base64
from PIL import Image
from io import BytesIO
import asyncio
import websockets
import numpy as np
import matplotlib.pyplot as plt
import cognitive_face as CF
from cognitive_face.face import detect
from datetime import datetime
from werkzeug.utils import secure_filename
import cognitive_face as CF
from cognitive_face.face import detect
import csv
host = "172.16.130.205"
#host = "172.16.130.37"
port = 8089

t = 0
time1 = [0]
sad_exp = [0.0]
#happy = 0.0
happy_exp = [0.0]
#neutral = 0.0
neutral_exp = [0.0]

print("Ready set go")
greeting = "hello"
async def hello(websocket, path): 
    global t
    global time1, sad_exp, happy_exp, neutral_exp
    data = await websocket.recv()
    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save('amol.png', 'PNG')
    KEY = "2609d590d76d4d4ca5d5cba9742f2dcf"
    ENDPOINT = "https://cec-facial-exp.cognitiveservices.azure.com/face/v1.0"
    CF.Key.set(KEY)
    CF.BaseUrl.set(ENDPOINT)
    img1 = 'C:/Users/anup.mishra1/Desktop/Flaskmongo-master/flask/static/amol.png'
    img2 = 'C:/Users/anup.mishra1/Desktop/Flaskmongo-master/flask/amol.png'
    face_model1 = detect(img1, attributes='emotion')
    #print("face model 1 result:")
    face_id1 = face_model1[0]['faceId']
   
    face_model2 = detect(img2, attributes='emotion')
   
    similar = []
    for i,j in enumerate(face_model2):   
       similar.append(j.get('faceId'))
    
    if len(similar) > 0:
        identified = CF.face.find_similars(face_id = face_id1, face_ids = similar)
    else:
        await websocket.send(greeting)
        identified=[]
    
    if len(identified) != 0:
        #sad = 0.0
        
        
        sad = face_model2[0]['faceAttributes']['emotion']['sadness']
        happy = face_model2[0]['faceAttributes']['emotion']['happiness']
        neutral = face_model2[0]['faceAttributes']['emotion']['neutral']
        #exp = [sad, happy, neutral]
        sad_exp.append(sad)
        happy_exp.append(happy)
        neutral_exp.append(neutral)
        '''       
        if sad > 0.50:
            #sad +=sad
            sad_exp.append(sad)
        elif happy > 0.50:
            #happy+=happy
            happy_exp.append(happy)
        elif neutral > 0.50:
            #neutral+=neutral
            neutral_exp.append(neutral)
        '''    
        f = open('expression.txt','a')
        f.write(str(neutral))
        f.close()    
    
        t+=15
        time1.append(t)
        time.sleep(1)       
        print(time1)
        print(sad_exp)
        print(happy_exp)
        print(neutral_exp)
        plt.plot(time1[1:], sad_exp[1:], time1[1:], happy_exp[1:], time1[1:], neutral_exp[1:])
        plt.xlabel('x - axis : Time') 
        plt.ylabel('y - axis : Expression')     
        plt.title('Experience') 
        plt.savefig('static/experience.jpg')
        await websocket.send(greeting) 
    else:
        await websocket.send(greeting)
        time.sleep(1)
        
      
      
    
    


start_server = websockets.serve(hello, host, port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
