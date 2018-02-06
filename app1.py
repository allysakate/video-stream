#docker run --rm --name my-mongo -it -p 27017:27017 mongo
#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response

#connect to mongodb
import pymongo
import gridfs
from pymongo import MongoClient

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# connect to database     
    client = MongoClient('mongodb://localhost:27017/')
    client.drop_database('test')
# data base name : 'test'
    database = client.test
# create a new gridfs object.
    fs = gridfs.GridFS(database)

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    getcount = 1 
    while (getcount < camera.count()):
        print (getcount)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        strcount = str(getcount)
        storename = 'testimage'+ strcount
        stored = fs.put(frame,filename=storename)
        outputdata =fs.get(stored).read()     
        outfilename = '/Users/johnanthonyjose/Documents/flask1/mongo-images/'+strcount+'.jpg'
        output= open(outfilename,'wb')   
        output.write(outputdata)
        getcount = getcount + 1   
        output.close()
    fsimage = fs.list()
    print(fsimage)   

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
