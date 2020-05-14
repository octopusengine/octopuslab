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
    adv_type_flags = (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)
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
    def __init__(self, uuid, flags, buffer_size=None, append=False):
        self.uuid = uuid
        self.flags = flags
        self.buffer_size = buffer_size
        self.append = append
        self.value_handle = None
        self._on_message_callback = lambda *_: None

    def __get__(self, instance, owner):
        return self

    def notify(self, conn_handle, data=None):
        blesync.gatts_notify(conn_handle, self.value_handle, data)

    def write(self, data):
        blesync.gatts_write(self.value_handle, data)

    def on_message(self, callback):
        self._on_message_callback = callback
        return callback


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
        characteristic._on_message_callback(self, conn_handle, received_data)

    def __init__(self, handles):
        self._characteristics = {}
        for characteristic, handle in zip(self.characteristics, handles):
            self._characteristics[handle] = characteristic
            characteristic.value_handle = handle
            if characteristic.buffer_size:
                blesync.gatts_set_buffer(
                    handle,
                    characteristic.buffer_size,
                    characteristic.append
                )


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
    ):
        self._service_classes = service_classes
        self._multiple_connections = multiple_connections
        self._service_by_handle = {}
        self._advertising_payload = _create_advertising_payload(
            name=name,
            appearance=appearance,
        )

    def start(self):

        blesync.active(True)
        services_declarations = _get_services_declarations(self._service_classes)
        all_handles = blesync.gatts_register_services(services_declarations)

        for handles, service_class in zip(
            all_handles,
            self._service_classes
        ):
            service = service_class(handles)
            for handle in handles:
                self._service_by_handle[handle] = service

        if self._multiple_connections:
            blesync.on_central_connect(self._advertise_on_central_connect)

        blesync.on_gatts_write(self._on_gatts_write)

        blesync.on_central_disconnect(self._on_central_disconnect)
        self._advertise()

    def _advertise(self, interval_us=500000):
        blesync.gap_advertise(interval_us, adv_data=self._advertising_payload)

    def _advertise_on_central_connect(self, conn_handle, addr_type, addr):
        # Start advertising again to allow multiple connections
        self._advertise()

    def _on_gatts_write(self, conn_handle, value_handle):
        service = self._service_by_handle[value_handle]
        service._on_gatts_write(conn_handle, value_handle)

    def _on_central_disconnect(self, conn_handle, addr_type, addr):
        # Start advertising again to allow a new connection.
        self._advertise()


on_connect = blesync.on_central_connect
on_disconnect = blesync.on_central_disconnect
