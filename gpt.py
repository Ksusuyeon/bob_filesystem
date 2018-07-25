import sys
import struct

def read_sector(f, sector, count=1):
    f.seek(sector *512)
    return f.read(count * 512)

def parser(data):
    for i in range(4):
        partition = data[i*128:(i+1)*128]
        print("=======================================")
        print("Starting LBA : ", struct.unpack_from("<I",partition,32)[0])
        print("size : ", struct.unpack_from("<I",partition,40)[0]-struct.unpack_from("<I",partition,32)[0]+1)
        print("")

def extend_partition(f):
    sector = 3
    data = read_sector(f,sector)
    for i in range(4):
        partition = data[i*128:(i+1)*128]
        if partition[0] == 0:
            break
        print("=======================================")        
        print("Starting LBA : ", struct.unpack_from("<I",partition,32)[0])
        print("size : ", struct.unpack_from("<I",partition,40)[0] - struct.unpack_from("<I",partition,32)[0] +1)
        print("")
        
    
filename = sys.argv[1]
f = open(filename, "rb")
data = read_sector(f,2)
parser(data)
extend_partition(f)


