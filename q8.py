from enum import Enum
from util import slurp, split_every
from itertools import starmap

def part1():
    """
    image is split into layers of width*height
    find layer with smallest number of zeros
    return number of 1s * number of 2s
    """
    image = slurp('inputs/q08')
    width, height = 25, 6
    layers = split_every(width * height, image)
    fewestZeroLayer = min(layers, key=lambda l: l.count('0'))
    print(fewestZeroLayer.count('1') * fewestZeroLayer.count('2'))

def part2():
    """
    stack the layers: first layer in front, last layer in back
    0 = black, 1 = white, 2 = transparent
    therefore black/white overlap everything, and transparent overlaps nothing
    """
    image = slurp('inputs/q08')
    width, height = 25, 6
    combined = combineLayers(image, width, height)
    print(layerToImage(combined, width))

def part2_test():
    test = "0222112222120000"
    print(''.join(combineLayers(test, 2, 2)))

class Color(Enum):
    BLACK = '0'
    WHITE = '1'
    TRANSPARENT = '2'

def combineLayers(image, width, height):
    layers = split_every(width * height, image)

    # Start with transparent canvas
    canvas = Color.TRANSPARENT.value * (width * height)

    def applyPixel(oldValue, newValue):
        """ apply newValue behind oldValue """
        if oldValue == Color.TRANSPARENT.value:
            return newValue
        else:
            return oldValue

    for layer in layers:
        canvas = starmap(applyPixel, zip(canvas, layer))

    return canvas

def layerToImage(image, width):
    """
    images are stored as a long string of chars. this function adds newlines
    so the image can be printed and viewed by a human, and removes transparent
    pixels
    """
    image = '\n'.join(''.join(chunk) for chunk in split_every(width, image))
    # Remove transparent pixels
    image = image.replace('2', ' ')
    # Make image more readable
    image = image.replace('0', '.')
    image = image.replace('1', '#')
    return image

part2()
