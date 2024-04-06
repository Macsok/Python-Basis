from PIL import Image

# cheat sheet
# im = Image.open('parrot.jpg') # Can be many different formats.
# pix = im.load()
# print(im.size)  # Get the width and hight of the image for iterating over
# print(pix[1, 1])  # Get the RGBA Value of the a pixel of an image
# pix[1, 10] = (1, 1, 1)  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png

def set_parity(bin_val, pix_tuple):
    """Sets first element in tuple to parity provided in bin_val argument"""
    # we concentrate only on first element of RGB vals.
    val = int(pix_tuple[0])

    # we check val parity, and return without changes if parity is correct
    if val % 2 == int(bin_val):
        return pix_tuple
    # we modify parity of val, if 0 we add, subtract otherwise
    else:
        if val != 0:
            val = val - 1
        else:
            val = val + 1
        # return new tuple
        return (val, pix_tuple[1], pix_tuple[2])
    
def get_parity(pix_tuple):
    """Get parity of first element in tuple"""
    if int(pix_tuple[0]) % 2 == 0:
        return 0
    else:
        return 1

def encrypt(source_image_path, save_as, plain_text):
    """Encrypts provided text in image and saves it as a new image"""
    # open image and load it into array of pixels
    image = Image.open(source_image_path)
    pixel = image.load()

    # convert text to binary representation
    bin_text = ''.join('{0:08b}'.format(ord(x), 'b') for x in plain_text)

    # check text length and convert to binary ([2:] to omit '0b')
    length = len(bin_text)
    len_bin = bin(length)[2:]
    # we gave away 100 first bits for writing down length of the encrypted information
    to_write = '0' * (100 - len(len_bin)) + len_bin
    
    count = 0
    # for every pixel in image
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if count < 100:
                # set parity to the one in the text length string
                pixel[x, y] = set_parity(to_write[count], pixel[x, y])
            else:
                # we subtract 100 cause it is index of other string
                pixel[x, y] = set_parity(bin_text[count - 100], pixel[x, y])
            # increase counter
            count += 1
        # break if finished writing
            if count >= length + 100:
                break
        if count >= length + 100:
            break
    # save image
    image.save(save_as, 'png')


def decrypt(image_path):
    """Reads encrypted text from an image"""
    # load image
    image = Image.open(image_path)
    pixel = image.load()

    # initialize counter and strings
    count = 0
    text = ''
    bin_len = ''
    read_to = 1

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if count < 100:
                # appends parity of a pixel to string
                bin_len += str(get_parity(pixel[x, y]))

            # convert length of the secret text to int
            if count == 100:
                read_to = int(bin_len, 2)
                print(f'Length of the message (bits): {read_to}')

            # break if whole readed
            if read_to <= 0:
                break

            if count >= 100:
                # append binary values
                text += str(get_parity(pixel[x, y]))
                # decrease readed values counter
                read_to -= 1
            
            # increase counter
            count += 1
        # break if whole readed
        if read_to <= 0:
            break

    # convert binary information to ANSI
    plain_text = ''
    for i in range(int(bin_len, 2) // 8):
        plain_text += chr(int(text[i * 8 : (i + 1) * 8], 2))
    return plain_text


# needs to be saved in PNG to not be compressed
def interface():
    inp = input('e - encrypt, d - decrypt: ')
    
    if inp == 'e':
        in_file = input('Input file: ')
        out_file = input('Save as [.png]: ')
        text = input('Text to encrypt: ')
        print('Encryting...')
        encrypt(in_file, out_file, text)
        print('Finished')
    
    if inp == 'd':
        in_file = input('Image to read [.png]: ')
        print('Reading...')
        print('Decrypted text:', decrypt(in_file))
    
    return 0

interface()