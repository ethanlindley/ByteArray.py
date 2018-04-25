# PyBuffer
A very simple script for writing and reading bytes.

This is my first project using Python.

Example of writing 40-byte integers:

```
def writeInt40(self, value):
    array = self.array
    offset = self.position
    
    array.insert(offset, value >> 32)
    array.insert(offset + 1, value >> 24)
    array.insert(offset + 2, value >> 16)
    array.insert(offset + 3, value >> 8)
    array.insert(offset + 4, value & 0xff)
    
    self.setPosition(5)
    return array
