from PIL import Image
import easygui






def encoder(EncodeString, ImageBytes):
    imagelist = list(ImageBytes)
    if(len(EncodeString) > (len(imagelist)/8)-8):
        raise ValueError("String too big for image")
        return None;
    currentpixel = 0;
    EncodeString = EncodeString + '/' #end char
    for char in EncodeString:
        if char == '/':
            writestring = '00000100'
        else:
            writestring = str(bin(ord(char))[2:].zfill(8)).replace('b', '')
        for bit in writestring:
            pixelRGBvalue = str(imagelist[currentpixel])
            pixelRGBvalue = pixelRGBvalue[:-1] + bit
            pixelRGBvalue = int(pixelRGBvalue)
            imagelist[currentpixel] = pixelRGBvalue
            currentpixel += 1


    return imagelist


def decoder(EncodedBytes):
    imagelist = list(EncodedBytes)
    content = [str(i)[-1:] for i in imagelist]
    contentString = ''.join(content);
    n = 8
    contentlist = [contentString[i:i+n] for i in range(0, len(contentString), n)]
    return_string = ''
    i = 0
    while contentlist[i] != '00000100':
        charNUM = int(contentlist[i], 2)
        char = chr(charNUM)
        return_string += char
        i += 1

    return return_string



def Encode_to_file( imageLocation, EncodeString, result_location):
    imageObject = Image.open(imageLocation)
    listOFrgb = encoder(EncodeString, imageObject.tobytes())
    newIMAGEbytes = bytes(listOFrgb)
    size = tuple(imageObject.size)
    #print(type(size))
    new_img = Image.frombytes('RGB', size, newIMAGEbytes)
    new_img.save(result_location)

def DecodeFromFile( filelocation):
    img = Image.open(filelocation)
    secret = decoder(img.tobytes())
    return secret


    
def GUIencode():
    print('Pick sample picture')
    file_location = easygui.fileopenbox(filetypes='.png')
    if file_location == None:
        print('You must pick a image file')
        return
    print('Type the encoded message or write //f for file options')
    result = input(':: ')
    string_to_encode = ''
    if result == '//f':
        text_location = easygui.fileopenbox(filetypes='*.txt')
        try:
            with open(text_location, 'r') as file:
                data = file.read()
            string_to_encode = data
        except:
            print('chose a file')
            return
    else:
        string_to_encode = result;

    save_loc = easygui.filesavebox(filetypes='.png')
    Encode_to_file(file_location, string_to_encode, save_loc)
    
def GUIdecoder():
    print('Pick encoded picture')
    file_location = easygui.fileopenbox(filetypes='png')
    stringreturn = DecodeFromFile(file_location)
    r = input("Press p for print or f to save to file ")
    if r == 'f':
        save_loc = easygui.filesavebox()
        with open(save_loc, 'w+') as f:
            f.write(stringreturn)
    else:
        print(stringreturn)

def GUIswitcher():
    print('Press e for encoding or d for decoding')
    r = input(':: ')
    if r == 'e':
        GUIencode()
    elif r == 'd':
        GUIdecoder()
    
while True:
    GUIswitcher()
