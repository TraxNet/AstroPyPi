import logging
import argparse
import phd2_client

logger = logging.getLogger()

def setup_loging(logilepath):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = logging.FileHandler(logilepath, mode='w')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TraxNet AstroPi')
    parser.add_argument('--server', type=str, help='PHD2 Server Address', default="localhost")
    parser.add_argument('--port', type=int, help='PHD2 Server Port', default=4400)

    setup_loging()

    args = parser.parse_args()
    server = args.server
    port = args.port

    client = phd2_client.PHD2Client(server, port)
    client.init()

    while True:
        pass
