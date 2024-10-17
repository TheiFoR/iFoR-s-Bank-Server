from client_handler import ClientHandler
from logger import logger
import settings
from server import Server
from TCPConnection.server import Server

server = Server('127.0.0.1', 1310, ClientHandler)

def main():
    logger.info("Start iFoR's Bank Server program")

    server.start()


if __name__ == '__main__':
    main()
