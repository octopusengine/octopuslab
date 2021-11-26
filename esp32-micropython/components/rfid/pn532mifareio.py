# Copyright (c) 2021 Petr Kracik
# Provides stream IO for PN532 RFID rader
# Support 1k Mifare Classic card

from io import IOBase

__version__ = "0.1"


class PN532MifareIO(IOBase):
    def __init__(self, mifare, id, key = b'\xff\xff\xff\xff\xff\xff', size = 1024, debug = False):
        self._mf = mifare
        self._key = key
        self._mfid = id
        # 0x60 KEY_A
        # 0x61 KEY_B
        self._keyid = 0x61
        self._buffer = bytes()
        self._bufpos = 0
        self._blockpos = 0
        self._debug = debug

        # Effective max buffer size
        if size == 1024:
            self._size = 736
            self._blocksize = 16
            self._sector0 = self.read(self._blocksize * 3)
        else:
            raise Exception("Unsupported Mifare classic size: {}".format(size))

        if self._sector0[0:4] != self._mfid:
            raise Exception("Provided ID does not match Sector 0 ID!")


    def read(self, count):
        if count < 0:
            raise ValueError("Can not read negative number of bytes")

        if self._bufpos + count > self._size:
            raise ValueError("Can not read more data")

        if self._bufpos + count > len(self._buffer):
            self._debuglog("read: Need more {} bytes! Buffer size: {}".format(self._bufpos + count - len(self._buffer), len(self._buffer)))
            self._read_mifare_block(self._bufpos + count - len(self._buffer))

        pos = self._bufpos
        self._bufpos += count
        return self._buffer[pos:self._bufpos]


    def seek(self, position):
        if position < 0:
            raise ValueError("Can not seek negative number")

        if position > len(self._buffer):
            raise ValueError("Can not seek beyond buffer")

        self._bufpos = position


    def seekable(self):
        return True


    def tell(self):
        return self._bufpos


    def write(self):
        raise NotImplementedError()

    def close(self):
        pass

    def _debuglog(self, val, *args, **kargs):
        if not self._debug:
            return
        
        print(val, *args, **kargs)


    def _read_mifare_block(self, count):
        self._debuglog("_read_mifare_block: Entry function mifare block: {}".format(self._blockpos))
        ndatablocksread = 0
        ndatablocks = count // self._blocksize

        if count % self._blocksize != 0:
            ndatablocks += 1

        self._debuglog("_read_mifare_block: Data blocks {}".format(ndatablocks))
        self._debuglog("_read_mifare_block: Read more {} bytes that is {} MiFare blocks From {} to {}".format(count, ndatablocks, self._blockpos, self._blockpos + ndatablocks))

        while ndatablocksread < ndatablocks:
            if self._blockpos % 4 == 0:
                self._debuglog("_read_mifare_block: Auth sector {}".format(self._blockpos//4))

                if not self._mf.mifare_classic_authenticate_block(self._mfid, self._blockpos, self._keyid, self._key):
                    raise ValueError("Failed to authenticate block {} of sector {}. Is provided key correct?".format(self._blockpos, self._blockpos//4))

            if self._blockpos % 4 != 3:
                self._debuglog("  \ Reading block {}".format(self._blockpos))
                data = self._mf.mifare_classic_read_block(self._blockpos)
                self._buffer += data
                ndatablocksread += 1
            else:
                self._debuglog("  \ Skipping AUTH block {}". format(self._blockpos))

            self._blockpos +=1
