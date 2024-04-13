import time
import math

def read_dictionary(file_path) -> list:
    """Reads dictionary from file, returns tuple: (dicitonary, bits_to_store_each_element)"""
    d_len = -1
    iter = 0
    dictio = {}
    with open(file_path, 'rb') as file:
        while(element := file.read(1)):
            #read dictionary
            if d_len > 0:
                dictio[iter] = (int(element.hex(), 16)).to_bytes(1, 'big')
                iter += 1
                d_len -= 1

            if d_len == -1:
                d_len = int(element.hex(), 16)
    #   how many bits to store each dictionary element
    N = math.ceil(math.log2(len(dictio)))
    return dictio, N

def decompress(file_path, decompressed_path):
    print('Decompressing...')
    dictionary, N = read_dictionary(file_path)
 
    start = time.time()
    # clear output file
    try: open(decompressed_path, 'w').close()
    except: print('Unable to clear output file.')
    
    output = open(decompressed_path, 'ab')
    buff = ''
    skip = -1
    with open(file_path, 'rb') as file:
        # skip dictionary
        file.read(1 + len(dictionary))
        while (portion := file.read(1)):
            # convert portion to binary
            portion = bin(int(portion.hex(), 16))[2:].zfill(8)
            if skip < 0:
                skip = int(portion[:3], 2)
                portion = portion[3:]

            # add portion to buffer
            buff += portion
            # write only if there is more bits that should be skipped
            while len(buff) - skip >= N:
                output.write(dictionary[int(buff[:N], 2)])
                buff = buff[N:]
    output.close()
    stop = time.time()
    print(f'Finished in {stop - start}')


to_decompress = input('File to deompress: ')
decompress(to_decompress, 'decompressed.txt')