"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy


from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)

pixel_pin = board.A2
num_pixels = 90
pixel_pause = 15e-3 * 100/num_pixels# 10ms

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.35, auto_write=False)

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

chaser = [INDIGO, VIOLET, CYAN, CANARY, YELLOW, ORANGE, RED]

my_fns = [color_chase(GREEN, pixel_pause), poly_chase(chaser, num_pixels//33, 300, pixel_pause),
color_chase(BLUE, pixel_pause), color_chase(RED, pixel_pause)]

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        if uart_service.in_waiting:
            packet = Packet.from_stream(uart_service)
            if isinstance(packet, ColorPacket):
                print(packet.color)
                pixels.fill(packet.color)
                pixels.show()
            elif isinstance(packet, ButtonPacket) and packet.pressed:
                if packet.button == ButtonPacket.UP:
                    print("Button UP")
                    poly_chase(chaser, 3, 300, pixel_pause)
                if packet.button == ButtonPacket.DOWN:
                    print("Button DOWN")
                    color_chase(BLUE, pixel_pause)
                if packet.button == ButtonPacket.LEFT:
                    print("Button LEFT")
                    rainbow_cycle(25)
                if packet.button == ButtonPacket.RIGHT:
                    print("Button RIGHT")
                    pixels.fill(BLACK)
                    pixels.show()
                if packet.button == ButtonPacket.BUTTON_1:
                    print("Button 1")
                    pixels.fill(GREEN)
                    pixels.show()
                if packet.button == ButtonPacket.BUTTON_2:
                    print("Button 2")
                    pixels.fill(RED)
                    pixels.show()
                if packet.button == ButtonPacket.BUTTON_3:
                    print("Button 3")
                    pixels.fill(BLUE)
                    pixels.show()
                if packet.button == ButtonPacket.BUTTON_4:
                    print("Button 4")
                    pixels.fill(WHITE)
                    pixels.show()
