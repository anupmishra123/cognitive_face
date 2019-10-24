from flask import Flask,render_template,url_for,request,flash,redirect
#from couchbase.cluster import Cluster
#from couchbase.cluster import PasswordAuthenticator
#cluster = Cluster('couchbase://localhost:8091')
#authenticator = PasswordAuthenticator('Admin', 'Amol@1996')
#cluster.authenticate(authenticator)
#cb = cluster.open_bucket('MyBucket')
from flask import Flask,render_template,url_for,flash,redirect
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import os
import cv2
from gridfs import GridFS
from pymongo import MongoClient
from flask import make_response
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
import cognitive_face as CF
from cognitive_face.face import detect

app = Flask(__name__,template_folder='template')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = 'static'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
'''app.config["MONGO_DBNAME"]= "myMongoDB"'''
app.config['MONGO_URI'] ="mongodb://localhost:27017/myMongoDB"
mongo = PyMongo(app)


@app.route("/")
def index():
    
    set={''}
    
    l=[]
    row_iter = mongo.db.user1.find()
    for row in row_iter:
        l.append(row)
    for i in l:
        for k,v in i.items():
            if k=='ClientName':
                set.add(v)
    return render_template('index.html',result=l,set=set)	
@app.route("/test", methods=['GET','POST'])
def test():
    set={''}
    set_cus={''}
    select = request.values.get('comp_select')
    var=str(select)
    l=[]
    row_iter = mongo.db.user1.find()
    for row in row_iter:
        l.append(row)
    for i in l:
        for k,v in i.items():
            if v==var:
                set_cus.add(i['CustomerName'])
    print(set_cus)
    return  render_template('index.html',result=l,r=var,set=set,set2=set_cus)
@app.route("/test2" , methods=['GET','POST'])
def test2():
    set={''}
    set_cus={''}
    select = request.values.get('comp_select2')
    var=str(select)
    row_iter = mongo.db.user1.find()
    l=[]
    row_iter = mongo.db.user1.find()
    for row in row_iter:
        l.append(row)
    for i in l:
        for k,v in i.items():
            if k=='ClientName':
                set.add(v)
            if v==var:
                set_cus.add(i['CustomerName'])
    print("user value")
    user = mongo.db.user1.find({'CustomerName' : var})
    print(user)
    #expression = 
    return render_template(f'''index.html''',result=l,r=var,cusName=var,user=user,set=set,set2=set_cus)
@app.route('/a')
def indexx():
    getpic()
    return render_template('frm.html')

@app.route('/create', methods=['POST','GET'])
def create():
     
    if 'img' in request.files:
        f = request.files['img']
        imgnm=request.form.get('cid')+'.jpg'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(imgnm)))
        #expretion=getExpretions(imgnm)
        mongo.db.user1.insert({'ClientName' : request.form.get('ClientName'),'CustomerName' : request.form.get('cn'),'date' : request.form.get('date'), 'profile_image_name' :imgnm})
        return '''<center><h1 style="color:blue;">Client Registered successfully..!</h1></center>
          <center><a href="/a" class="previous">&laquo; GO for next client registration..!</a></center>
            '''
    else:
        return '''<center><h1 style="color:blue;">Client Not Registered Correctly..try again!</h1></center>
          <center><a href="/a" class="previous">&laquo; Previous</a></center>
            '''

def getExpretions(imgnm):
    KEY = "2609d590d76d4d4ca5d5cba9742f2dcf"
    ENDPOINT = "https://face-exp.cognitiveservices.azure.com/face/v1.0"
    CF.Key.set(KEY)
    CF.BaseUrl.set(ENDPOINT)
    img1 ='static/'+imgnm
    #+user['profile_image_name']
    img2 ='Raspi/101.png'
    face_model1 = detect(img1, attributes='emotion')
    print(face_model1)
    for i,j in enumerate(face_model1):
        print(j.get('faceId'))
    face_id1 = face_model1[0]['faceId']
    print(face_id1)
    face_model2 = detect(img2, attributes='emotion')
    print(face_model2)
    similar = []
    for i in face_model2:
        similar.append(i.get('faceId'))
    print(similar)
    identified = CF.face.find_similars(face_id = face_id1, face_ids = similar)
    confidence = identified[0]['confidence']
    return confidence

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


def profile(CustomerName):
    user = mongo.db.user1.find_one_or_404({'CustomerName' : CustomerName})
    return user

@app.route('/profile/<CustomerName>')
def profile2(CustomerName):
    select = request.values.get('comp_select2')
    var=str(select)
    user = mongo.db.user1.find_one_or_404({'CustomerName' : CustomerName})
    return f'''
        <h1>{var}</h1>
        <img src = "{url_for('file', filename=user['profile_image_name'])}">
    '''
#@app.route('/getpic')
def getpic():
    camera = cv2.VideoCapture(0)
    while(True):
        ret, img = camera.read()
    
        cv2.imshow('image', img)
        cv2.imwrite('0001.jpg',img)

        if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
            camera.release()
            cv2.destroyAllWindows()
            break    
    return "Done"
if __name__ == "__main__":
	app.run(debug=True)
    

