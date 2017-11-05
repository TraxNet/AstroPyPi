import logging
import argparse
import phd2_client
import luma_ui
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.emulator.device import pygame

logger = logging.getLogger('astropypi')

def setup_loging(logilepath):
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logilepath)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


if __name__ == "__main__":
    setup_loging("astropypi.log")

    parser = argparse.ArgumentParser(description='TraxNet AstroPi')
    parser.add_argument('--server', type=str, help='PHD2 Server Address', default="localhost")
    parser.add_argument('--port', type=int, help='PHD2 Server Port', default=4400)
    parser.add_argument('--i2c', type=int, help='Hex address for the i2c display. Default=0x3C', default=0x3C)
    args = parser.parse_args()


    #serial = i2c(port=1, address=args.port.i2c)
    #device = ssd1306(serial, rotate=0)
    #device = emulator(1, 2, 3, 'RGB', 'none', 6)
    device = pygame(96, 64)

    ui_client = luma_ui.LumaUserInterface(device)

    client = phd2_client.PHD2Client(args.server, args.port, ui_client, 6.05, 714)
    client.init()
    device.show()

    client.init()

    while True:
        ui_client.render(0.1)
        time.sleep(0.1)

