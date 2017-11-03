import logging
import argparse
import phd2_client
import luma_ui
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.emulator.device import pygame

logger = logging.getLogger()

def setup_loging(logilepath):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = logging.FileHandler(logilepath, mode='w')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)


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
    device = pygame()

    ui_client = luma_ui.LumaUserInterface(device)

    client = phd2_client.PHD2Client(args.server, args.port, ui_client, 6.05, 714)
    device.show()

    client.init()

    while True:
        ui_client.render()
        time.sleep(0.1)

