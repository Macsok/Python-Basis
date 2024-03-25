import math

#   specify input and output files
file_path = 'do_kompresji.txt'
compressed_path = 'compressed.txt'

#def create_dictionary(file_path):
dictionary = {}
with open(file_path, 'r') as file:
    for line in file:
        for element in line:
            #   increase value if in the dictionary, add otherwise
            try: dictionary[element] = dictionary[element] + 1
            except: dictionary[element] = 1
#   sort elements in dictionary by keys (ASCII order)
dictionary = {key:dictionary[key] for key in sorted(dictionary.keys())}

#   assign values to elements in dictionary
ind = 0
k = 0
ind_dict = {}
for key in dictionary.keys():
    ind_dict[key] = ind
    ind += 1
    #   count number of elements to compress
    k += dictionary[key]

#   how many bits to store each dictionary element
N = math.ceil(math.log2(len(dictionary)))
#   how many bits should be added to form whole byte
R = (8 - (3 + N * k) % 8) % 8

#   clear output file
try: open(compressed_path, 'w').close()
except: print('Unable to clear output file.')

def save_in_binary(file_path, compressed_path, add_dictionary):
    #   open output file with append option
    with open(compressed_path, "a") as output:
        #   length of the dictionary
        output.write('{0:08b}'.format(len(dictionary)))

        #   add dictionary in ASCII
        if add_dictionary:
            for key in dictionary.keys():
                output.write(key)

        #   added bits - strored on 3 bits
        output.write('{0:08b}'.format(R)[-3:])

        #   read file to compress each element
        with open(file_path, 'r') as file:
            for line in file:
                for element in line:
                    #   append every element to output file (in binary), only N last bits
                    output.write('{0:08b}'.format(ind_dict[element])[-N:])
        
        #   add extra bits to make sure the output is in whole bytes
        output.write('0' * R)


def compress(file_path, compressed_path):
    #   open output file with append option
    with open(compressed_path, "a", encoding='utf-8') as output:
        #   length of the dictionary
        output.write(chr(len(dictionary)))

        #   add dictionary in ASCII
        for key in dictionary.keys():
            output.write(key)

        #   added bits - strored on 3 bits
        buff = '{0:08b}'.format(R)[-3:]

        #   read file to compress each element
        with open(file_path, 'r') as file:
            for line in file:
                for element in line:
                    #   append every element to buffor (in binary), only N last bits
                    buff += '{0:08b}'.format(ind_dict[element])[-N:]

                    #   if bit count >= 8 then store to file
                    if len(buff) >= 8:
                        #   convert first 8 bits to int then to char
                        output.write(chr(int(buff[:8], 2)))
                        buff = buff[8:]
        
        #   add extra bits to make sure the output is in whole bytes
        if R:
            buff += str('0' * R)
            output.write(chr(int(buff[:8], 2)))

compress(file_path, compressed_path)