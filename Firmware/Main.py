import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.oled import Oled, OledDisplayMode, OledReactionType
import busio
import adafruit_ssd1306

keyboard = KMKKeyboard()

keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler = EncoderHandler()
encoder_handler.pins = ((board.D6, board.D7, board.D9),)
encoder_handler.map = [((KC.VOLD, KC.VOLU, KC.F6),)]
keyboard.modules.append(encoder_handler)

i2c = busio.I2C(board.D5, board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

def oled_update(oled, keyboard):
    oled.fill(0)
    if keyboard.keys_pressed:
        oled.text("Fusion 360", 30, 0, 1)
        pressed = keyboard.keys_pressed
        oled.text("[E]" if (0,0) in pressed else " E ", 0, 8, 1)
        oled.text("[F]" if (0,1) in pressed else " F ", 42, 8, 1)
        oled.text("[D]" if (0,2) in pressed else " D ", 84, 8, 1)
        oled.text("[L]" if (1,0) in pressed else " L ", 0, 16, 1)
        oled.text("[M]" if (1,1) in pressed else " M ", 42, 16, 1)
        oled.text("[C]" if (1,2) in pressed else " C ", 84, 16, 1)
        oled.text(f"{len(pressed)} key(s)", 30, 24, 1)
    else:
        oled.text("Sivasankar's", 10, 0, 1)
        oled.text("Fusion 360 Pad", 10, 8, 1)
        oled.text("E F D", 10, 16, 1)
        oled.text("L M C", 10, 24, 1)
    oled.show()

oled_ext = Oled(
    OledDisplayMode.CUSTOM,
    oled_update,
    width=128,
    height=32
)
keyboard.extensions.append(oled_ext)

keyboard.keymap = [
    [KC.E, KC.F, KC.D, KC.L, KC.M, KC.C]
]

if __name__ == '__main__':
    keyboard.go()
