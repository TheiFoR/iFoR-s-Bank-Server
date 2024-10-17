import sys

sys.path.append('../../logger')

from logger import logger
import threading
import struct

from socket import socket


class BaseClientHandler(threading.Thread):
    _socket: socket = None
    _address = None
    message_handler: dict = None
    answer_to_message: dict = None

    def __init__(self, client_socket: socket, address):
        super().__init__()
        self._socket = client_socket
        self._address = address

    def parse_message(self, data: bytes) -> (int, bytes):
        if len(data) == 0:
            logger.warning("Received data is empty")
            return 0, b''

        command_id = int.from_bytes(data[0: 2], byteorder='little')
        parameters = {}

        message_bytes = data[2:]

        i = 0
        while i < len(message_bytes):
            name_size = int.from_bytes(message_bytes[i: i + 2], byteorder='little')
            size = int.from_bytes(message_bytes[i + 2: i + 4], byteorder='little')
            name = message_bytes[i + 4: i + 4 + name_size].decode('utf-8')
            parameters[name] = message_bytes[i + 4 + name_size: i + 4 + name_size + size]
            i = i + 4 + name_size + size

        return command_id, parameters

    def run(self):
        logger.info(f'ClientHandler client - {self._address}')
        while True:
            data = self._socket.recv(1024)

            command_id, parameters = self.parse_message(data)

            logger.debug(f'ClientHandler command id {command_id}, parameters: {parameters}. Raw data: {data}')

            if self.message_handler is None:
                logger.warning("Message handler is None")
                continue

            if not dict(self.message_handler).keys().__contains__(command_id):
                logger.warning("Message handler is not contains command_id: " + str(command_id))
                continue

            code, response = self.message_handler[command_id](self, parameters)

            self.send(command_id, response)

            if code == -1:
                break

        logger.info(f'Client disconnected, job complete')

    def sendBytes(self, data: bytes):
        print("Send to:", self._socket.getsockname(), self._socket.getpeername())
        self._socket.sendall(data)

    def send(self, command_id, response):
        # Начинаем собирать сообщение
        message = bytearray()

        # Добавляем командный id
        message.append(command_id & 0xFF)
        message.append((command_id >> 8) & 0xFF)

        for name, item in response.items():
            # Определяем тип данных и обрабатываем их
            if isinstance(item, int):
                if item.bit_length() <= 16:  # short
                    value_format = 'h'  # short
                    bytes_data = self.get_prepare_bytes(name, value_format, item)
                elif item.bit_length() <= 64:  # long long
                    value_format = 'q'  # long long
                    bytes_data = self.get_prepare_bytes(name, value_format, item)
                else:
                    value_format = 'i'  # int
                    bytes_data = self.get_prepare_bytes(name, value_format, item)
            elif isinstance(item, str):
                value_format = 's'  # str
                bytes_data = self.get_prepare_bytes(name, value_format, item)
            else:
                raise TypeError(f"Unknown type for item: {type(item)}")

            message.extend(bytes_data)

        logger.debug(f"Message to send: {message}")
        self.sendBytes(message)

    def get_prepare_bytes(self, name: str, value_type: str, value, size=-1):
        if size == -1:
            size = struct.calcsize(value_type)
        else:
            size *= struct.calcsize(value_type)

        # Начинаем формировать байты результата
        result = bytearray()

        # Добавляем размер данных
        result.append(size & 0xFF)
        result.append((size >> 8) & 0xFF)

        # Добавляем размер имени
        result.append(len(name) & 0xFF)
        result.append((len(name) >> 8) & 0xFF)

        # Добавляем имя
        result.extend(name.encode('utf-8'))

        if value_type == 's':
            result.extend(value.encode())
        else:
            result.extend(struct.pack(value_type, value))

        return result
