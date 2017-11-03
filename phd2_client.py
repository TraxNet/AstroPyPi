import phd2_socket
import thread
import logging
import time
from collections import deque

logger = logging.getLogger()

class PHD2Status:
    Stopped = 0
    Selected = 1
    Calibrating = 2
    Guiding = 3
    LostLock = 4
    Paused = 5
    Looping = 6

    def parse(str_value):
        if str_value == "Stopped":
            return PHD2Status.Stopped
        elif str_value == "Selected":
            return PHD2Status.Selected
        elif str_value == "Calibrating":
            return PHD2Status.Calibrating
        elif str_value == "LostLock":
            return PHD2Status.LostLock
        elif str_value == "Paused":
            return PHD2Status.Paused
        elif str_value == "Looping":
            return PHD2Status.Looping

def phd2client_worker(client, host, port):
    logging.info("Starting PHD2 Connection to " + host + ":" + port + "...")
    client_socket = phd2_socket.PH2Socket()
    client_socket.connect(host, port)
    logging.info("Connected")

    while client.abort != False:
        try:
            data = client_socket.receive()
            client.parse(data)
        except RuntimeError as e:
            logging.exception(e)
            break

    client_socket.disconnect()
    client.aborted = True

def is_type(data, str_type):
    return data["Event"] == str_type

def shift(list, value):
    list.rotate(1)
    list.popleft()
    list.appendleft(value)

class PHD2Client:
    def __init__(self, host, port, ui, pixel_size_um, focal_len_mm):
        self.ph2_status = PHD2Status.Stopped
        self.abort = False
        self.host = host
        self.port = port
        self.aborted = False
        self.ui = ui
        self.guide_points_ra = deque()
        self.guide_points_dec = deque()
        self.pixel_size = pixel_size_um
        self.focal_len = focal_len_mm

    def add_point(self, value_ra, value_dec):
        if len(self.guide_points_ra) > self.ui.get_max_points():
            shift(self.guide_points_ra, value_ra)
            shift(self.guide_points_dec, value_dec)
        else:
            self.guide_points_ra.appendleft(value_ra)
            self.guide_points_dec.appendleft(value_dec)

    def clear_points(self):
        self.guide_points_ra.clear()
        self.guide_points_dec.clear()

    def to_arcsecs(self, value):
        return self.pixel_size * self.focal_len * 206.265

    def init(self):
        self.phd2_worker_thread = thread.start_new_thread(phd2client_worker, (self, self.host, self.port))

    def close(self):
        self.abort = True
        while self.aborted != True:
            time.sleep(0.1)

    def process_guidestep(self, data):
        guide_ra = data["RADistanceGuide"]
        guide_dec = data["DecDistanceGuide"]

        self.add_point(self.to_arcsecs(guide_ra), self.to_arcsecs(guide_dec))
        self.ui.update_graph(self.guide_points_ra, self.guide_points_dec)


    def parse(self, data):
        logging.info("PHD2 Event: " + data)
        if is_type(data, "AppState"):
            self.status == PHD2Status.parse(data["State"])
        elif is_type(data, "StarLost"):
            self.ph2_status = PHD2Status.LostLock
        elif is_type(data, "Paused"):
            self.ph2_status = PHD2Status.Paused
        elif is_type(data, "LoopingExposuresStopped"):
            self.ph2_status = PHD2Status.Stopped
        elif is_type(data, "LoopingExposures"):
            self.ph2_status = PHD2Status.Looping
        elif is_type(data, "StartCalibration"):
            self.ph2_status = PHD2Status.Calibrating
        elif is_type(data, "GuideStep"):
            self.ph2_status = PHD2Status.Guiding
            self.process_guidestep(self, data)

        self.ui.update_status(self.ph2_status)