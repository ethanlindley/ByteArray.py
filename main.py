import math  # Used for writeInt64
import struct  # Used for ByteArray
import numpy as np  # Used for util functions

class Buffer:
    def __init__(self, array=[0] * 1024, offset=0, endian=0, debug=0):
        self.array = array  # Defaults to 1024, when debug is false (0), self.array is printed with a length of 256
        self.offset = offset  # Defaults to [0]
        self.endian = endian  # Defaults to BigEndian (0)
        self.debug = debug  # Defaults to false (0)

    def getStream(self):
        return self.array

    def getOffset(self):
        return self.offset

    def getEndian(self):
        return self.endian

    def getDebug(self):
        return self.debug

    def bytesAvailable(self):
        length = 1024 - self.offset
        if length == 0:
            print "Byte stream is full"  # The offset is 1024, but there's a chance the byte stream is NOT full, just nothing to write to
        return length

    def getWrittenBytes(self):
        return np.array(self.array)[np.array(self.array) > 0]  # Values higher than 0

    def getLengthBeforeByte(self, byte):
        return self.array[:self.array.index(byte)]

    def accurateBytesAvailable(self, byte):
        totalLength = len(self.getLengthBeforeByte(byte))
        return self.bytesAvailable() + totalLength

    def skipByte(self, amountToSkip):
        self.offset += amountToSkip

    def fillStream(self, numberToFill):
        self.array = self.array[numberToFill] * 1024  # Fills the byte stream with 1024 "numberToFill"

    def fixStream(self):  # This was a temporary fix that is not being used
        if self.offset > len(self.array):
            self.array += [0] * int(self.offset - len(self.array))
        else:
            return self.array

    def toString(self):
        print "Current offset: " + str(self.offset)  # Prints offset
        if self.debug == 0:
            print "256 length byte stream: " + str(self.array[0:len(self.array) / 4])  # Length of 256
        else:
            print "Byte stream: " + str(self.array)  # Full byte stream, 1024 length
        print "Written bytes: " + str(self.getWrittenBytes())  # Prints values in the byte stream that are higher than 0
        if self.endian == 0:
            print "Endian: Big endian (0)"
        else:
            print "Endian: Little endian (1)"
        print "Bytes available: " + str(self.bytesAvailable())  # 1024 - self.offset

    def writeInt8(self, value):
        self.array.insert(self.offset, value & 0xff)
        self.offset += 1
        return self.toString()

    def writeInt16(self, value):
        value = +value
        self.offset = self.offset >> 0
        if self.endian == 0:
            self.array.insert(self.offset, value >> 8)
            self.array.insert(self.offset + 1, value & 0xff)
        else:
            self.array.insert(self.offset, value & 0xff)
            self.array.insert(self.offset + 1, value >> 8)
        self.offset += 2
        return self.toString()

    def writeInt24(self, value):
        value = +value
        self.offset = self.offset >> 0
        if self.endian == 0:
            self.array.insert(self.offset, value >> 16)
            self.array.insert(self.offset + 1, value >> 8)
            self.array.insert(self.offset + 2, value & 0xff)
        else:
            self.array.insert(self.offset, value & 0xff)
            self.array.insert(self.offset + 1, value >> 8)
            self.array.insert(self.offset + 2, value >> 16)
        self.offset += 3
        return self.toString()

    def writeInt32(self, value):  # I don't know why but Little endian bytes go to the fifth offset in the byte stream? This also seems to be the same in Node.js
        value = +value
        self.offset = self.offset >> 0
        if self.endian == 0:
            self.array.insert(self.offset, value >> 24)
            self.array.insert(self.offset + 1, value >> 16)
            self.array.insert(self.offset + 2, value >> 8)
            self.array.insert(self.offset + 3, value & 0xff)
            self.offset += 4
        else:
            self.offset += 4
            self.array.insert(self.offset, value & 0xFF)
            self.array.insert(self.offset + 1, value >> 8)
            self.array.insert(self.offset + 2, value >> 16)
            self.array.insert(self.offset + 3, value >> 24)
        return self.toString()

    def writeInt40(self, value):
        value = +value
        self.offset = self.offset >> 0
        self.offset += 1  # writeInt8
        self.writeInt32(int(value))
        return self.toString()

    def writeInt48(self, value):
        value = +value
        self.offset = self.offset >> 0
        self.offset += 2  # writeInt16
        self.writeInt32(int(value))
        return self.toString()

    def writeInt56(self, value):
        value = +value
        self.offset = self.offset >> 0
        self.offset += 3  # writeInt24
        self.writeInt32(int(value))
        return self.toString()

    def writeInt64(self, value):  # The byte does not get overwritten in the byte stream, because we use Int32 twice with the same offset (4+4=8)
        value = +value
        self.offset = self.offset >> 0
        if self.endian == 0:
            high = math.floor(int(value / 0x100000000))
            low = value - high * 0x100000000
            self.writeInt32(int(high))
            self.writeInt32(int(low))
        else:
            SHIFT_RIGHT_32 = 1 / (1 << 16) * (1 << 16)
            if value < 0x8000000000000000:
                self.writeInt32(int(value & -1))
                self.writeInt32(int(math.floor(value * SHIFT_RIGHT_32)))  # Kills any float values
        return self.toString()

    def readInt8(self):
        self.offset = self.offset >> 0
        return self.array[self.offset-1]

