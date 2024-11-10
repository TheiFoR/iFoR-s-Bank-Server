import json
import struct
import sys

import enums.types
from enums.types import MetaData

sys.path.append('../new_types')

from new_types.package import Package

class ByteParser:
    @staticmethod
    def parse(data: bytes) -> Package:
        package_id = ByteParser.to_int(data[:2], 'H')
        package_data = ByteParser.deserialize(data[2:])
        return Package(package_id, package_data)

    @staticmethod
    def unparse(package: Package) -> bytes:
        data = ByteParser.from_int(package.id, 'H')
        data += ByteParser.serialize(package.data)
        return data

    @staticmethod
    def serialize(data: dict) -> bytes:
        byte_data = bytearray()

        byte_data.extend(struct.pack('>I', len(data)))

        for key, value in data.items():
            key_bytes = key.encode('utf-16be')
            key_len = len(key_bytes)
            byte_data.extend(struct.pack('>I', key_len))
            byte_data.extend(key_bytes)

            # Сериализация значения
            if isinstance(value, int):  # Если значение целое
                byte_data.extend(struct.pack('>I', MetaData.int))
                byte_data.extend(b'\x00')
                byte_data.extend(struct.pack('>i', value))
            elif isinstance(value, float):
                byte_data.extend(struct.pack('>I', MetaData.double))
                byte_data.extend(b'\x00')
                byte_data.extend(struct.pack('>d', value))
            elif isinstance(value, str):
                byte_data.extend(struct.pack('>I', MetaData.string))
                byte_data.extend(b'\x00')
                byte_data.extend(struct.pack('>I', len(value)*2))
                byte_data.extend(value.encode('utf-16be'))
            else:
                print(f"Unsupported value type: {type(value)}")

        return byte_data

    @staticmethod
    def deserialize(data: bytes) -> dict:
        result = {}
        index = 0

        num_elements = struct.unpack_from('>I', data, index)[0]
        index += 4

        for _ in range(num_elements):
            key_length = struct.unpack_from('>I', data, index)[0]
            index += 4

            key = data[index:index + key_length].decode('utf-16be')
            index += key_length

            value_type = struct.unpack_from('>I', data, index)[0]
            index += 4
            index += 1

            if value_type == MetaData.int:
                value = int(struct.unpack_from('>i', data, index)[0])
                index += 4
            elif value_type == MetaData.longlong:
                value = int(struct.unpack_from('>q', data, index)[0])
                index += 8
            elif value_type == MetaData.double:
                value = float(struct.unpack_from('>d', data, index)[0])
                index += 8
            elif value_type == MetaData.string:
                value_size = int(struct.unpack_from('>i', data, index)[0])
                index += 4
                value = data[index:index + value_size].decode('utf-16be')
                index += 8
            else:
                raise ValueError(f"Unsupported QVariant type: {value_type}")

            result[key] = value

        return result

    @staticmethod
    def to_int(data: bytes, fmt: str) -> int:
        return struct.unpack(fmt, data)[0]

    @staticmethod
    def from_int(value: int, fmt: str) -> bytes:
        return struct.pack(fmt, value)