import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid
from adafruit_hid.keycode import Keycode
import json
import time

# $ is for variable names
# ! is for function names
# & is for special keycodes
# &() is for special keycods which needs to be holded
# &(WAIT_CLICK) is for waiting for click

class KeyboardController:
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)
        self.keyboard_layout = KeyboardLayoutUS(self.keyboard)
        self.keycodes = dir(Keycode)
        self.key_functions = json.load(open("personal/key_functions.json"))
        self.variables = json.load(open("personal/secret.json"))
        self.typing_delay=0
        

    def type_string(self, string):
        self.keyboard_layout.write(string,delay=self.typing_delay)

    
    def press_special_key(self, *keycodes):
        for keycode in keycodes:
            self.keyboard.press(keycode)
        self.keyboard.release_all()
    
    def press_and_hold(self, *keycodes):
        for keycode in keycodes:
            self.keyboard.press(keycode)
    
    def release_all_keys(self):
        self.keyboard.release_all()

    def get_key_function_value(self, function_name):
        return self.key_functions[function_name]

    def get_variable_value(self, variable_name):
        return self.variables[variable_name]
    
    def replace_all_functions(self, code_line):
        #add space in front and back to avoid lots of problems
        code_line = " " + code_line + " "
        return_line = ""
        # firstly convert all functions in code line to its values 
        i=0
        while(i<len(code_line)):
            if code_line[i] == '!' and  code_line[i-1] != '`':
                return_line += self.replace_all_functions(self.get_key_function_value(code_line[i+1:code_line.index(' ', i+1)]))+" "
                i=code_line.index(' ', i+1)
            elif code_line[i] == '`' and code_line[i+1] == '!':
                i+=1
            else:
                return_line += code_line[i]
            i+=1

        return return_line

    def replace_all_variables(self, code_line):
        #add space in front and back to avoid lots of problems
        code_line = " " + code_line + " "
        return_line = ""
        # replace all variables in code line to its values
        i=0
        while(i<len(code_line)):
            if code_line[i] == '$' and  code_line[i-1] != '`':
                return_line += self.get_variable_value(code_line[i+1:code_line.index(' ', i+1)])+" "
                i=code_line.index(' ', i+1)
            elif code_line[i] == '`' and code_line[i+1] == '$':
                i+=1
            else:
                return_line += code_line[i]
            i+=1
        return return_line
    
    def execute_keycodes(self, keycodes,all_access=None):
        for keycode in keycodes:
            if keycode in self.keycodes:
                self.keyboard.press(getattr(Keycode, keycode))
            elif keycode.isdigit():
                time.sleep(int(keycode)/1000)
            elif keycode == "WAIT_CLICK":
                all_access.wait_for_select_button()
            else:
                print(f"Keycode {keycode} not found")
            time.sleep(self.typing_delay)
        time.sleep(self.typing_delay)
        self.keyboard.release_all()
    
    def execute_code_line(self, code_line,all_access=None):

        code_line = self.replace_all_functions(code_line)
        code_line = self.replace_all_variables(code_line)
        actions = code_line.split(" &")
        for action in actions:
            action = action.replace("`", "")
            if action[0] == '(':
                self.execute_keycodes(action[1:action.index(')')].split(" "),all_access)   
                self.type_string(action[action.index(')')+1:].strip())
                # print(action[1:action.index(')')].split(" "))
                # print(action[action.index(')')+1:])
            else:
                self.type_string(action.strip())
                # print(action)
        