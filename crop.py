#importing libraries
from svgpathtools import svg2paths
from PIL import Image, ImageDraw
import numpy
from tqdm import tqdm
import os


def main():
    # run
    for i in [270,271,272,273,274,275,276,277,278,279,300,301,302,303,304]:
        print("{}.jpg started".format(i))
        crop(i)


def svg_to_coordinates(lst):
    """
    conversion function
    :param lst: list of lists of svg paths
    :return: list of list of coordinates as tuples
    """
    output=[]
    f=float
    for e in lst:
        figure=[]
        for i in range(len(e)//3):
            figure.append((f(e[i*3+1]),f(e[i*3+2])))
        output.append(figure)
    return output


def find_adjacents(value, items):
    i = items.index(value)
    return items[i+1:i+2]


def crop(page_number):
    """
    crop images by vector masks
    :param page_number: Page Number
    :return: cropped/page_number/cropped_image.png
    """
    try:
        # Create target Directory
        os.mkdir("cropped")
        print("Root Directory Created")
    except:
        print("Root Directory Already Exists.")

    #open vector graphic and crate list of lists of coordinates
    paths, attributes = svg2paths('ground-truth/locations/{}.svg'.format(page_number))
    paths_list = []

    #get ID's
    svg = open('ground-truth/locations/{}.svg'.format(page_number), "r")
    IDs=[]
    for aline in svg:
        try:
            splitted = (aline.split("\" "))
            IDs.append("".join(find_adjacents("stroke-width=\"1", splitted))[4:])
        except ValueError:
            pass
    svg.close()

    for k, v in enumerate(attributes):
        paths_list.append(v['d'].split(" "))  # print d-string of k-th path in SVG
    coordinates=svg_to_coordinates(paths_list)

    # read image as RGB and add alpha (transparency)
    im = Image.open('images/{}.jpg'.format(page_number)).convert("RGBA")

    # convert to numpy (for convenience)
    imArray = numpy.asarray(im)

    # create mask
    for counter, coords in (enumerate(tqdm(coordinates))):
        polygon = coords
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
        ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
        mask = numpy.array(maskIm)

        # assemble new image (uint8: 0-255)
        newImArray = numpy.empty(imArray.shape,dtype='uint8')

        # colors (three first columns, RGB)
        newImArray[:,:,:3] = imArray[:,:,:3]

        # transparency (4th column)
        newImArray[:,:,3] = mask*255



        # back to Image from numpy
        newIm = Image.fromarray(newImArray,"RGBA")

        #removing transparent borders
        bbox = newIm.convert("RGBa").getbbox()
        copped_image=newIm.crop(bbox)

        # apply image correction here

        #resizing every image to 100x100 aspect ratio
        resized=copped_image.resize((100,100), Image.ANTIALIAS)

        resized.save("cropped/{}.png".format(IDs[counter]))


if __name__ == '__main__':
    main()
