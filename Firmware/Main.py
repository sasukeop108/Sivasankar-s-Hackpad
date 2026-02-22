from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
import board
import busio
import adafruit_ssd1306
import digitalio
import time
import gc

keyboard = KMKKeyboard()

keyboard.col_pins = (board.D0, board.D1, board.D2)
keyboard.row_pins = (board.D3, board.D8)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [
        KC.E, KC.F, KC.D,
        KC.L, KC.M, KC.C
    ]
]

encoder_handler = EncoderHandler()
encoder_handler.pins = (
    (board.D6, board.D7, board.D9),
)
encoder_handler.map = [
    ((KC.VOLD, KC.VOLU, KC.F6),)
]
keyboard.modules.append(encoder_handler)

class FusionOledDisplay:
    def __init__(self):
        self.i2c = busio.I2C(board.D5, board.D4)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=0x3C)
        self.oled.fill(0)
        self.oled.show()
        self.last_pressed_state = False
        self.last_update = 0
        self.update_interval = 0.1
        
    def update(self, keyboard):
        current_time = time.monotonic()
        if current_time - self.last_update < self.update_interval:
            return
        self.last_update = current_time
        
        keys_pressed = len(keyboard.keys_pressed) > 0
        
        self.oled.fill(0)
        
        if keys_pressed:
            self.show_fusion_grid(keyboard)
        else:
            self.show_idle()
        
        self.oled.show()
    
    def show_idle(self):
        self.oled.rect(0, 0, 127, 63, 1)
        self.oled.text("Sivasankar's", 20, 10, 1)
        self.oled.text("Fusion 360 Pad", 15, 20, 1)
        self.oled.text("E:Extrude L:Line", 10, 40, 1)
        self.oled.text("F:Fillet  M:Move", 10, 50, 1)
        self.oled.text("D:Dim    C:Circle", 10, 60, 1)
    
    def show_fusion_grid(self, keyboard):
        self.oled.text("Fusion 360", 30, 0, 1)
        self.oled.text("┌─────┬─────┬─────┐", 0, 8, 1)
        
        row0_cmds = ["E", "F", "D"]
        row0_str = "│"
        for col in range(3):
            if keyboard.keys_pressed and (0, col) in keyboard.keys_pressed:
                row0_str += f"  ●{row0_cmds[col]} │"
            else:
                row0_str += f"  {row0_cmds[col]}  │"
        self.oled.text(row0_str, 0, 16, 1)
        
        self.oled.text("├─────┼─────┼─────┤", 0, 24, 1)
        
        row1_cmds = ["L", "M", "C"]
        row1_str = "│"
        for col in range(3):
            if keyboard.keys_pressed and (1, col) in keyboard.keys_pressed:
                row1_str += f"  ●{row1_cmds[col]} │"
            else:
                row1_str += f"  {row1_cmds[col]}  │"
        self.oled.text(row1_str, 0, 32, 1)
        
        self.oled.text("└─────┴─────┴─────┘", 0, 40, 1)
        
        pressed_count = 0
        y_pos = 48
        for row in range(2):
            for col in range(3):
                if keyboard.keys_pressed and (row, col) in keyboard.keys_pressed:
                    idx = row * 3 + col
                    cmd_name = ["Extrude", "Fillet", "Dim", "Line", "Move", "Circle"][idx]
                    self.oled.text(f"► {cmd_name}", 10, y_pos, 1)
                    y_pos += 8
                    pressed_count += 1
                    if y_pos > 56:
                        break
            if y_pos > 56:
                break
        
        self.oled.text("ENC:Zoom/Fit", 70, 56, 1)

oled_display = FusionOledDisplay()
keyboard.extensions.append(oled_display)

if __name__ == '__main__':
    keyboard.go()
