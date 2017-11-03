import phd2_client
from luma.core.render import canvas


from collections import deque


class GuidingGraph:
    def __init__(self, max_points):
        self.points_ra = deque([], max_points)
        self.points_dec = deque([], max_points)

    def update(self, points_ra, points_dec):
        self.points_ra.clear()
        self.points_dec.clear()
        self.points_ra.append(points_ra)
        self.points_dec.append(points_dec)

    def render(self, canvas):
        pass

class LumaUserInterface:
    def __init__(self, device):
        self.status = phd2_client.PHD2Status.Stopped
        self.alert = None
        self.device = device
        self.guiding_graph = GuidingGraph(self.max_guide_points())

    def update_graph(self, points_ra, points_dec):
        self.guiding_graph.update(points_ra, points_dec)

    def update_status(self, status):
        pass

    def show_alert(self, message):
        pass

    def max_guide_points(self):
        return 80

    def render(self):
        with canvas(self.device) as draw:
            self.guiding_graph.render(draw)

