#importing libraries
from svgpathtools import svg2paths
from PIL import Image, ImageDraw
import numpy
from tqdm import tqdm


def svg_to_coordinates(lst):
    output=[]
    f=float
    for e in lst:
        figure=[]
        for i in range(len(e)/3):
            figure.append((f(e[i*3+1]),f(e[i*3+2])))
        output.append(figure)
    return output

paths, attributes = svg2paths('ground-truth/locations/270.svg')

paths_list=[]
for k, v in enumerate(attributes):
    paths_list.append(v['d'].split(" "))  # print d-string of k-th path in SVG


def crop(image,coordinates):
    # read image as RGB and add alpha (transparency)
    im = Image.open(image).convert("RGBA")

    # convert to numpy (for convenience)
    imArray = numpy.asarray(im)

    # create mask
    for counter, coords in tqdm(enumerate(coordinates)):
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
        newIm = Image.fromarray(newImArray, "RGBA")

        #outocrop Image
        newIm = autocrop_image(newIm)
        newIm.save("cropped/{}.png".format(counter))



crop("images/270.jpg",svg_to_coordinates(paths_list))