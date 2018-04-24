import math
import numpy as np

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

b = Buffer()
b.writeInt40(1)