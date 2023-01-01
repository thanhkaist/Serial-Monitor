import binascii
import can
import canopen

if __name__ == '__main__':


    # Different representation of ascii string
    print("=====Different representation of byte array======")
    ascii_string = "send abc \x0a\x0b\x0c"
    print(f"STRING: {ascii_string}") # "send abc \x0a\x0b\x0c"
    mbytes = ascii_string.encode('utf-8') # b'send abc \x0a\x0b\x0c'
    for byte in mbytes:
        print(byte,end= ",") # 115,101,110,100,32,97,98,99,32,10,11,12,
    print()
    for byte in mbytes:
        print(hex(byte),end= ",") # 0x73,0x65,0x6e,0x64,0x20,0x61,0x62,0x63,0x20,0xa,0xb,0xc,
    print()
    print(f"THE STRING OF BYTES {mbytes.decode('utf-8')}") # send abc \x0a\x0b\x0c
    
    print("=====================================")
        
    print("=====Use string to inpux bytes array as hexes======")
    # Start with hex string: each two hex chars are one byte
    Hexstring = "73656e6420616263200a0b0c"
    print(f"HEX STRING: {Hexstring}") # 73656e6420616263200a0b0c
    # Convert it to bytes representation
    mbytes = binascii.unhexlify(Hexstring) # b'send abc \x0a\x0b\x0c'
    for byte in mbytes:
        print(byte,end= ",") # 115,101,110,100,32,97,98,99,32,10,11,12,
    print()
    for byte in mbytes:
        print(hex(byte),end= ",") # 0x73,0x65,0x6e,0x64,0x20,0x61,0x62,0x63,0x20,0xa,0xb,0xc,
    print()
    print(mbytes) # b'send abc \x0a\x0b\x0c'
    # print the bytes as string
    print(mbytes.decode('utf-8')) # send abc \x0a\x0b\x0c
    # print the bytes as hex string
    print(binascii.hexlify(mbytes)) # b'73656e6420616263200a0b0c'
    print(binascii.hexlify(mbytes).decode('utf-8')) # 73656e6420616263200a0b0c
    print("=====================================")


pdo = can.Message(arbitration_id=0x180, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
print(pdo.arbitration_id.to_bytes)
print(pdo.data)


# contruct can frame
func_code = 0x180
node_id = 0x01
# 11 bit communication object id
cob_id = (func_code+node_id) & 0x07FF
print(cob_id)
print(bin(cob_id<<5|0x0003))
is_RTR = 0 & 0x0001
data_len =3 & 0x000F
# (cob_id + node_id)[11] + RTR[1] + data_len[4]
can_header = (cob_id)<<5 | is_RTR<<4 | data_len
# can_header to 2 bytes
can_header_bytes = can_header.to_bytes(2, byteorder='big') 
# can_header_bytes =str(can_header).encode('utf-8')
print(can_header_bytes)
for byte in can_header_bytes:
    print(hex(byte),end= ",")
for byte in can_header_bytes:
    print(bin(byte),end= ",")
print()

data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
# sending bytes 

sending_bytes = can_header_bytes + bytes(data)
for byte in sending_bytes:
    print(hex(byte),end= ",") 

print()

def build_can_frame(func_code,node_id,data_len,data,RTR=0):
    # 11 bit communication object id
    cob_id = (func_code+node_id) & 0x07FF
    is_RTR = RTR & 0x0001
    data_len =data_len & 0x000F
    # (cob_id + node_id)[11] + RTR[1] + data_len[4]
    can_header = (cob_id)<<5 | is_RTR<<4 | data_len
    # can_header to 2 bytes
    can_header_bytes = can_header.to_bytes(2, byteorder='big') 
    # can_header_bytes =str(can_header).encode('utf-8')
    sending_bytes = can_header_bytes + bytes(data)
    return sending_bytes

import enum
# test build_can_frame

class CommunicationObject(enum):
    TPDO0 = 0x180
    RPDO0 = 0x200
    TPDO1 = 0x280
    RPDO1 = 0x300
    TPDO2 = 0x380
    RPDO2 = 0x400
    TPDO3 = 0x480
    RPDO3 = 0x500

class ControllerNodeID(enum):
    PTR = 0x01
    Track = 0x02
    FIZ_CONTROLLER = 0x03
    CAN_USB = 0x04
    FIZ_MOTOR = 0x05
    PAN_ELMO = 0x06
    TILT_ELMO = 0x07
    ROLL_ELMO = 0x08
    TRACK_ELMO = 17


sending_bytes = build_can_frame(0x180,0x01,3,[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])

for byte in sending_bytes:
    print(hex(byte),end= ",")

