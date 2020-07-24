"""
# simple example:
from utils.ble import bleuart

def on_data_received(connection, data):
    print(str(data))

uart = bleuart.BLEUART(name='octopus', on_data_received=on_data_received)
uart.start()
"""

__version__ = "1.0.0"

import struct

import bluetooth
from micropython import const


# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)


# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(
    limited_disc=False,
    br_edr=False,
    name=None,
    services=None,
    appearance=0
):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)),
    )

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    # See org.bluetooth.characteristic.gap.appearance.xml
    _append(_ADV_TYPE_APPEARANCE, struct.pack("<h", appearance))

    return payload


_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_NOTIFY,
)
_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    bluetooth.FLAG_WRITE,
)
_SERVICE = (
    _UUID,
    (_TX, _RX,),
)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_COMPUTER = const(128)

_IRQ_CENTRAL_CONNECT = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT = const(1 << 1)
_IRQ_GATTS_WRITE = const(1 << 2)

_ble = bluetooth.BLE()


class BLEUARTConnection:
    def __init__(self, conn_handle, tx_handle):
        self._conn_handle = conn_handle
        self._tx_handle = tx_handle

    def write(self, data):
        _ble.gatts_notify(self._conn_handle, self._tx_handle, data)

    def close(self):
        _ble.gap_disconnect(self._conn_handle)


class BLEUART:

    def __init__(self, name, on_data_received=None, on_connection_made=None, rxbuf=100):
        self._rx_buf = rxbuf
        self._connections = dict()
        self._on_data_received = on_data_received
        self._on_connection_made = on_connection_made
        # Optionally add services=[_UART_UUID], but this is likely to make the payload too large.
        self._advertising_payload = advertising_payload(
            name=name,
            appearance=_ADV_APPEARANCE_GENERIC_COMPUTER
        )

    def start(self):
        _ble.active(True)
        _ble.irq(handler=self._irq)

        ((self._tx_handle, self._rx_handle,),) = _ble.gatts_register_services(
            (_SERVICE,)
        )
        # Increase the size of the rx buffer and enable append mode.
        _ble.gatts_set_buffer(self._rx_handle, self._rx_buf, True)
        self._advertise()

    def _irq(self, event, data):
        try:
            self._IRQ_HANDLERS[event](self, data)
        except KeyError:
            pass

    def _irq_central_connect(self, data):
        conn_handle, _, _ = data
        self._connections[conn_handle] = connection = BLEUARTConnection(
            conn_handle, self._tx_handle
        )
        if self._on_connection_made:
            self._on_connection_made(connection)

    def _irq_central_disconnect(self, data):
        conn_handle, _, _ = data
        if conn_handle in self._connections:
            del self._connections[conn_handle]
        # Start advertising again to allow a new connection.
        self._advertise()

    def _irq_gatts_write(self, data):
        conn_handle, value_handle = data
        if value_handle != self._rx_handle:
            return

        try:
            connection = self._connections[conn_handle]
        except KeyError:
            return

        received_data = _ble.gatts_read(self._rx_handle)
        if self._on_data_received:
            self._on_data_received(connection, received_data)

    _IRQ_HANDLERS = {
        _IRQ_CENTRAL_CONNECT: _irq_central_connect,
        _IRQ_CENTRAL_DISCONNECT: _irq_central_disconnect,
        _IRQ_GATTS_WRITE: _irq_gatts_write,
    }

    def _advertise(self, interval_us=500000):
        _ble.gap_advertise(interval_us, adv_data=self._advertising_payload)
