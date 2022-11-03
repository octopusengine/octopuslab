# The MIT License (MIT)
# Copyright (c) 2019-2022 Jan Cespivo

__version__ = "1.0.3"

from collections import deque

from bluetooth import BLE, UUID
import machine
from micropython import const, schedule
import time

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_L2CAP_CONNECT = const(23)

curr_conn_handle = None


def _register_callback(irq, callback):
    _callbacks[irq].append(callback)


def _event(irq, data, key):
    _events[irq][key].append(data)


def _call_callbacks(irq_data):
    irq, data = irq_data

    for callback in _callbacks[irq]:
        callback(*data)


def _callback(irq, data):
    schedule(_call_callbacks, (irq, data))


def _register_event(irq, key, bufferlen=1):
    _events[irq][key] = deque(tuple(), bufferlen)


# TODO
# def _irq_gatts_read_request(data):
#     # A central has issued a read. Note: this is a hard IRQ.
#     # Return None to deny the read.
#     # Note: This event is not supported on ESP32.
#     conn_handle, attr_handle = data
#     _event(_IRQ_GATTS_READ_REQUEST, data, conn_handle)


_events = {
    _IRQ_SCAN_RESULT: {},
    _IRQ_SCAN_DONE: {},
    _IRQ_PERIPHERAL_CONNECT: {},
    _IRQ_PERIPHERAL_DISCONNECT: {},
    _IRQ_GATTC_SERVICE_RESULT: {},
    _IRQ_GATTC_SERVICE_DONE: {},
    _IRQ_GATTC_CHARACTERISTIC_RESULT: {},
    _IRQ_GATTC_CHARACTERISTIC_DONE: {},
    _IRQ_GATTC_DESCRIPTOR_RESULT: {},
    _IRQ_GATTC_DESCRIPTOR_DONE: {},
    _IRQ_GATTC_READ_RESULT: {},
    _IRQ_GATTC_WRITE_DONE: {},
}

_callbacks = {
    _IRQ_CENTRAL_CONNECT: [],
    _IRQ_CENTRAL_DISCONNECT: [],
    _IRQ_PERIPHERAL_DISCONNECT: [],
    _IRQ_GATTS_WRITE: [],
    _IRQ_GATTC_NOTIFY: [],
    _IRQ_GATTC_INDICATE: [],
    # _IRQ_GATTS_READ_REQUEST: _irq_gatts_read_request,
}


def _irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        print("dis------"*10)
        conn_handle, addr_type, addr = data
        curr_conn_handle = conn_handle
        print(conn_handle,type(conn_handle),curr_conn_handle)
        time.sleep(2)
        print("dis------"*10)
        disconnect_client()
        print(">>>>>>>>>>>>>>>"*5)
    
    if event in (
        _IRQ_CENTRAL_CONNECT,
        _IRQ_CENTRAL_DISCONNECT
    ):
        # A central has connected to this peripheral.
        # A central has disconnected from this peripheral.
        conn_handle, addr_type, addr = data
        data = conn_handle, addr_type, bytes(addr)
        _callback(event, data)
    elif event == _IRQ_PERIPHERAL_DISCONNECT:
        # A central has disconnected from this peripheral or connect timeout
        if data == (65535, 255, b'\x00\x00\x00\x00\x00\x00'):
            # connect timeout
            _event(event, None, None)
        else:
            conn_handle, addr_type, addr = data
            data = conn_handle, addr_type, bytes(addr)
            _callback(event, data)
    elif event == _IRQ_GATTS_WRITE:
        # A central has written to this characteristic or descriptor.
        # conn_handle, attr_handle = data
        _callback(event, data)
    elif event in (_IRQ_GATTC_NOTIFY, _IRQ_GATTC_INDICATE):
        # A peripheral has sent a notify request.
        # A peripheral has sent an indicate request.
        conn_handle, value_handle, notify_data = data
        data = conn_handle, value_handle, bytes(notify_data)
        _callback(event, data)
    elif event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        data = addr_type, bytes(addr), adv_type, rssi, bytes(adv_data)
        _event(event, data, None)
    elif event == _IRQ_SCAN_DONE:
        # A single scan result.
        _event(event, None, None)
    elif event == _IRQ_PERIPHERAL_CONNECT:
        # A successful gap_connect().
        conn_handle, addr_type, addr = data
        key = addr_type, bytes(addr)
        _event(event, conn_handle, key)
    elif event == _IRQ_GATTC_SERVICE_RESULT:
        # Called for each service found by gattc_discover_services().
        conn_handle, start_handle, end_handle, uuid = data
        data = start_handle, end_handle, UUID(uuid)
        _event(event, data, conn_handle)
    elif event == _IRQ_GATTC_SERVICE_DONE:
        # Called once service discovery is complete.
        # Note: Status will be zero on success, implementation-specific value otherwise.
        conn_handle, status = data
        _event(event, status, conn_handle)
    elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
        # Called for each characteristic found by gattc_discover_services().
        conn_handle, def_handle, value_handle, properties, uuid = data
        data = def_handle, value_handle, properties, UUID(uuid)
        _event(event, data, conn_handle)
    elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
        # Called once service discovery is complete.
        # Note: Status will be zero on success, implementation-specific value otherwise.
        conn_handle, status = data
        _event(event, status, conn_handle)
    elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
        # Called for each descriptor found by gattc_discover_descriptors().
        conn_handle, dsc_handle, uuid = data
        data = dsc_handle, UUID(uuid)
        _event(event, data, conn_handle)
    elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
        # Called once service discovery is complete.
        # Note: Status will be zero on success, implementation-specific value otherwise.
        conn_handle, status = data
        _event(event, status, conn_handle)
    elif event == _IRQ_GATTC_READ_RESULT:
        # A gattc_read() has completed.
        conn_handle, value_handle, char_data = data
        key = conn_handle, value_handle
        _event(event, bytes(char_data), key)
    elif event == _IRQ_GATTC_READ_DONE:
        # A gattc_read() has completed.
        # Note: The value_handle will be zero on btstack (but present on NimBLE).
        # Note: Status will be zero on success, implementation-specific value otherwise.
        # conn_handle, value_handle, status = data
        # key = conn_handle, value_handle
        # data = status
        return  # TODO
    elif event == _IRQ_GATTC_WRITE_DONE:
        # A gattc_write() has completed.
        # Note: The value_handle will be zero on btstack (but present on NimBLE).
        # Note: Status will be zero on success, implementation-specific value otherwise.
        conn_handle, value_handle, status = data
        key = conn_handle, value_handle
        _event(event, status, key)
    elif event == _IRQ_L2CAP_CONNECT:
        conn_handle, cid, psm, our_mtu, peer_mtu = data
        print("BLE_DIS_"*12)
        print("_IRQ_L2CAP_CONNECT",conn_handle, cid)
        curr_conn_handle = conn_handle
        curr_conn_cid = cid
        time.sleep(1)
        print("-disconnect_client")
        disconnect_client()

    else:
        return

