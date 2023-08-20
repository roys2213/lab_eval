from construct.core import *
from construct.lib import *

def pad( data_len):
    Pad = GreedyRange(Byte)
    pad_len = ( 2 - data_len)%4
    if (data_len + pad_len + 2) %4 != 0:
        raise PadLenError({'data_len': data_len, 'pad_len':pad_len}, \
                          "32 bits alignment is not respected")
    return Pad.build(range(pad_len + 1)[1:])
