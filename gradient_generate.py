#From https://jjmojojjmojo.github.io/time-based-fading.html

import board
import neopixel
import time

import adafruit_fancyled.adafruit_fancyled as fancy

BRIGHTNESS = 0.4

rgb = neopixel.NeoPixel(board.A2, 100, brightness=BRIGHTNESS, auto_write=False)

def make_gradient(colors, count=24, cycle=True):
    values = []
    ratio = 1.0/len(colors)
    for index, color in enumerate(colors):
        value = float(index*ratio)
        values.append((value, color))

    if cycle:
        values.append((1.0, colors[0]))

    palette = []
    for expanded in fancy.expand_gradient(values, count):
        palette.append(fancy.gamma_adjust(expanded, brightness=BRIGHTNESS).pack())

    return tuple(palette)

WHITE = fancy.CRGB(255, 255, 255)
BLACK = fancy.CRGB(0, 0, 0)
RED = fancy.CRGB(255, 0, 0)
GREEN = fancy.CRGB(0, 255, 0)
YELLOW = fancy.CRGB(255, 255, 0)
MAGENTA = fancy.CRGB(255, 0, 255)
CYAN = fancy.CRGB(0, 255, 255)
BLUE = fancy.CRGB(0, 0, 255)
ORANGE = fancy.CRGB(255, 127, 0)
VIOLET = fancy.CRGB(139, 0, 255)
INDIGO = fancy.CRGB(46, 43, 95)
PINK = fancy.CRGB(255, 127, 127)
MINT = fancy.CRGB(127, 255, 127)
ROBIN = fancy.CRGB(127, 127, 255)
CANARY = fancy.CRGB(255, 255, 127)

gradient = make_gradient([
    RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET
])

print("gradient = ", gradient)

index = 0

while True:
    rgb.fill(gradient[index])
    rgb.write()

    index += 1
    if index > len(gradient)-1:
        index = 0

    time.sleep(0.2)