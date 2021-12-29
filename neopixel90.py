"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

pixel_pin = board.A2
num_pixels = 90
pixel_pause = 15e-3 # 10ms

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=True)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

def single_chase(color, wait):
    for idx in range(1, num_pixels - 1):
        pixels[idx] = color
        pixels[idx - 1] = BLACK
        pixels.show()
        time.sleep(wait)

def poly_chase(color_array, dup_count, pix_count, wait):
    dup_interval = num_pixels//dup_count
    for idx in range(0,pix_count): # distance travelled
    # for idx in range(chase_size, num_pixels - chase_size):  
        for dupe in range(dup_count):
            for px in enumerate(color_array):
                pixels[(dup_interval *dupe + idx + px[0])%num_pixels] = px[1]
            pixels[(dup_interval *dupe + idx -1)%num_pixels] = BLACK

        pixels.show()
        time.sleep(wait)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


WHITE = fancy.CRGB(255, 255, 255).pack()
BLACK = fancy.CRGB(0, 0, 0).pack()
RED = fancy.CRGB(255, 0, 0).pack()
GREEN = fancy.CRGB(0, 255, 0).pack()
YELLOW = fancy.CRGB(255, 255, 0).pack()
MAGENTA = fancy.CRGB(255, 0, 255).pack()
CYAN = fancy.CRGB(0, 255, 255).pack()
BLUE = fancy.CRGB(0, 0, 255).pack()
ORANGE = fancy.CRGB(255, 127, 0).pack()
VIOLET = fancy.CRGB(139, 0, 255).pack()
INDIGO = fancy.CRGB(46, 43, 95).pack()
PINK = fancy.CRGB(255, 127, 127).pack()
MINT = fancy.CRGB(127, 255, 127).pack()
ROBIN = fancy.CRGB(127, 127, 255).pack()
CANARY = fancy.CRGB(255, 255, 127).pack()

print("Green", GREEN)
print (dir(GREEN))
chaser = [INDIGO, VIOLET, YELLOW, ORANGE, RED]

while True:
    poly_chase(chaser, 3, 300, pixel_pause)
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)

    color_chase(RED, pixel_pause)  # Increase the number to slow down the color chase
    color_chase(YELLOW, pixel_pause)
    color_chase(GREEN, pixel_pause)
    color_chase(CYAN, pixel_pause)
    color_chase(BLUE, pixel_pause)
    color_chase(VIOLET, pixel_pause)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow