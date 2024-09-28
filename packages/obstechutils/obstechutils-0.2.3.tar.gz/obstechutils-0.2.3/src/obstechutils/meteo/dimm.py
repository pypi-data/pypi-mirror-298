from __future__ import annotations

from obstechutils.mqtt import MQTTClient
from obstechutils.dataclasses import strictdataclass
from obstechutils.cameras import RegionOfInterest, Subwindow, Camera

from mpmath import hyper
from pydantic.types import PositiveFloat
from pydantic import computed_field

from functools import cached_propertiy, lru_cache

from photutils.centroids import centroid_com as centroid
import cv2
import sys
import argparse
import json
import numpy as np
from astropy.time import Time
import time

arcsec = np.pi / 180 / 3600

DetBox: type = tuple[int, int, int, int]
DetDim: type = tuple[int, int]

def widen_box(box: DetBox, det_dim: DetDim, margin: int = 0):

    x0 = box[0] - widening
    y0 = box[1] + widening
    height = box[2] + 2 * widening
    width = box[2] + 2 * widening

    x0 += max(-x0, 0) + min(det_dim[2] - width - x0, 0)
    y0 += max(-y0, 0) + min(det_dim[3] - height - y0, 0)
    
    return x0, y, height, width

@strictdataclass
class DimmTelescope:

    hole_diameter: float # m
    hole_distance: float # m
    wavelength: float # m
    focal_length: float
    alt: float # degrees
    az: float = np.nan # degrees
 
    @computed_field
    @cached_property
    def airmass(self) -> float:
        return 1. / np.cos(np.deg2rad(self.alt))
    
    @computed_field
    @cached_property
    def ks(self) -> float:
        """

        """ 
        return 0.98 * (self.hole_diameter / self.wavelength) ** (1/5)

    # Formulae by Tokovinin (2002) replaced by exact ones by Sasiela (2007)
    # Discrepancy increases as holes get closer...

    @computed_field
    @cached_property
    def kl(self) -> float:
        b = self.b
        return 1 - 0.531 * b**(1/3) * float(hyper([-5/6,5/2,1/6,2/3], [5,3,-1/3], b**2))
    
    @computed_field
    @cached_property
    def kt(self) -> float:
        b = self.b
        return 1 - 0.799 * b **(1/3) * float(hyper([-5/6,5/2,1/6], [5,3], b**2))
    
    @computed_field
    @cached_property
    def b(self) -> float:
        return self.hole_diameter / self.hole_distance
x


