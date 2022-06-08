# OctopusLab based on carlosgilgonzalez
# 2022 Petr Kracik

# License: MIT

import utime as time
from .octopus_pn532 import PN532, BusyError

_SPI_STATREAD = const(0x02)
_SPI_DATAWRITE = const(0x01)
_SPI_DATAREAD = const(0x03)
_SPI_READY = const(0x01)

def reverse_bit(num):
    """Turn an LSB byte to an MSB byte, and vice versa. Used for SPI as
    it is LSB for the PN532, but 99% of SPI implementations are MSB only!"""
    result = 0
    for _ in range(8):
        result <<= 1
        result += (num & 1)
        num >>= 1
    return result


class PN532_SPI(PN532):
    """Driver for the PN532 connected over SPI"""

    def __init__(self, spi, ss, *, reset=None, debug=False):
        """Create an instance of the PN532 class using Serial connection.
        Optional reset pin and debugging output.
        """
        self.debug = debug
        self._spi = spi
        self._ss = ss
        super().__init__(debug=debug, reset=reset)

    def _wakeup(self):
        """Send any special commands/data to wake up PN532"""
        if self._reset_pin:
            # self._reset_pin.value = True
            self._reset_pin.value(1)
            time.sleep(0.01)
        self.low_power = False
        self._ss(0)
        self._spi.write(
            b"\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )  # wake up!
        self._ss(1)
        if self.debug:
            print("PN532 wake up")
        self.SAM_configuration()


    def _wait_ready(self, timeout=1):
        """Wait `timeout` seconds"""
        status_query = bytearray([reverse_bit(_SPI_STATREAD), 0])
        status = bytearray([0, 0])
        timestamp = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), timestamp) < timeout * 1000:
            time.sleep(0.02)   # required
            self._ss(0)
            time.sleep_ms(2)
            self._spi.write_readinto(status_query, status)
            time.sleep_ms(2)
            self._ss(1)

            if reverse_bit(status[1]) == 0x01:
                return True
            else:
                time.sleep(0.01)

        # Timed out!
        return False

    def _read_data(self, count):
        """Read a specified count of bytes from the PN532."""
        # Build a read request frame.
        frame = bytearray(count+1)
        # Add the SPI data read signal byte, but LSB'ify it
        frame[0] = reverse_bit(_SPI_DATAREAD)
        time.sleep(0.02)   # required
        self._ss(0)
        time.sleep_ms(2)
        self._spi.write_readinto(frame, frame)
        time.sleep_ms(2)
        self._ss(1)
        for i, val in enumerate(frame):
            frame[i] = reverse_bit(val)  # turn LSB data to MSB
        if self.debug:
            print("DEBUG: _read_data: ", [hex(i) for i in frame[1:]])
        return frame[1:]   # don't return the status byte


    def _write_data(self, framebytes):
        """Write a specified count of bytes to the PN532"""
        # start by making a frame with data write in front,
        # then rest of bytes, and LSBify it
        rev_frame = [reverse_bit(x)
                     for x in bytes([_SPI_DATAWRITE]) + framebytes]
        if self.debug:
            print("DEBUG: _write_data: ", [hex(i) for i in rev_frame])
        time.sleep(0.02)
        self._ss(0)
        time.sleep_ms(2)
        self._spi.write(bytes(rev_frame))
        time.sleep_ms(2)
        self._ss(1)
