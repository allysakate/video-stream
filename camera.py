import time
from base_camera import BaseCamera
from glob import glob

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imglist = glob('*.jpeg')
    imgs = [open(f,'rb').read() for f in imglist]
    imgcount = len(imglist) + 1

    @staticmethod
    def count():
        return Camera.imgcount

    @staticmethod
    def frames():
        imgret = 1
        while (imgret < Camera.imgcount):
            time.sleep(0.5)
            yield Camera.imgs[int(time.time()) % Camera.imgcount]
            imgret = imgret + 1    
