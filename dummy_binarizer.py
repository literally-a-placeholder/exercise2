from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

img = Image.open("270-19.png")
arr = np.asarray(img)

arr = (arr > 130)*255

newIm = Image.fromarray(np.uint8(arr))
newImBW = Image.new("RGBA", newIm.size, "WHITE")
newImBW.paste(newIm, (0,0), newIm)
newImBW.convert('L').save('dummy270-19.png')