class ByteArray:
    def __init__(this, bytes=""):
        this.bytes = bytes

    def isUnicode(this, value):
        if type(value) == unicode:
            value = value.encode("utf-8")
            return value
        pass

    def writeByte(this, value):
        this.isUnicode(value)
        this.bytes += pack("!b", int(value)) # Offset: 1
        return this.bytes

    def writeUnsignedByte(this, value):
        this.isUnicode(value)
        this.bytes += pack("!B", int(value)) # Offset: 1
        return this.bytes

    def writeShort(this, value):
        this.isUnicode(value)
        this.bytes += pack("!h", int(value)) # Offset: 2
        return this.bytes

    def writeUnsignedShort(this, value):
        this.isUnicode(value)
        this.bytes += pack("!H", int(value)) # Offset: 2
        return this.bytes

    def writeInt(this, value):
        this.isUnicode(value)
        this.bytes += pack("!i", int(value)) # Offset: 4
        return this.bytes

    def writeUnsignedInt(this, value):
        this.isUnicode(value)
        this.bytes += pack("!I", int(value)) # Offset: 4
        return this.bytes

    def writeBoolean(this, value):
        this.isUnicode(value)
        this.bytes += pack("!?", int(value)) # Offset: 1
        return this.bytes

    def writeUTF(this, value):
        this.isUnicode(value)
        value = str(value)
        size = len(value)
        this.writeShort(size) # Offset: 2
        this.write(value) # Offset: 2 + 1 = 3
        return this.bytes

    def writeUTFBytes(this, value, size):
        this.isUnicode(value)
        for data in str(pack("!b", 0)) * int(size):
            if len(value) < int(size):
                value = value + pack("!b", 0)
        this.write(value)
        return this.bytes

    def writeBytes(this, value):
        this.bytes += value
        return this.bytes

    def write(this, value):
        this.bytes += value

    def readByte(this):
        value = unpack('!b', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return value

    def readUnsignedByte(this):
        value = unpack('!B', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return value

    def readShort(this):
        value = unpack('!h', this.bytes[:2])[0]
        this.bytes = this.bytes[2:]
        return value

    def readUnsignedShort(this):
        value = unpack('!H', this.bytes[:2])[0]
        this.bytes = this.bytes[2:]
        return value

    def readInt(this):
        value = unpack('!i', this.bytes[:4])[0]
        this.bytes = this.bytes[4:]
        return value

    def readUnsignedInt(this):
        value = unpack('!I', this.bytes[:4])[0]
        this.bytes = this.bytes[4:]
        return value

    def readUTF(this):
        size = unpack('!h', this.bytes[:2])[0]
        value = this.bytes[2:2 + size]
        this.bytes = this.bytes[size + 2:]
        return value

    def readBoolean(this):
        value = unpack('!?', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return (True if value == 1 else False)

    def readUTFBytes(this, size):
        value = this.bytes[:int(size)]
        this.bytes = this.bytes[int(size):]
        return value

    def getLength(this):
        return len(this.bytes)

    def bytesAvailable(this):
        return len(this.bytes) > 0

    def toByteArray(this):
        return this.bytes

b = Buffer()
b.writeInt40(1)