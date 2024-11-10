from logger import logger

from tcp_connection.client import Client
from tcp_connection.server import Server

server = Server('127.0.0.1', 1310, Client)

def main():
    logger.info("Start iFoR's Bank Server program")

    server.start()


if __name__ == '__main__':
    main()
