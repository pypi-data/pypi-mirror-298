from obstechutils.cameras.asi import RegionOfInterest, AsiCamera
from matplotlib import pylab as plt
import time 
import numpy as np



def quick_photo(width=3096, height=2080):

    exposure_time = 0.0005
    model = 'ZWO ASI178MM' 
    with AsiCamera(model=model).open(exposure_time=0.001, gain=400) as camera:
        I = camera.capture()
    plt.imshow(I)

model = 'ZWO ASI178MM' 
camera = asi.Camera(0)
xmax, ymax = cam.get_roi()[2:]
nframes = 50
with camera.open(video=True, exptime=0.0005) as cam:
    for axis in 0, 1:
        for n in [80, 160, 320, 640, 1280]:
                 
            x, y = n, 2080
            if axis == 1:
                x, y = y, x
            print(x, y)
            if x > xmax or y > ymax:
                raise RuntimeError('wrong size')
            cam.set_roi(width=x, height=y, bins=1)

            cam.start_video_capture()
            I = np.zeros((y, x), dtype=int)
            t0 = time.time()
            for i in range(nframes):
                I += cam.capture_video_frame()
            t1 = time.time()
            rate = nframes / (t1 - t0)
            cam.stop_video_capture()

            print(f"capture_video_frame {x} x {y}: {rate:.1f} fps")

