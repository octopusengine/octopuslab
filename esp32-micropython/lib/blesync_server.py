# The MIT License (MIT)
# Copyright (c) 2019-2020 Jan Cespivo

__version__ = "1.0.2"

import struct
from micropython import const
import blesync

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

_ADV_IND = const(0x00)
'''
Known as Advertising Indications (ADV_IND), where a peripheral device requests connection to any central device (i.e., not directed at a particular central device).
Example: A smart watch requesting connection to any central device.
'''
_ADV_DIRECT_IND = const(0x01)
'''
Similar to ADV_IND, yet the connection request is directed at a specific central device.
Example: A smart watch requesting connection to a specific central device.
'''
_ADV_SCAN_IND = const(0x02)
'''
Similar to ADV_NONCONN_IND, with the option additional information via scan responses.
Example: A warehouse pallet beacon allowing a central device to request additional information about the pallet. 
'''
_ADV_NONCONN_IND = const(0x03)
'''
Non connectable devices, advertising information to any listening device.
Example: Beacons in museums defining proximity to specific exhibits.
'''


# Generate a payload to be passed to gap_advertise(adv_data=...).
def _create_advertising_payload(
    limited_disc=False,
    br_edr=False,
    name=None,
    services=None,
    appearance=0  # UNKNOWN
):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    # some combinations of flags aren't allowed TODO describe
    adv_type_flags = (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)
    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", adv_type_flags),
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


class Characteristic:

    def encode(self, decoded):
        return decoded

    def decode(self, encoded):
        return encoded

    def __init__(self, uuid, flags, buffer_size=None, buffer_append=False):
        self.uuid = uuid
        self.flags = flags
        self._buffer_size = buffer_size
        self._buffer_append = buffer_append
        self._value_handle = None
        self._on_write_callback = lambda *_: None

    def __get__(self, service, service_class):
        # for cpython compliance
        # in micropython cls.attribute doesn't invoke __get__
        if service is None:
            return self

        return ServerServiceCharacteristic(service.connections, self._value_handle)

    def __set__(self, service, value):
        blesync.gatts_write(self._value_handle, self.encode(value))

    def set_value_handle(self, value_handle):
        if self._buffer_size:
            blesync.gatts_set_buffer(
                value_handle,
                self._buffer_size,
                self._buffer_append
            )
        self._value_handle = value_handle

    def call_write_callback(self, service, conn_handle, received_data):
        return self._on_write_callback(
            service,
            conn_handle,
            self.decode(received_data)
        )

    # if write flag
    def on_write(self, callback):
        self._on_write_callback = callback
        return callback


class ServerServiceCharacteristic:
    def __init__(self, connections, value_handle):
        self._connections = connections
        self.value_handle = value_handle

    def notify(self, conn_handle, data=None):
        blesync.gatts_notify(conn_handle, self.value_handle, data)

    def notify_multiple(self, conn_handles, data=None):
        for conn_handle in conn_handles:
            self.notify(conn_handle, data=data)

    def notify_all(self, data=None):
        self.notify_multiple(self._connections, data=data)


class Service:
    characteristics = tuple()  # TODO it won't be needed in py 3.6

    @classmethod
    def get_characteristics_declarations(cls):
        return [
            (characteristic.uuid, characteristic.flags)  # TODO BLE descriptors
            for characteristic in cls.characteristics
        ]

    def _on_gatts_write(self, conn_handle, value_handle):
        received_data = blesync.gatts_read(value_handle)
        characteristic = self._characteristics[value_handle]
        characteristic.call_write_callback(self, conn_handle, received_data)

    def __init__(self, connections, handles):
        self.connections = connections
        self._characteristics = {}
        for characteristic, handle in zip(self.characteristics, handles):
            characteristic.set_value_handle(handle)
            self._characteristics[handle] = characteristic


def _get_services_declarations(service_classes):
    return [
        (service_class.uuid, service_class.get_characteristics_declarations())
        for service_class in service_classes
    ]


class Server:
    def __init__(self,
        name,
        *service_classes,
        multiple_connections=False,
        appearance=0,
        advertise_interval_us=50000,
    ):
        self._advertise_interval_us = advertise_interval_us
        self._service_classes = service_classes
        self._multiple_connections = multiple_connections
        self._service_by_handle = {}
        self._advertising_payload = _create_advertising_payload(
            name=name,
            appearance=appearance,
        )
        self.connections = []

    def start(self):

        blesync.activate()
        services_declarations = _get_services_declarations(self._service_classes)
        all_handles = blesync.gatts_register_services(services_declarations)

        services = []

        for handles, service_class in zip(
            all_handles,
            self._service_classes
        ):
            service = service_class(self.connections, handles)
            services.append(service)
            for handle in handles:
                self._service_by_handle[handle] = service

        blesync.on_central_connect(self._on_central_connect)
        blesync.on_central_disconnect(self._on_central_disconnect)
        blesync.on_gatts_write(self._on_gatts_write)
        self._advertise()
        return services

    def _advertise(self):
        blesync.gap_advertise(
            self._advertise_interval_us,
            adv_data=self._advertising_payload
        )

    def _on_central_connect(self, conn_handle, addr_type, addr):
        self.connections.append(conn_handle)
        if self._multiple_connections:
            # Start advertising again to allow multiple connections
            self._advertise()

    def _on_gatts_write(self, conn_handle, value_handle):
        service = self._service_by_handle[value_handle]
        service._on_gatts_write(conn_handle, value_handle)

    def _on_central_disconnect(self, conn_handle, addr_type, addr):
        self.connections.remove(conn_handle)
        # Start advertising again to allow a new connection.
        self._advertise()


on_connect = blesync.on_central_connect
on_disconnect = blesync.on_central_disconnect
