# Copyright (c) 2022, Eric Lemoine
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import base64
import json as _json

from .eio_types import JsonProtocol

(OPEN, CLOSE, PING, PONG, MESSAGE, UPGRADE, NOOP) = (0, 1, 2, 3, 4, 5, 6)
packet_names = {
    OPEN: "OPEN",
    CLOSE: "CLOSE",
    PING: "PING",
    PONG: "PONG",
    MESSAGE: "MESSAGE",
    UPGRADE: "UPGRADE",
    NOOP: "NOOP",
}

binary_types = (bytes, bytearray)


class Packet:
    """Engine.IO packet."""

    json: JsonProtocol = _json

    def __init__(self, packet_type=NOOP, data=None, binary=None, encoded_packet=None):
        self.packet_type = packet_type
        self.data = data
        if binary is not None:
            self.binary = binary
        elif isinstance(data, str):
            self.binary = False
        elif isinstance(data, (bytes, bytearray)):
            self.binary = True
        else:
            self.binary = False
        if encoded_packet:
            self.decode(encoded_packet)

    def encode(self, b64=False, always_bytes=True):
        """Encode the packet for transmission."""
        if self.binary and not b64:
            encoded_packet = bytes((self.packet_type,))
        else:
            encoded_packet = str(self.packet_type)
            if self.binary and b64:
                encoded_packet = "b" + encoded_packet
        if self.binary:
            if b64:
                encoded_packet += base64.b64encode(self.data).decode("utf-8")
            else:
                encoded_packet += self.data
        elif isinstance(self.data, str):
            encoded_packet += self.data
        elif isinstance(self.data, (dict, list)):
            encoded_packet += self.json.dumps(self.data, separators=(",", ":"))
        elif self.data is not None:
            encoded_packet += str(self.data)
        if always_bytes and not isinstance(encoded_packet, binary_types):
            encoded_packet = encoded_packet.encode("utf-8")
        return encoded_packet

    def decode(self, encoded_packet):
        """Decode a transmitted package."""
        b64 = False
        if not isinstance(encoded_packet, binary_types):
            encoded_packet = encoded_packet.encode("utf-8")
        elif not isinstance(encoded_packet, bytes):
            encoded_packet = bytes(encoded_packet)
        self.packet_type = encoded_packet[0:1][0]
        if self.packet_type == 98:  # 'b' --> binary base64 encoded packet
            self.binary = True
            encoded_packet = encoded_packet[1:]
            self.packet_type = encoded_packet[0:1][0]
            self.packet_type -= 48
            b64 = True
        elif self.packet_type >= 48:
            self.packet_type -= 48
            self.binary = False
        else:
            self.binary = True
        self.data = None
        if len(encoded_packet) > 1:
            if self.binary:
                if b64:
                    self.data = base64.b64decode(encoded_packet[1:])
                else:
                    self.data = encoded_packet[1:]
            else:
                try:
                    self.data = self.json.loads(encoded_packet[1:].decode("utf-8"))
                    if isinstance(self.data, int):
                        # do not allow integer payloads, see
                        # github.com/miguelgrinberg/python-engineio/issues/75
                        # for background on this decision
                        raise ValueError
                except ValueError:
                    self.data = encoded_packet[1:].decode("utf-8")

    def __repr__(self) -> str:
        return (
            f"Packet({packet_names[self.packet_type]}, "
            f"data={self.data if not isinstance(self.data, bytes) else '<binary>'})"
        )
