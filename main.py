import logging
import argparse
import phd2_client
import luma_ui
import time
import sys
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.emulator.device import pygame

logger = logging.getLogger('astropypi')


def setup_loging(logilepath):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if logilepath:
        # create file handler which logs even debug messages
        fh = logging.FileHandler(logilepath)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)

    ch.setFormatter(formatter)
    # add the handlers to the logger

    logger.addHandler(ch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TraxNet AstroPi')
    parser.add_argument('--server', type=str, help='PHD2 Server Address', default="localhost")
    parser.add_argument('--port', type=int, help='PHD2 Server Port', default=4400)
    parser.add_argument('--i2c', type=int, help='Hex address for the i2c display. Default=0x3C', default=0x3C)
    parser.add_argument('--log', type=str, help="Filepath to store logs. Default none", default=None)
    parser.add_argument('--focal', type=int, help="Focal Length of the guide scope in mm. Default=714mm", default=714)
    parser.add_argument('--pixsize', type=int, help="Pixel size of your CCD in microns (um). Default=6.05um", default=6.05)
    parser.add_argument('--simui', type=bool, help="If true, the UI will not use a i2c OLED display but a pygame based windows", default=False)
    args = parser.parse_args()

    setup_loging(args.log)

    device = None
    if args.simui:
        device = pygame(96, 64)
    else:
        serial = i2c(port=1, address=args.port.i2c)
        device = ssd1306(serial, rotate=0)

    ui_client = luma_ui.LumaUserInterface(device, 96, 60)

    client = phd2_client.PHD2Client(args.server, args.port, ui_client, args.pixsize, args.focal)
    client.init()
    device.show()

    client.init()

    while True:
        ui_client.render(0.1)
        time.sleep(0.1)

