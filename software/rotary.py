import board
import digitalio
import time

class RotaryEncoder:
    def __init__(self, clk_pin=board.GP22, dt_pin=board.GP20, sw_pin=board.GP18,
                 left_pin=board.GP15, center_pin=board.GP14, right_pin=board.GP11):

        self.clk = digitalio.DigitalInOut(clk_pin)
        self.clk.direction = digitalio.Direction.INPUT
        self.clk.pull = digitalio.Pull.UP
        self.dt = digitalio.DigitalInOut(dt_pin)
        self.dt.direction = digitalio.Direction.INPUT
        self.dt.pull = digitalio.Pull.UP
        self.sw = digitalio.DigitalInOut(sw_pin)
        self.sw.direction = digitalio.Direction.INPUT
        self.sw.pull = digitalio.Pull.UP
        

        self.left = digitalio.DigitalInOut(left_pin)
        self.left.direction = digitalio.Direction.INPUT
        self.left.pull = digitalio.Pull.DOWN
        self.center = digitalio.DigitalInOut(center_pin)
        self.center.direction = digitalio.Direction.INPUT
        self.center.pull = digitalio.Pull.DOWN
        self.right = digitalio.DigitalInOut(right_pin)
        self.right.direction = digitalio.Direction.INPUT
        self.right.pull = digitalio.Pull.DOWN
        

        self.last_clk_state = self.clk.value
        self.last_button_states = {
            'left': False,
            'center': False,
            'right': False,
            'sw': True  
        }
        
        # List to store the last 10 actions and timestamps
        self.actions = []
        self.timestamps = []
        #actions are stored as int as follows:
        # 0: CW
        # 1: CCW
        # 2: SW_Pressed
        # 3: SW_Released
        # 4: LEFT_Pressed
        # 5: LEFT_Released
        # 6: CENTER_Pressed
        # 7: CENTER_Released
        # 8: RIGHT_Pressed
        # 9: RIGHT_Released

    def update(self):

        current_clk_state = self.clk.value

        if self.last_clk_state == 1 and current_clk_state == 0:

            if self.dt.value == 1:
                # Clockwise rotation
                self._log_action(0)
            else:
                # Counterclockwise rotation
                self._log_action(1)


        self.last_clk_state = current_clk_state
        

        current_sw_state = self.sw.value
        if current_sw_state != self.last_button_states['sw']:
            self._log_action((3 if current_sw_state else 2))
            self.last_button_states['sw'] = current_sw_state
        

        for button, pin in [("left", self.left), ("center", self.center), ("right", self.right)]:
            current_state = pin.value
            if current_state != self.last_button_states[button]:
                self._log_action(self.button_number(button) + (0 if current_state else 1))
                self.last_button_states[button] = current_state
        
        time.sleep(0.001)  # Small delay to debounce

    def button_number(self,name):
        if name == "left":
            return 4
        elif name == "center":
            return 6
        elif name == "right":
            return 8
        
    def _log_action(self, action):
        self.actions.append(action)
        self.timestamps.append(time.monotonic())
        if len(self.actions) > 10:
            self.actions.pop(0)
            self.timestamps.pop(0)

    def add_fake_action(self):
        self._log_action(100)

    def get_actions(self):
        return list(zip(self.actions, self.timestamps))
    
    def get_last_action(self):
        if self.actions:
            return (self.actions[-1], self.timestamps[-1])
        return None
    def get_last_action_time(self):
        if self.actions:
            return self.timestamps[-1]
        return None
    
    def convert_to_string(self, action):
        if action == 0:
            return 'CW'
        elif action == 1:
            return 'CCW'
        elif action == 2:
            return 'SW_Pressed'
        elif action == 3:
            return 'SW_Released'
        elif action == 4:
            return 'LEFT_Pressed'
        elif action == 5:
            return 'LEFT_Released'
        elif action == 6:
            return 'CENTER_Pressed'
        elif action == 7:
            return 'CENTER_Released'
        elif action == 8:
            return 'RIGHT_Pressed'
        elif action == 9:
            return 'RIGHT_Released'
        return 'Unknown'

    def check_if_back_button_pressed(self):
        # if last action was right pressed
        if self.actions[-1] == 8:
            return True
        else:
            return False

    def check_if_select_button_pressed(self):
        # if last two actions are right pressed and right released
        if self.actions[-2:] == [2,3]:
            return True
        else:
            return False
    
    def check_if_rotary_positive(self):
        # if last action is CW
        if self.actions[-1] == 0:
            return True
        else:
            return False
    
    def check_if_rotary_negative(self):
        # if last action is CCW
        if self.actions[-1] == 1:
            return True
        else:
            return False
    def drop_last_action(self):
        if self.actions:
            self.actions.pop()
            self.timestamps.pop()