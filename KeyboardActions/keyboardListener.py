from pynput.keyboard import Controller, Key
from pynput import keyboard
import time
import sys, os

#Check if windows or mac
is_windows = os.name == 'nt'
resizeKey = Key.ctrl if is_windows else Key.cmd
def resizeWindow(zoom = 1):
    keyboard = Controller()
    for _ in range(20):
        with keyboard.pressed(resizeKey):
            keyboard.press('-')
            keyboard.release('-')
        # time.sleep(0.1)
    for _ in range(0, zoom):
        with keyboard.pressed(resizeKey):
            keyboard.press('+')
            keyboard.release('+')
    # time.sleep(0.1)
    del keyboard

# Define a key listener
class MyKeyListener:
    def __init__(self, key_actions={}):
        self.keys_pressed = set()
        self.key_actions = key_actions
        self.user_input= None
    def on_press(self, key):
        self.keys_pressed.add(str(key))

    def add_key_action(self, key, action):
        self.key_actions[str(key)] = action
    
    def remove_key_action(self, key):
        if str(key) in self.key_actions:
            del self.key_actions[str(key)]
    def add_key_actions(self, key_actions):
        self.key_actions = key_actions

    def clear_pressed_keys(self):
        self.keys_pressed.clear()

    def on_release(self, key):
        self.keys_pressed.discard(str(key))

    def is_pressed(self, key):
        return str(key) in self.keys_pressed

    # define what keys can be pressed
    #do the entire alphabet from a-z
    def is_a_pressed(self):
        return "'a'" in self.keys_pressed
    def is_b_pressed(self):
        return "'b'" in self.keys_pressed
    def is_c_pressed(self):
        return "'c'" in self.keys_pressed
    def is_d_pressed(self):
        return "'d'" in self.keys_pressed
    def is_e_pressed(self):
        return "'e'" in self.keys_pressed
    def is_f_pressed(self):
        return "'f'" in self.keys_pressed
    def is_g_pressed(self):
        return "'g'" in self.keys_pressed
    def is_h_pressed(self):
        return "'h'" in self.keys_pressed
    def is_i_pressed(self): 
        return "'i'" in self.keys_pressed
    def is_j_pressed(self):
        return "'j'" in self.keys_pressed
    def is_k_pressed(self):
        return "'k'" in self.keys_pressed
    def is_l_pressed(self):
        return "'l'" in self.keys_pressed
    def is_m_pressed(self):
        return "'m'" in self.keys_pressed
    def is_n_pressed(self):
        return "'n'" in self.keys_pressed
    def is_o_pressed(self):
        return "'o'" in self.keys_pressed
    def is_p_pressed(self):
        return "'p'" in self.keys_pressed
    def is_q_pressed(self):
        return "'q'" in self.keys_pressed
    def is_r_pressed(self):
        return "'r'" in self.keys_pressed
    def is_s_pressed(self):
        return "'s'" in self.keys_pressed
    def is_t_pressed(self):
        return "'t'" in self.keys_pressed
    def is_u_pressed(self):
        return "'u'" in self.keys_pressed
    def is_v_pressed(self):
        return "'v'" in self.keys_pressed
    def is_w_pressed(self):
        return "'w'" in self.keys_pressed
    def is_x_pressed(self):
        return "'x'" in self.keys_pressed
    def is_y_pressed(self):
        return "'y'" in self.keys_pressed
    def is_z_pressed(self):
        return "'z'" in self.keys_pressed
    
    #do the numbers from 0-9
    def is_0_pressed(self):
        return "'0'" in self.keys_pressed
    def is_1_pressed(self):
        return "'1'" in self.keys_pressed
    def is_2_pressed(self):
        return "'2'" in self.keys_pressed
    def is_3_pressed(self):
        return "'3'" in self.keys_pressed
    def is_4_pressed(self):
        return "'4'" in self.keys_pressed
    def is_5_pressed(self):
        return "'5'" in self.keys_pressed
    def is_6_pressed(self):
        return "'6'" in self.keys_pressed
    def is_7_pressed(self):
        return "'7'" in self.keys_pressed
    def is_8_pressed(self):
        return "'8'" in self.keys_pressed
    def is_9_pressed(self):
        return "'9'" in self.keys_pressed
    def get_pressed_number(self):
        if self.is_0_pressed():
            return '0'
        elif self.is_1_pressed():
            return '1'
        elif self.is_2_pressed():
            return '2'
        elif self.is_3_pressed():
            return '3'
        elif self.is_4_pressed():
            return '4'
        elif self.is_5_pressed():
            return '5'
        elif self.is_6_pressed():
            return '6'
        elif self.is_7_pressed():
            return '7'
        elif self.is_8_pressed():
            return '8'
        elif self.is_9_pressed():
            return '9'
        else:
            return False
    
    #See if wasd is pressed
    def wasd(self):
        if self.is_w_pressed():
            return "w"
        elif self.is_a_pressed():
            return "a"
        elif self.is_s_pressed():
            return "s"
        elif self.is_d_pressed():
            return "d"
        else:
            return False
    #se if any key is pressed and return that key
    def get_pressed_key(self):
        for key in self.keys_pressed:
            return key
        return False


    #Non keyboard charcters like enter 
    def is_left_arrow_pressed(self):
        return "Key.left" in self.keys_pressed
    def is_right_arrow_pressed(self):
        return "Key.right" in self.keys_pressed
    def is_up_arrow_pressed(self):
        return "Key.up" in self.keys_pressed
    def is_down_arrow_pressed(self):
        return "Key.down" in self.keys_pressed
    def is_backspace_pressed(self):
        return "Key.backspace" in self.keys_pressed
    def is_enter_pressed(self):
        return "Key.enter" in self.keys_pressed
    def is_tab_pressed(self):
        return "Key.tab" in self.keys_pressed
    def is_shift_pressed(self):
        return "Key.shift" in self.keys_pressed
    def is_space_pressed(self):
        return "Key.space" in self.keys_pressed
    def is_ctrl_pressed(self):
        return "Key.ctrl" in self.keys_pressed
    def is_esc_pressed(self):
        if "Key.esc" in self.keys_pressed:
            print("You have exited the program")
            sys.stdout.write("\033[?25h" + "\033[0m")
            return True
            # sys.exit()
        
    
    def is_smallQuote_pressed(self):
        return "'`'" in self.keys_pressed
    
    def check_keys(self):
        for key in list(self.keys_pressed):  # Create a copy of self.keys_pressed
            if key in self.key_actions:
                self.key_actions[key]()

        self.is_esc_pressed()

# Key_Listener = MyKeyListener()
# Listener = keyboard.Listener(
#     on_press=Key_Listener.on_press,
#     on_release=Key_Listener.on_release)

# #Use to call the key listener set something equal to it to get the keyboard
# def startKeyboard():
#     Key_Listener = MyKeyListener()
#     Listener = keyboard.Listener(
#         on_press=Key_Listener.on_press,
#         on_release=Key_Listener.on_release)
#     Listener.start()
#     # Key_Listener = MyKeyListener()
#     # Listener = keyboard.Listener(
#     #     on_press=Key_Listener.on_press,
#     #     on_release=Key_Listener.on_release)
#     # Listener.start()
#     # return [key_listener, listener]

# #Stops the current keybard 
# def stopKeyboard():
#     Listener.stop()
#     # del Listener

# startKeyboard()
#example
# if Key_Listener.is_1_pressed():
#     print("1")

#when getting keyboard input type in:
    # key_listener = MyKeyListener()
    #         listener = keyboard.Listener(
    #             on_press=key_listener.on_press,
    #             on_release=key_listener.on_release)