from dd.ph import *
import cv2, time

class Camera:
    def __init__(self, config):
        self.config = config
        self.capture = None
        self.init()
        job.run('dd_demo_camera_{0}'.format(self.name), self.start, [])

    def init(self):
        config = self.config
        self.name = config.name
        if self.capture:
            self.capture.release()
        self.capture = cv2.VideoCapture(config.value)
        self.framerate = int(self.capture.get(5))
        self.sleeptime = 1.0 / self.framerate
        self.frame = None
        if config.size:
            self.capture.set(3, config.size[0])
            self.capture.set(4, config.size[1])
        ret, self.frame = self.capture.read()

    def start(self):
        while True:
            ret, self.frame = self.capture.read()            
            if not ret:
                time.sleep(5)
                self.init()
            else:
                time.sleep(self.sleeptime)

    def read(self):
        if self.frame is None: return None
        imgbytes = cv2.imencode('.png', self.frame)[1].tobytes()
        return imgbytes

store = dd.dynamic()
def Sets(json):
    global store
    models = jh.Decode(json)
    for model in models:
        store[model.name] = model

cameraCache = MemoryCache()
def Read(name):
    def keyFn(keydata):
        return 'dd_demo_camera_{0}'.format(keydata)
    def dataFn(keydata):
        if store[keydata]:
            return Camera(store[keydata])
    camera = cameraCache.find(name, keyFn, dataFn)
    if not camera: return None
    return camera.read()