#from machine import Timer

#tim2.init(period=per, mode=Timer.PERIODIC, callback=lambda t:timerAction())


def disconnect_client():
    #if curr_conn_handle:
    BLE.gap_disconnect(0)
    #curr_conn_handle = None

def _wait_for_event(irq, key, event_exception_class=None):
    event_queue = _events[irq][key]

    while not event_queue:
        machine.idle()

    event_result = event_queue.popleft()
    if event_exception_class and event_result:
        raise event_exception_class(event_result)
    return event_result


def _wait_for_disjunct_events(irq_1, key_1, irq_2, key_2):
    event_queue_1 = _events[irq_1][key_1]
    event_queue_2 = _events[irq_2][key_2]

    while True:
        if event_queue_1:
            return event_queue_1.popleft(), None
        elif event_queue_2:
            return None, event_queue_2.popleft()

        machine.idle()


_ble = BLE()

config = _ble.config
gap_advertise = _ble.gap_advertise
gatts_register_services = _ble.gatts_register_services
gatts_read = _ble.gatts_read
gatts_write = _ble.gatts_write
gatts_set_buffer = _ble.gatts_set_buffer
gap_disconnect = _ble.gap_disconnect


def _results_until_done(
    event_result, event_done, event_done_exception_class, event_key, func, args
):
    _register_event(event_result, event_key, bufferlen=100)
    _register_event(event_done, event_key)

    func(*args)

    results_queue = _events[event_result][event_key]
    done_queue = _events[event_done][event_key]
    while True:
        while results_queue:
            yield results_queue.popleft()

        if done_queue:
            done_status = done_queue.popleft()
            if done_status:
                raise event_done_exception_class(done_status)
            return

        machine.idle()


def gap_scan(duration_ms, interval_us=None, window_us=None):
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

    assert not (interval_us is None and window_us is not None), \
        "Argument window_us has to be specified if interval_us is specified"

    args = [duration_ms]
    if interval_us is not None:
        args.append(interval_us)
        if window_us is not None:
            args.append(window_us)
    try:
        yield from _results_until_done(
            _IRQ_SCAN_RESULT,
            _IRQ_SCAN_DONE,
            None,
            None,
            func=_ble.gap_scan,
            args=args
        )
    except GeneratorExit:
        _ble.gap_scan(None)
        _wait_for_event(_IRQ_SCAN_DONE, None)


def gatts_notify(conn_handle, handle, data=None):
    if data is None:
        return _ble.gatts_notify(conn_handle, handle)
    return _ble.gatts_notify(conn_handle, handle, data)


def activate():
    if not _ble.active():
        _ble.active(True)
        _ble.irq(_irq)


