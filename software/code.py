import board
import busio
from oled import *
from rotary import *
import digitalio
import time
from keyboard import *
from func import *







oled = OLED()
encoder = RotaryEncoder()
keyboard = KeyboardController()
delay=delay_handler()
pattern = json.load(open("pattern.json"))
menu = json.load(open("scroll.json"))

last_action_time=0
menu_tracker = [0]
special_function_value=0        # 0 when no special function is active
current_index,oled_text,menu_width=get_nested_value(menu,menu_tracker)
while True:
    encoder.update()
    run_special_function(special_function_value,keyboard_object=keyboard,delay_object=delay)
    if  encoder.timestamps and last_action_time != encoder.timestamps[-1]:
        last_action_time = encoder.timestamps[-1]
        
        # stop the running special function
        special_function_value=0
        # for i in range(10):
        #     #keyboard.execute_code_line("2")
        #     keyboard.press_special_key(Keycode.a)

        # check patterns
        pattern_function = pattern_checker(pattern, encoder.actions)
        if pattern_function != None:
            oled.update_text(pattern_function)
            keyboard.execute_code_line(pattern_function)
        
        current_menu_index = get_nested_value(menu, menu_tracker)

        # check menu
        if encoder.check_if_rotary_positive():
            menu_tracker[-1] += 1
            if menu_tracker[-1] >= menu_width:
                menu_tracker[-1] = 0
        elif encoder.check_if_rotary_negative():
            menu_tracker[-1] -= 1
            if menu_tracker[-1] < 0:
                menu_tracker[-1] = menu_width - 1
        elif encoder.check_if_select_button_pressed():
            if isinstance(current_index["value"], dict):
                menu_tracker.append(0)
            else:
                if(isinstance(current_index["value"],int)):
                    special_function_value=current_index["value"]
                else:
                    keyboard.execute_code_line("!clear_termial_line")
                    keyboard.execute_code_line(current_index["value"])
                    keyboard.execute_code_line("&(ENTER)")
        elif encoder.check_if_back_button_pressed():
            if len(menu_tracker) > 1:
                menu_tracker.pop()
                special_function_value=0
        
        current_index,oled_text,menu_width=get_nested_value(menu,menu_tracker)
        oled.update_text("menu>"+oled_text,x=0,y=55)
        oled.print_text(current_index["oled"],x=0,y=20,scale=1)
        if "auto_type" in current_index and current_index["auto_type"]:
            keyboard.execute_code_line("!clear_termial_line")
            keyboard.execute_code_line(current_index["value"])
