# The MIT License (MIT)
# Copyright (c) 2019-2020 Jan Cespivo

__version__ = "1.0.2"

import bluetooth

import blesync_client


class UARTService(blesync_client.Service):
    uuid = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")

    _rx = blesync_client.Characteristic(
        bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    )
    _tx = blesync_client.Characteristic(
        bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    )

    on_message = _tx.on_notify

    def send(self, message, ack=False):
        self._rx.write(message, ack)
