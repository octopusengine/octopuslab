# The MIT License (MIT)
# Copyright (c) 2019-2020 Jan Cespivo

__version__ = "1.0.2"

from collections import namedtuple
import struct

import bluetooth
from micropython import const

import blesync

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)


def _next(iterator, default):
    try:
        return next(iterator)
    except StopIteration:
        return default


def _split_data(payload):
    i = 0
    result = []
    data = memoryview(payload)
    len_data = len(data)
    while i < len_data:
        length = data[i]
        result.append(data[i + 1:i + 1 + length])
        i += length + 1
    return result


def parse_adv_data(payload):
    return [(d[0], d[1:]) for d in _split_data(payload)]


def _find_adv_data(data, find_adv_type):
    for adv_type, payload in data:
        if adv_type == find_adv_type:
            yield payload


def decode_adv_name(data):
    payload = _next(_find_adv_data(data, _ADV_TYPE_NAME), None)
    if payload:
        return str(payload, "utf-8")
    return ''


def decode_adv_type_flags(data):
    payload = _next(_find_adv_data(data, _ADV_TYPE_FLAGS), None)
    if payload:
        return payload[0]


def decode_adv_services(data):
    services = []
    for payload in _find_adv_data(data, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<h", payload)[0]))
    for payload in _find_adv_data(data, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<d", payload)[0]))
    for payload in _find_adv_data(data, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(payload))
    return services


# TODO ADV_FLAGS
# _ADV_IND = const(0x00)
# '''
# Known as Advertising Indications (ADV_IND), where a peripheral device requests connection to any central device (i.e., not directed at a particular central device).
# Example: A smart watch requesting connection to any central device.
# '''
# _ADV_DIRECT_IND = const(0x01)
# '''
# Similar to ADV_IND, yet the connection request is directed at a specific central device.
# Example: A smart watch requesting connection to a specific central device.
# '''
# _ADV_SCAN_IND = const(0x02)
# '''
# Similar to ADV_NONCONN_IND, with the option additional information via scan responses.
# Example: A warehouse pallet beacon allowing a central device to request additional information about the pallet.
# '''
# _ADV_NONCONN_IND = const(0x03)
# '''
# Non connectable devices, advertising information to any listening device.
# Example: Beacons in museums defining proximity to specific exhibits.
# '''
# _ADV_SCAN_RSP = const(0x04)
# '''
# Scan response
# '''


Device = namedtuple(
    'Device',
    ('addr_type', 'addr', 'adv_name', 'adv_type_flags', 'rssi', 'services')
)


def scan(duration_ms, interval_us=None, window_us=None):
    """
    if it is interrupted during the iteration, the close() has to be called
    see https://github.com/micropython/micropython/issues/6183
    Example:
        scan_iter = scan(
            duration_ms=duration_ms,
            interval_us=interval_us,
            window_us=window_us,
        )

        for device in scan_iter:
            scan_iter.close()
            return device
    """

    blesync.activate()
    gap_scan_iter = blesync.gap_scan(
        duration_ms, interval_us=interval_us, window_us=window_us
    )
    try:
        for addr_type, addr, adv_type, rssi, adv_data in gap_scan_iter:
            parsed_data = parse_adv_data(adv_data)
            adv_name = decode_adv_name(parsed_data)
            adv_type_flags = decode_adv_type_flags(parsed_data)
            adv_services = decode_adv_services(parsed_data)
            yield Device(
                addr_type=addr_type,
                addr=addr,
                adv_name=adv_name,
                adv_type_flags=adv_type_flags,
                rssi=rssi,
                services=adv_services,
            )
    except GeneratorExit:
        gap_scan_iter.close()


class DeviceNotFound(Exception):
    pass


def find_device(name, duration_ms, interval_us=None, window_us=None):
    scan_iter = scan(
        duration_ms=duration_ms,
        interval_us=interval_us,
        window_us=window_us,
    )

    for device in scan_iter:
        if device.adv_name == name:
            scan_iter.close()
            return device

    raise DeviceNotFound()


class ConnectTimeoutError(Exception):
    pass


class Client:
    def __init__(self, *service_classes):
        self._service_classes = service_classes
        self._services = {}
        blesync.on_gattc_notify(self._on_notify)
        blesync.on_gattc_indicate(self._on_notify)

    def connect(self, addr_type, addr, timeout_ms=2000):
        # TODO separate connect and service creation
        blesync.activate()
        try:
            conn_handle = blesync.gap_connect(addr_type, addr, timeout_ms=timeout_ms)
        except blesync.GapConnectTimeoutError:
            raise ConnectTimeoutError

        if not self._service_classes:
            return {}

        ret = {}
        for start_handle, end_handle, uuid in blesync.gattc_discover_services(
            conn_handle
        ):
            for service_class in self._service_classes:
                try:
                    service = service_class(uuid, conn_handle, start_handle, end_handle)
                except ValueError:
                    continue
                else:
                    self._services.setdefault(conn_handle, []).append(service)
                    ret.setdefault(service_class, []).append(service)
        return ret

    def find_and_connect(
        self,
        device_name,
        scan_duration_ms=20000,
        scan_interval_us=30000,
        scan_window_us=30000,
        connect_timeout_ms=2000,
    ):
        device = find_device(
            device_name,
            duration_ms=scan_duration_ms,
            interval_us=scan_interval_us,
            window_us=scan_window_us,
        )
        return self.connect(
            device.addr_type,
            device.addr,
            timeout_ms=connect_timeout_ms
        )

    def _on_notify(self, conn_handle, value_handle, notify_data):
        try:
            services = self._services[conn_handle]
        except KeyError:
            pass
        else:
            for service in services:
                service._on_notify(value_handle, notify_data)


class Characteristic:
    def __init__(self, uuid):  # TODO flags
        self.uuid = uuid
        self._value_handles = {}
        self._on_notify_callback = lambda service, value: None

    def encode(self, decoded):
        return decoded

    def decode(self, encoded):
        return encoded

    def __get__(self, service, service_class):
        # for cpython compliance
        # in micropython cls.attribute doesn't invoke __get__
        if service is None:
            return self

        return ClientServiceCharacteristic(
            service.conn_handle,
            self._value_handles[service],
            self.encode,
            self.decode,
        )

    def register(self, uuid, service, value_handle):
        if uuid != self.uuid:
            raise ValueError
        self._value_handles[service] = value_handle

    def call_notify_callback(self, service, value):
        self._on_notify_callback(service, self.decode(value))

    # if notify flag
    def on_notify(self, callback):
        self._on_notify_callback = callback
        return callback


class ClientServiceCharacteristic:
    def __init__(self, conn_handle, value_handle, encode, decode):
        self._conn_handle = conn_handle
        self._value_handle = value_handle
        self._decode = encode
        self._encode = decode

    # if read flag
    def read(self):
        return self._decode(blesync.gattc_read(self._conn_handle, self._value_handle))

    # if write flag
    def write(self, data, ack=False):
        self._encode(data)
        blesync.gattc_write(self._conn_handle, self._value_handle, data, ack)


class Service:
    # https://www.bluetooth.com/specifications/gatt/services/
    uuid = NotImplemented

    @classmethod
    def _get_characteristics(cls):
        for name in dir(cls):
            attr = getattr(cls, name)
            if isinstance(attr, Characteristic):
                yield attr

    def __init__(self, uuid, conn_handle, start_handle, end_handle):
        if uuid != self.uuid:
            raise ValueError
        characteristics = list(self._get_characteristics())
        self._characteristics = {}
        self.conn_handle = conn_handle
        for def_handle, value_handle, properties, uuid in blesync.gattc_discover_characteristics(
            conn_handle, start_handle, end_handle
        ):
            for index, characteristic in enumerate(characteristics, start=1):
                try:
                    characteristic.register(uuid, self, value_handle)
                except ValueError:
                    continue
                else:
                    self._characteristics[value_handle] = characteristic
                    if index == len(self._characteristics):
                        return
                    break

    def _on_notify(self, value_handle, message):
        characteristic = self._characteristics[value_handle]
        characteristic.call_notify_callback(self, message)

        # if bluetooth.FLAG_WRITE & properties == 0:
        # on_(characteristic_name)%_write_received
        # self.handles[uuid] = value_handle
        # if len(self.handles) == len(characteristics):
        #     break

    # def disconnect(self, connection: BLEConnection, callback):
    #     self._assert_active()
    #     self._disconnect_callback[connection] = callback
    #     _ble.gap_disconnect(connection.conn_handle)


on_disconnect = blesync.on_peripherial_disconnect
