import time
import random

def pattern_checker(patterns, action):
    for key, value in patterns.items():
        len_of_action = len(action)
        key=convert_key_to_int(key)
        if len_of_action >= len(key): 
            if key == action[len_of_action-len(key):]:
                return value
    return None




def convert_key_to_int(key):
    split_key = key.split(" ")
    for i in range(len(split_key)):
        split_key[i] = press_char_to_int(split_key[i])
    
    return split_key




def get_nested_value(scroll, menu_tracker):
    key_list = list(map(str,menu_tracker))
    current = scroll
    oled_text = ""
    for key in key_list[:-1]:
        if key in current:
                oled_text += current[key]["oled"] + ">"
                current = current[key]["value"]
        else:
            return None  # Key not found
    if key_list[-1] in current:
        total_child=len(current)
        current = current[key_list[-1]]
    else:
        return None
    return current,oled_text,total_child
        


# Note: action to key mapping
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

def press_char_to_int(key):
    if  key == "CW":
        return 0
    elif key == "CCW":
        return 1
    elif key == "SP":
        return 2
    elif key == "SR":
        return 3
    elif key == "LP":
        return 4
    elif key == "LR":
        return 5
    elif key == "CP":
        return 6
    elif key == "CR":
        return 7
    elif key == "RP":
        return 8
    elif key == "RR":
        return 9

    

## all special functions are down here

def run_special_function(function_no,keyboard_object,delay_object):
    if (function_no==0):
        return
    elif (function_no==1):
        return







class delay_handler:
    def __init__(self):
        self.last_time=time.monotonic()
        self.delay_set=0
    def reset_timer(self):
        self.last_time=time.monotonic()
    def set_delay(self,delay):
        self.delay_set=delay
        self.reset_timer()
    def get_time_diff(self):
        return time.monotonic()-self.last_time
    def delay_complete(self):
        return self.get_time_diff()>self.delay_set
    

class all_access_functions:
    def __init__(self,oled_object,rotary_object,keyboard_object,delay_object):
        self.oled=oled_object
        self.rotary=rotary_object
        self.keyboard=keyboard_object
        self.delay=delay_object

    def wait_for_select_button(self):
        last_action_time = self.rotary.get_last_action_time()
        self.oled.clear()
        self.oled.print_text("waiting \n for \n select",x=10,y=10)
        while not ((self.rotary.check_if_select_button_pressed() or self.rotary.check_if_back_button_pressed()) and self.rotary.get_last_action_time() != last_action_time): 
            self.rotary.update()
        self.oled.clear()
        if self.rotary.check_if_select_button_pressed():
            self.rotary.drop_last_action()
            return True
        else:
            self.rotary.drop_last_action()
            return False
        


