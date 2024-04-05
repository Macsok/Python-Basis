from PIL import Image

im = Image.open('parrot.jpg') # Can be many different formats.
pix = im.load()
print(im.size)  # Get the width and hight of the image for iterating over
print(pix[1, 1])  # Get the RGBA Value of the a pixel of an image
pix[1, 10] = (1, 1, 1)  # Set the RGBA Value of the image (tuple)
im.save('alive_parrot.png')  # Save the modified pixels as .png

def set_parity(bin_val, pix_tuple):
    """Sets first element in tuple to parity provided in bin_val argument"""
    # we concentrate only on first element of RGB vals.
    val = pix_tuple[0]

    # we check val parity, and return without changes if parity is correct
    if val % 2 == bin_val:
        return pix_tuple
    # we modify parity of val, if 0 we add, subtract otherwise
    else:
        if val != 0:
            val = val - 1
        else:
            val = val + 1
        # return new tuple
        return (val, pix_tuple[1], pix_tuple[2])


def encrypt(source_image_path, save_as, plain_text):
    # open image and load it into array of pixels
    image = Image.open(source_image_path)
    pixel = image.load()

    # convert text to binary representation
    bin_text = ''.join('{0:08b}'.format(ord(x), 'b') for x in plain_text)

    # check text length and convert to binary ([2:] to omit '0b')
    length = len(plain_text)
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
    image.save(save_as)

print(bin(102)[2:])
encrypt('parrot.jpg', 'out.jpg', 'a' * 1000)