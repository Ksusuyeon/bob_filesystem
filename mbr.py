import sys
import struct

def read_sectors(fd, sector, count = 1):
    fd.seek(sector * 512)
    return fd.read(count * 512)
def check(data):
    if data[-2] != 0x55 and data[-1] != 0xAA:
        print("이 파티션은 Boor Record가 아닙니다.")

def print_table_entry(table):
    print("=======================================")
    print("Starting LBA : ", struct.unpack_from("<I", table, 8)[0])
    print("size : ", struct.unpack_from("<I", table, 12)[0])
    print("")

def ebr_parser(f,base,sector = 0):
    f.seek((base+sector)*512)
    data = f.read(512)
    check(data)

    partition_data = data[446:446+64]
    
    for i in range(4):
        temp = partition_data[i*16:(i+1)*16]

        if temp[4] == 7:
            print("=======================================")
            print("Starting LBA : ", struct.unpack_from("<I", temp, 8)[0]+base+sector)
            print("size : ", struct.unpack_from("<I", temp, 12)[0])
            print("")

        elif temp[4] == 5:
            sector = struct.unpack_from("<I",temp,8)[0]
            #print("sector:",sector)
            ebr_parser(f,base,sector)

        elif temp[4] == 0:
            continue
             
filename = sys.argv[1]
f = open(filename, "rb")
data = read_sectors(f, 0)

check(data)
partition_data = data[446:446+64]

table1 = partition_data[0:16]
table2 = partition_data[16:32]
table3 = partition_data[32:48]
table4 = partition_data[48:64]

base = struct.unpack_from("<I",table4, 8)[0]

print_table_entry(table1)
print_table_entry(table2)
print_table_entry(table3)

ebr_parser(f,base)
