import keyboard
import  hashlib
import binascii
import json
def get_json_filename():
    while True:
        filename = input("Enter the JSON filename in the current folder: ")
        try:
            with open(filename, 'r') as f:
                pass  # Check if file can be opened
                f.close()
            return filename
        except IOError as e:
            print(f"Error: Cannot open the file. {e}. Please try again.")

def explain_buttons():
    print("\nButton Mappings:")
    print("A/a = Anti-clockwise step (CCW)")
    print("D/d = Clockwise step (CW)")
    print("Left Arrow = LEFT_Pressed, LEFT_Released")
    print("Right Arrow = RIGHT_Pressed, RIGHT_Released")
    print("Up Arrow = CENTER_Pressed, CENTER_Released")
    print("\nEnter your password using the above keys. Press Enter to finish.\n")


def record_password():
    events = []
    pressed_keys = set()  # Track pressed keys to avoid repeats
    
    def on_key_event(e):
        nonlocal events
        if e.event_type == keyboard.KEY_DOWN:
            # Check if the key is already pressed (to avoid repeats)
            if e.name in pressed_keys:
                return
            pressed_keys.add(e.name)
            
            if e.name.lower() == 'a':
                events.append(1)
                print('*', end='', flush=True)
            elif e.name.lower() == 'd':
                events.append(0)
                print('*', end='', flush=True)
            elif e.name == 'left':
                events.append(4)
                print('*', end='', flush=True)
            elif e.name == 'right':
                events.append(8)
                print('*', end='', flush=True)
            elif e.name == 'up':
                events.append(6)
                print('*', end='', flush=True)
        elif e.event_type == keyboard.KEY_UP:
            # Remove from pressed keys
            if e.name in pressed_keys:
                pressed_keys.remove(e.name)
            if e.name == 'left':
                events.append(5)
                print('*', end='', flush=True)
            elif e.name == 'right':
                events.append(9)
                print('*', end='', flush=True)
            elif e.name == 'up':
                events.append(7)
                print('*', end='', flush=True)
    
    keyboard.hook(on_key_event)
    print("Start entering your password...")
    keyboard.wait('enter')
    keyboard.unhook_all()
    print()  # New line after Enter
    return events

def is_valid_password(key_str):
    if not (8 <= len(key_str)):
        return False
    return True


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def crypto_process(key_str, data):
    if not is_valid_password(key_str):
        raise ValueError("Invalid key! Must be 8-30 digits (1-5)")
    
    key_bytes = key_str.encode('utf-8')
    key_hash = hashlib.sha256(key_bytes).digest()
    
    result = bytearray()
    counter = 0
    
    for i in range(0, len(data), 32):
        counter_bytes = counter.to_bytes(4, 'big')
        keystream = hashlib.sha256(key_hash + counter_bytes).digest()
        
        chunk = data[i:i+32]
        processed_chunk = xor_bytes(chunk, keystream[:len(chunk)])
        
        result.extend(processed_chunk)
        counter += 1
    
    return bytes(result)

def encrypt(key_str, plaintext):
    plain_bytes = plaintext.encode('utf-8')
    encrypted_bytes = crypto_process(key_str, plain_bytes)
    # Use binascii for base64 encoding
    return binascii.b2a_base64(encrypted_bytes).decode('utf-8').strip()

def decrypt(key_str, ciphertext):
    # Use binascii for base64 decoding
    encrypted_bytes = binascii.a2b_base64(ciphertext)
    decrypted_bytes = crypto_process(key_str, encrypted_bytes)
    return decrypted_bytes.decode('utf-8')


def main():
    filename = get_json_filename()
    explain_buttons()
    password_events = record_password()
    print("\nPassword recorded as:")
    password_str = ''.join(map(str, password_events))
    file=json.load(open(filename, 'r'))
    for key in file:
        file[key]= encrypt(password_str, file[key])
    with open("secret.json", 'w') as f:
        json.dump(file, f)
    print("Encrypted secrets saved to secret.json")



if __name__ == "__main__":
    main()