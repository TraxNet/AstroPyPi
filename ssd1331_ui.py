import phd2_client
from collections import deque

class SSD1331_UserInterface:
    def __init__(self):
        self.points_ra = deque(self.max_guide_points())
        self.points_dec = deque(self.max_guide_points())
        self.status = phd2_client.PHD2Status.Stopped
        self.alert = None

        pass

    def update_graph(self, points_ra, points_dec):
        self.points_ra.clear()
        self.points_dec.clear()
        self.points_ra.append(points_ra)
        self.points_dec.append(points_dec)
        pass

    def update_status(self, status):
        pass

    def show_alert(self, message):
        pass

    def max_guide_points(self):
        return 80

    def render(self):
        pass
