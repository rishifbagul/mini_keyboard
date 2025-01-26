# Mini-Keyboard

This open-source project is a versatile system that integrates a rotary encoder, an OLED display, and keyboard automation to create an interactive menu system. It is designed to simplify repetitive tasks by allowing users to navigate through menus using a rotary encoder and execute predefined keyboard shortcuts or commands.

## Prerequisites

Before getting started, ensure that your Raspberry Pi Pico is set up with **CircuitPython**. Follow these steps:

1. **Install CircuitPython**:
   - Download the latest CircuitPython UF2 file from the [official CircuitPython website](https://circuitpython.org/board/raspberry_pi_pico/).
   - Connect your Raspberry Pi Pico to your computer via USB while holding the BOOTSEL button.
   - Drag and drop the downloaded UF2 file onto the RPI-RP2 drive that appears.

2. **Copy the Code**:
   - After CircuitPython is installed, the Raspberry Pi Pico will appear as a drive named `CIRCUITPY`.
   - Copy the entire contents of the `software` directory from this repository to the `CIRCUITPY` drive.

3. **Configure JSON Files**:
   - Modify the `key_functions.json`, `scroll.json`, and `pattern.json` files to define your desired shortcuts, menus, and patterns. Detailed explanations for each file are provided below.

---

## Features

- **Rotary Encoder Navigation**: Navigate through menus using a rotary encoder with clockwise (CW) and counterclockwise (CCW) rotation.
- **OLED Display**: Display menu options and feedback on an OLED screen.
- **Keyboard Automation**: Execute predefined keyboard shortcuts or commands using the `keyboard.py` module.
- **Customizable Menus**: Define menus and actions in `scroll.json`.
- **Pattern Recognition**: Execute commands based on specific rotary encoder and button press patterns defined in `pattern.json`.
- **Key Functions**: Define complex keyboard shortcuts and sequences in `key_functions.json`.

---

## Configuration Files

### `key_functions.json`

This file defines keyboard shortcuts and sequences that can be executed by the system. Each key function is a string that represents a sequence of key presses, delays, and special key codes.

#### Example:
```json
{
    "admin_login": "$admin_username &(TAB) $admin_password &(ENTER)",
    "laptop_login": "$laptop_password &(ENTER)",
    "open_cmd_prompt": "&(WINDOWS R) &(500) cmd &(ENTER) &(2000)"
}

- **`$`**: Denotes a variable that will be replaced with its corresponding value from `secret.json`.
- **`&()`**: Denotes a special key code or a delay. For example, `&(WINDOWS R)` simulates pressing the Windows key and R, and `&(500)` introduces a 500ms delay.
- **`!`**: Denotes a user-defined function that can be executed by the system. user-defined functions are defined in `key_functions.py`.
---

### `scroll.json`

This file defines the menu structure and the actions associated with each menu option. Each menu option can either execute a command or navigate to a submenu.

#### Example:
```json
{
    "0": {
        "name": "git lab menu",
        "oled": "Git",
        "value": {
            "0": {
                "name": "git status",
                "oled": "status",
                "auto_type": true,
                "value": "git status"
            },
            "1": {
                "name": "git add",
                "oled": "add",
                "auto_type": true,
                "value": "git add ."
            }
        }
    }
}

- **`name`**: The name of the menu option.
- **`oled`**: The text displayed on the OLED screen for this option.
- **`value`**: The action to be executed when the option is selected. This can be a command string or a submenu.
- **`auto_type`**: If `true`, the command will be automatically typed when the option is selected.

---

### `pattern.json`

This file defines specific sequences of rotary encoder and button presses that trigger predefined actions. Each pattern is a string of actions separated by spaces.

#### Example:
```json
{
    "RP CP CR RR": "!laptop_login",
    "RP CP CR CP CR RR": "!laptop_linux_login"
}

- **Action Codes**:
  - `RP`: Right button pressed.
  - `RR`: Right button released.
  - `CP`: Center button pressed.
  - `CR`: Center button released.
  - `LP`: Left button pressed.
  - `LR`: Left button released.
  - `CW`: Clockwise rotation.
  - `CCW`: Counterclockwise rotation.

- **`!`**: Denotes a user-defined function that can be executed by the system. user-defined functions are defined in `key_functions.py`.
- **Patterns**: Each pattern is a sequence of action codes that, when detected, will trigger the corresponding action defined in `key_functions.json`.

---

## Usage

1. **Configuration**: Modify `key_functions.json`, `scroll.json`, and `pattern.json` to define your desired shortcuts, menus, and patterns.
2. **Run**: The system will automatically start when the Raspberry Pi Pico is powered on. Use the rotary encoder to navigate through the menus and execute commands.

---

## Example Workflow

1. **Navigate to Git Menu**: Rotate the encoder to select the "Git" menu on the OLED display.
2. **Select Git Status**: Rotate the encoder to highlight "status" and press the select button to execute `git status`.
3. **Pattern Recognition**: Press the right button, then the center button, then release both in sequence to trigger the `!laptop_login` command.


---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code follows the project's coding standards and includes appropriate documentation.

---

## License

This project is licensed under the Open Source MIT License. 

---

## Acknowledgments

- Thanks to the Adafruit community for their excellent libraries and tutorials.

---

Feel free to explore the code, customize it for your needs, and contribute to its development!