@strictdataclass(config=dict(arbitrary_types_allowed=True))
class SingleDimmMeasurement(MQTTClient):

    camera: Camera 
    telescope: DimmTelescope
    exposure_time: float # s
    target: str
    start_time: int = 0
    max_motion: float = 6 # arcsec    
    period: float  # s

    def publish_seeing(self):

        payload = dict(
            description="zenithal seeing at 500 nm",
            longitudinal_seeing=self.seeing(direction=0),
            transverse_seeing=self.seeing(direction=1),
            longitudinal_seeing_bin2=self.seeing(direction=0, bin=2),
            transverse_seeing_bin2=self.seeing(direction=1, bin=2),
            target=self.target,
            altitude=self.alt,
            azimuth=self.az,
            wavelength=self.telescope.wavelength,
            reference_wavelength=500e-9,
            reference_altitude=90,
        )
        self.publish_json(payload=payload)

    @computed_field
    @cached_property
    def longitudinal_coherence_time(self) -> float:
        raise NotImplementedError()

    @computed_field
    @cached_property
    def transverse_coherence_time(self) -> float:
        raise NotImplementedError()

    @lru_cache
    def seeing(self, *, direction, bin=1) -> float:
        """The longitudinal and transverse seeing can be obtained
        with binning of the data to assess the amount of impact
        of the in-measurment atmospheric variations."""
        diff = self.differential_motion[direction]
        if bin > 1:
            diff = diff.reshape((-1, bin)).mean(axis=1)

        ks = self.telescope.ks
        kl = 0.364 * self.telescope.kl
        kt = 0.364 * self.telescope.kt
        seeing = ks * (np.var(diff) / kl) ** (3/5)

        secz = self.telescope.airmass
        lam = self.telescope.wavelength
        zenithal_correction = secz ** (3/5) * (lam / 500e-3) ** (1/5)
        nominal_seeing = seeing * zenithal_correction
        
        return nominal_seeing / arcsec

    @computed_field
    @cached_property
    def differential_motion(self) -> np.ndarray:

        # I clocked the centroid calculations at ~70 microseconds per
        # pair of subwindows on the Obstech DIMM machine, so we can do 
        # the calculation during the video
 
        roi = self.roi
        c1, c2 = [], []

        camera.exposure = self.exposure_time
        camera.roi = roi
        camera.video = True

        while Time.now().unix - self.start_time < self.period - 10:
            I = camera.capture().T
            I1 = I[win1.x1:win1.x2, win1.y1:win1.y2]
            I2 = I[win2.x1:win2.x2, win2.y1:win2.y2]
            c1.append(centroid(I1)) 
            c2.append(centroid(I2)) 
    
        camera.video = False       
 
        # first index is 1 in photutils
        c1 = np.array(c1) - 1
        c2 = np.array(c2) - 1
        
        scale = self.camera.pixel_size / self.telescope.focal_length

        c12_mean = c2.mean() - c1.mean()
        dc = c2 - c1 - c12_mean
        w12 = [win2.x1 - win1.x1, win2.y1 - win1.y1]
            
        theta = np.arctan2(c12_mean[1] + w12[1], c12_mean[0] + w12[0])
        sin = np.sin(theta)
        
        C, S = np.cos(theta), np.sin(theta)
        l12 = (dc[0] * C - dc[1] * S) * scale 
        t12 = (dc[0] * S + dc[1] * C) * scale
    
        # keep good values

        limit = self.max_motion
        keep = np.logical_and(l12.abs() < limit, t12.abs() < limit)

        return np.array(l12[keep], t12[keep])
 
    @computed_field
    @cached_property
    def _subwindows(self) -> tuple[RegionOfInterest, Subwindow, Subwindow]:
        """Take a few seconds of exposures to determine the positions of the 
        two DIMM images and determine an acceptable cropping of the full frame 
        as well as the subwindows for each image."""
         
        # Stack 5s of full frame video, i.e. about 115 frames
        # Could check without video but gain should probably be
        # changed and tested...
        kwargs = dict(exptime=2 * self.exposure_time, video=True)
        camera.video = True
        det_dim = camera.width, camera.height
        camera.exposure = 4 * self.exposure_time

        I = np.zeros(det_dim, dtype=int)    
        t0 = time.time()
        while time.time() - t0 < 5:
            I += cam.capture_video_frame().T

        camera.video = False

        # find contours on an image rescaled to 8 bits
        I = 200 * I / np.percentile(I, 99.9)
        I = I.astype(np.uint8).reshape(det_dim)
        ret, thresh = cv2.threadold(I, 3, 255, 0)
        contours, hierarchi = cv2.findContours( 
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # find the two brightest objects (most extended) and give a bounding 
        # box with 2 arcsec margin around contours.
        boxes = [cv2.boundingRect(c) for c in contours]
        boxes = sorted(boxes, key=lambda box: box[2]*box[3])
        box1, box2 = np.array(boxes[-2:])

        margin = int(2 / self.plate_scale + .5)
        box1 = widen_box(box1, det_dim, margin=margin)
        box2 = widen_box(box2, det_dim, margin=margin)

        # Ensure both star images fit well within a horizontal strip of at
        # least 12 arcsec (~60 pixels) 
        ymin = min(box1[1], box2[1])
        ymax = max(box1[1] + box1[3], box2[1] + box2[3])
        min_height = int(12 / self.plate_scale + .5)
        height = max(ymax - ymin, min_height)
        height = ((1 + height) // 2) * 2

        y0 = (ymin + ymax - height) // 2
        y0 = min(max(y0, 0), det_dim[1] - height)
        
        roi = RegionOfInterest(
            x0=0, 
            y0=y0, 
            width=det_dim[0],
            height=height,
        )

        # subwindows within it to be called like I[x0:x1, y0:y1] format.
        win1 = Subwindow(
            x0=box1[0],           y0=box1[1] - det_dim[1],
            x1=box1[0] + box1[2], y1=box1[1] + box1[3] - det_dim[1]
        )
        win2 = Subwindow(
            x0=box2[0],           y0=box2[1] - det_dim[1],
            x1=box2[0] + box2[2], y1=box2[1] + box2[3] - det_dim[1]
        )

        return roi, win1, win2

    @computed_field
    @property
    def region_of_interest(self) -> RegionOfInterest:
        """Returns a cropping of the image such as the two images of the DIMM fit."""
        return self._subwindows[0]

    @computed_field
    @property
    def subwindows(self) -> tuple[Subwindow, Subwindow]:
        """Returns the subwindows for each of the two DIMM images."""
        return self._subwindows[1:]


@strictdataclass
class DimmMonitor(MQTTClient):

    """Wait for MQTT message sent by NINA and launch a single
    seeing measurement."""

    camera_type: type
    camera_brand: str
    gain: int
    pixel_size: float
    exposure_time: float 
    
    def on_message(self, c, u, message):
        
        now = Time.now().unix
        payload = json.loads(message.decode)

        telescope = DimmTelescope(
            alt=payload.alt,
            az=payload.az,
            hole_diameter=payload['hole_diameter'],
            hole_distance=payload['hole_distance'],
            focal_length=payload['focal_length'],
        )

        camera = camera_type(name=camera_name)
        camera.gain = self.gain

        dimm = SingleDimmMeasurement(
            username=self.username,
            password=self.password,
            server=self.server,
            qos=self.qos,
            timeout=self.timeout,
            default_publish_topic=self.default_publish_topic,
            target=payload['target'],
            telescope=telescope,
            camera=camera,
            exposure_time=self.exposure_time,
            period=payload.get('period', 120),
            start_time=payload.get('time', now),
        )
        dimm.connect()
        dimm.publish_seeing()