def deactivate():
    if _ble.active():
        _ble.active(False)


def is_active():
    return _ble.active()


class GapConnectTimeoutError(Exception):
    pass


def gap_connect(addr_type, addr, timeout_ms=2000):
    _register_event(_IRQ_PERIPHERAL_CONNECT, (addr_type, addr))
    _register_event(_IRQ_PERIPHERAL_DISCONNECT, None)
    _register_event(_IRQ_L2CAP_CONNECT, (conn_handle, cid, psm, our_mtu, peer_mtu))
    _ble.gap_connect(addr_type, addr, timeout_ms)
    conn_handle, _ = _wait_for_disjunct_events(
        _IRQ_PERIPHERAL_CONNECT, (addr_type, addr),
        _IRQ_PERIPHERAL_DISCONNECT, None
    )
    if conn_handle is None:
        raise GapConnectTimeoutError
    return conn_handle


class GattcDiscoverServicesError(Exception):
    pass


def gattc_discover_services(conn_handle, uuid=None):
    args = [conn_handle]
    if uuid is not None:
        args.append(uuid)

    return list(_results_until_done(
        event_result=_IRQ_GATTC_SERVICE_RESULT,
        event_done=_IRQ_GATTC_SERVICE_DONE,
        event_done_exception_class=GattcDiscoverServicesError,
        event_key=conn_handle,
        func=_ble.gattc_discover_services,
        args=args
    ))


class GattcDiscoverCharacteristicsError(Exception):
    pass


def gattc_discover_characteristics(
    conn_handle,
    start_handle,
    end_handle,
):
    # TODO uuid argument
    return list(_results_until_done(
        event_result=_IRQ_GATTC_CHARACTERISTIC_RESULT,
        event_done=_IRQ_GATTC_CHARACTERISTIC_DONE,
        event_done_exception_class=GattcDiscoverCharacteristicsError,
        event_key=conn_handle,
        func=_ble.gattc_discover_characteristics,
        args=(conn_handle, start_handle, end_handle)
    ))


class GattcDiscoverDescriptorError(Exception):
    pass


def gattc_discover_descriptors(conn_handle, start_handle, end_handle):
    return list(_results_until_done(
        event_result=_IRQ_GATTC_DESCRIPTOR_RESULT,
        event_done=_IRQ_GATTC_DESCRIPTOR_DONE,
        event_done_exception_class=GattcDiscoverDescriptorError,
        event_key=conn_handle,
        func=_ble.gattc_discover_descriptors,
        args=(conn_handle, start_handle, end_handle)
    ))


class GattcReadError(Exception):
    pass


def gattc_read(conn_handle, value_handle):
    # conn_handle, value_handle, char_data
    _register_event(_IRQ_GATTC_READ_RESULT, (conn_handle, value_handle))
    _ble.gattc_read(conn_handle, value_handle)
    return _wait_for_event(
        _IRQ_GATTC_READ_RESULT,
        (conn_handle, value_handle),
        GattcReadError
    )


class GattcWriteError(Exception):
    pass


def gattc_write(conn_handle, value_handle, data, ack=False):
    # wait for return status of write if ack is True
    # otherwise return None immediately
    _register_event(_IRQ_GATTC_WRITE_DONE, (conn_handle, value_handle))
    _ble.gattc_write(conn_handle, value_handle, data, ack)
    if ack:
        return _wait_for_event(
            _IRQ_GATTC_WRITE_DONE,
            (conn_handle, value_handle),
            GattcWriteError
        )


def on_central_connect(callback):
    # A central has connected to this peripheral.
    # conn_handle, addr_type, addr
    return _register_callback(_IRQ_CENTRAL_CONNECT, callback)


def on_central_disconnect(callback):
    # A central has disconnected from this peripheral.
    # conn_handle, addr_type, addr
    _register_callback(_IRQ_CENTRAL_DISCONNECT, callback)
    return callback


def on_peripherial_disconnect(callback):
    # Connected peripheral has disconnected.
    # conn_handle, addr_type, addr
    _register_callback(_IRQ_PERIPHERAL_DISCONNECT, callback)
    return callback


def on_gatts_write(callback):
    # A central has written to this characteristic or descriptor.
    # conn_handle, value_handle
    _register_callback(_IRQ_GATTS_WRITE, callback)
    return callback


def on_gattc_notify(callback):
    # A peripheral has sent a notify request.
    # conn_handle, value_handle, notify_data
    _register_callback(_IRQ_GATTC_NOTIFY, callback)
    return callback


def on_gattc_indicate(callback):
    # A peripheral has sent an indicate request.
    # conn_handle, value_handle, notify_data
    _register_callback(_IRQ_GATTC_INDICATE, callback)
    return callback

# TODO
# def on_gatts_read_request(conn_handle):
#     _add_callback(_callback_gatts_read_request, conn_handle,
#         gatts_read_request_callback)
