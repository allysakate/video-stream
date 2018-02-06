import time
from base_camera import BaseCamera
from glob import glob
import pymongo
import gridfs
from pymongo import MongoClient

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imglist = glob('*.jpeg')
    imgs = [open(f,'rb').read() for f in imglist]
    imgcount = len(imglist) + 1

# connect to database name: 'test' and create a new gridfs object
    client = MongoClient('mongodb://localhost:27017/')
    database = client.test 
    fs = gridfs.GridFS(database)   

    @staticmethod
    def count():
        return Camera.imgcount

# store and get images to/from Database
    @staticmethod
    def frames():
        imgret = 1
        while (imgret < Camera.imgcount):
            strcount  = str(imgret)
            storename = 'testimage'+ strcount
            stored    = Camera.fs.put(Camera.imgs,filename=storename)
            retrieved = Camera.fs.get(stored).read()
            content_type = Camera.fs.content_type            
            time.sleep(0.5)
            yield retrieved[int(time.time()) % Camera.imgcount]
            imgret = imgret + 1  