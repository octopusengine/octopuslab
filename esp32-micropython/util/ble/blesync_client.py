from collections import namedtuple

from micropython import const

import util.ble.blesync

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)


# 0x00 - ADV_IND - connectable and scannable
# undirected
# advertising
# 0x01 - ADV_DIRECT_IND - connectable
# directed
# advertising
# 0x02 - ADV_SCAN_IND - scannable
# undirected
# advertising
# 0x03 - ADV_NONCONN_IND - non - connectable
# undirected
# advertising
# 0x04 - SCAN_RSP - scan
# response

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
    return {
        d[0]: d[1:]
        for d in _split_data(payload)
    }


def decode_adv_name(data):
    try:
        encoded_name = data[_ADV_TYPE_NAME]
    except KeyError:
        return ''
    else:
        return str(encoded_name, "utf-8")


def decode_adv_type(data):
    try:
        return data[_ADV_TYPE_FLAGS][0]
    except KeyError:
        return None


# TODO
# def decode_services(payload):
#     services = []
#     for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
#         services.append(bluetooth.UUID(struct.unpack("<h", u)[0]))
#     for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
#         services.append(bluetooth.UUID(struct.unpack("<d", u)[0]))
#     for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
#         services.append(bluetooth.UUID(u))
#     return services


BLEDevice = namedtuple(
    'BLEDevice',
    ('addr_type', 'addr', 'adv_name', 'adv_type_flags', 'rssi',)
)

BLEService = namedtuple(
    'BLEService',
    ('start_handle', 'end_handle', 'uuid')
)

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


def scan():
    blesync.active(True)
    for addr_type, addr, adv_type, rssi, adv_data in blesync.gap_scan(
        2000,
        30000,
        30000
    ):
        parsed_data = parse_adv_data(adv_data)
        adv_name = decode_adv_name(parsed_data)
        adv_type_flags = decode_adv_type(parsed_data)

        # addr buffer is owned by caller so need to copy it.
        addr_copy = bytes(addr)
        yield BLEDevice(
            addr_type=addr_type,
            addr=addr_copy,
            adv_name=adv_name,
            adv_type_flags=adv_type_flags,
            rssi=rssi,
        )


class BLEClient:
    def __init__(self, *service_classes):
        self._service_classes = service_classes
        self._services = {}
        blesync.on_gattc_notify(self._on_gattc_message)
        blesync.on_gattc_indicate(self._on_gattc_message)

    def connect(self, addr_type, addr):
        # TODO separate connect and service creation
        blesync.active(True)
        conn_handle = blesync.gap_connect(addr_type, addr)

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

    def _on_gattc_message(self, conn_handle, value_handle, notify_data):
        try:
            services = self._services[conn_handle]
        except KeyError:
            pass
        else:
            for service in services:
                service._on_gattc_message(value_handle, notify_data)


class Characteristic:
    def __init__(self, uuid):  # TODO flags
        self.uuid = uuid
        self._value_handles = {}
        self.connected_characteristic = None
        self._on_message_callback = lambda *_: None

    def __get__(self, service, owner=None):
        return ConnectedCharacteristic(
            service.conn_handle,
            self._value_handles[service]
        )

    def register(self, uuid, service, value_handle):
        if uuid != self.uuid:
            raise ValueError
        self._value_handles[service] = value_handle

    def __delete__(self, service):
        del self._value_handles[service]

    def on_message(self, callback):
        self._on_message_callback = callback
        return callback


class ConnectedCharacteristic:
    def __init__(self, conn_handle, value_handle):
        self._conn_handle = conn_handle
        self._value_handle = value_handle

    def read(self, timeout_ms=None):
        return blesync.gattc_read(
            self._conn_handle,
            self._value_handle,
            timeout_ms
        )

    def write(self, data, ack=False, timeout_ms=None):
        blesync.gattc_write(
            self._conn_handle, self._value_handle, data, ack, timeout_ms
        )


class Service:
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
            for characteristic in characteristics:  # TODO enumerate
                try:
                    characteristic.register(uuid, self, value_handle)
                except ValueError:
                    continue
                else:
                    self._characteristics[value_handle] = characteristic
                    if len(self._characteristics) == len(characteristics):
                        return
                    break

    def _on_gattc_message(self, value_handle, message):
        characteristic = self._characteristics[value_handle]
        characteristic._on_message_callback(self, message)

        # if bluetooth.FLAG_WRITE & properties == 0:
        # on_(characteristic_name)%_write_received
        # self.handles[uuid] = value_handle
        # if len(self.handles) == len(characteristics):
        #     break

    # def disconnect(self, connection: BLEConnection, callback):
    #     self._assert_active()
    #     self._disconnect_callback[connection] = callback
    #     _ble.gap_disconnect(connection.conn_handle)
