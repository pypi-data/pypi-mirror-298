from obstechutils.cameras.asi import AsiCamera, RegionOfInterest

camera = AsiCamera(
    model='ZWO ASI1788MM', 
    pixel_size=2.4e-6,
    gain=400
)

def quick_capture(width, height):
    roi = RegionOfInterest(width=width, height=height)
    with camera.open(exptime=0.001) as camhandle:
        I = camhandle.capture()
    

