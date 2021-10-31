"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel

pixel_pin = board.A2
num_pixels = 90
pixel_pause = 15e-3 # 10ms

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)


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


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
chaser = [YELLOW, YELLOW, YELLOW, GREEN, PURPLE, RED]

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
    color_chase(PURPLE, pixel_pause)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow