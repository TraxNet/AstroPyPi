import phd2_client
import os
import logging
import threading
from luma.core.render import canvas
from PIL import ImageFont

logger = logging.getLogger('astropypi')

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


class GuidingGraph:
    def __init__(self, max_points):
        self.points_ra = []
        self.points_dec = []
        self.offset_x = 2
        self.offset_y = 1
        self.list_lock = threading.Lock()

    def update(self, points_ra, points_dec):
        self.list_lock.acquire()
        self.points_ra = points_ra
        self.points_dec = points_dec

        self.list_lock.release()

    def point_to_screenspace(self, point):
        return (self.offset_x+point[0], self.offset_y+point[1]*30+30)

    def draw_points(self, draw, points, color):
        self.list_lock.acquire()
        prev = self.point_to_screenspace((0, 0.0))

        for index in range(len(points)):
            point = points[index]
            new_point = self.point_to_screenspace((index+1, point))
            draw.line([prev, new_point], fill=color)
            prev = new_point
        self.list_lock.release()

    def render(self, draw):
        draw.line([(self.offset_x, self.offset_y+30), (self.offset_x+90, self.offset_y+30)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y), (self.offset_x, self.offset_y+60)], fill=(128,128,128))

        draw.line([(self.offset_x, self.offset_y + 00), (self.offset_x + 2, self.offset_y + 00)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y + 10), (self.offset_x + 2, self.offset_y + 10)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y + 20), (self.offset_x + 2, self.offset_y + 20)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y + 40), (self.offset_x + 2, self.offset_y + 40)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y + 50), (self.offset_x + 2, self.offset_y + 50)], fill=(128, 128, 128))
        draw.line([(self.offset_x, self.offset_y + 60), (self.offset_x + 2, self.offset_y + 60)], fill=(128, 128, 128))

        self.draw_points(draw, self.points_dec, (255, 0, 0))
        self.draw_points(draw, self.points_ra, (0, 0, 255))

class LumaUserInterface:
    def __init__(self, device):
        self.status = phd2_client.PHD2Status.Stopped
        self.alert = None
        self.device = device
        self.guiding_graph = GuidingGraph(self.max_guide_points())
        self.alert_msg = None
        self.alert_time = 0.0
        self.alert_time_max = 5.0
        self.font = make_font("tiny.ttf", 8)

    def draw_status(self, draw):
        draw.text((30, 2), text=phd2_client.status_str(self.status), font=self.font, fill="red")

    def update_graph(self, points_ra, points_dec):
        self.guiding_graph.update(points_ra, points_dec)

    def update_status(self, status):
        pass

    def show_alert(self, message):
        pass

    def max_guide_points(self):
        return 80

    def render(self, delta):
        if self.alert_msg:
            self.alert_time -= delta;
            if self.alert_time <= 0.0:
                self.alert_msg = None
                self.alert_time = 0.0

        with canvas(self.device) as draw:
            self.guiding_graph.render(draw)

        self.draw_status(draw)