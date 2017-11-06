import phd2_client
import os
import logging
import threading
import math
from luma.core.render import canvas
from PIL import ImageFont


logger = logging.getLogger('astropypi')

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


class GuidingGraph:
    def __init__(self, width, height):
        self.points_ra = []
        self.points_dec = []
        self.offset_x = 2
        self.offset_y = 1
        self.list_lock = threading.Lock()
        self.width = width
        self.height = height

    def update(self, points_ra, points_dec):
        self.list_lock.acquire()
        self.points_ra = points_ra
        self.points_dec = points_dec

        self.list_lock.release()

    def point_to_screenspace(self, point, height):
        return (self.offset_x+point[0], self.offset_y+point[1]*height*0.5+height*0.5)

    def draw_points(self, draw, points, color, height):
        self.list_lock.acquire()
        prev = self.point_to_screenspace((0, 0.0), height)

        for index in range(len(points)):
            point = points[index]
            new_point = self.point_to_screenspace((index+1, point), height)
            draw.line([prev, new_point], fill=color)
            prev = new_point
        self.list_lock.release()

    def draw_axis(self, draw, height, increment):
        draw.line([(self.offset_x, self.offset_y), (self.offset_x, self.offset_y + self.height)], fill=(128, 128, 128))

        draw.line([(self.offset_x - 1, self.offset_y              ), (self.offset_x + 2, self.offset_y              )], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*1), (self.offset_x + 2, self.offset_y + increment*1)], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*2), (self.offset_x + 2, self.offset_y + increment*2)], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*3), (self.offset_x + self.width, self.offset_y + increment*3)], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*4), (self.offset_x + 2, self.offset_y + increment*4)], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*5), (self.offset_x + 2, self.offset_y + increment*5)], fill=(128, 128, 128))
        draw.line([(self.offset_x - 1, self.offset_y + increment*6), (self.offset_x + 2, self.offset_y + increment*6)], fill=(128, 128, 128))

    def render(self, draw, height, increment):
        self.draw_axis(draw, height, increment)

        self.draw_points(draw, self.points_dec, (255, 0, 0), height)
        self.draw_points(draw, self.points_ra, (0, 0, 255), height)

class LumaUserInterface:
    def __init__(self, device, width, height):
        self.status = phd2_client.PHD2Status.Stopped
        self.alert = None
        self.device = device
        self.max_points = width - 2
        self.height = height
        self.width = width
        self.guiding_graph = GuidingGraph(width, height)
        self.alert_msg = None
        self.alert_time = 0.0
        self.alert_time_max = 5.0
        self.font = make_font("tiny.ttf", 4)
        self.snr = None
        self.increments = math.ceil(height / 10)

    def draw_status(self, draw):
        status_text = phd2_client.status_str(self.status)
        textsize = draw.textsize(status_text, font=self.font)
        draw.text((94-textsize[0], self.height-6), text=status_text, font=self.font, fill="white", align="right")

        if self.snr:
            snr_text = "SNR: " + str(self.snr)
            textsize = draw.textsize(snr_text, font=self.font)
            draw.text((94-textsize[0], self.height-12), text=snr_text, font=self.font, fill="white")

    def update_snr(self, snr_value):
        self.snr = snr_value

    def update_graph(self, points_ra, points_dec):
        self.guiding_graph.update(points_ra, points_dec)

    def update_status(self, status):
        self.status = status

    def show_alert(self, message):
        pass

    def max_guide_points(self):
        return self.width-4

    def render(self, delta):
        if self.alert_msg:
            self.alert_time -= delta;
            if self.alert_time <= 0.0:
                self.alert_msg = None
                self.alert_time = 0.0

        with canvas(self.device) as draw:
            self.guiding_graph.render(draw, self.height, self.height / self.increments) # 3 arcsec width error in the graph
            self.draw_status(draw)