# Chromatek RGB Push Button Switch Controller

Python library for controlling a Chromatek RGB push button switch connected to a Raspberry Pi 4 Model B.

## Hardware Specifications

- **Model**: AFK Tech RGB Push Button Switch
- **Operation Mode**: Push Button
- **Current Rating**: 5 Amps
- **Operating Voltage**: 5V DC
- **Contact Type**: Normally Open
- **Circuit Type**: 1-way

## Wiring Configuration

| Chromatek Pin | Raspberry Pi Pin | Description |
|---------------|------------------|-------------|
| PIN 1 (VDD) | 5V | Power supply |
| PIN 2 (Data In) | GPIO 18 | RGB LED data (WS2812B protocol) |
| PIN 4 (Ground) | GND | Ground |
| C (Common) | GND | Button common |
| NO (Normally Open) | GPIO 23 | Button state detection |

## Installation

### Prerequisites

1. **Enable SPI** (required for WS2812B control):
```bash
sudo raspi-config
# Navigate to: Interfacing Options > SPI > Enable
```

2. **System dependencies**:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: The `rpi_ws281x` library may require root privileges to access GPIO. You might need to run your scripts with `sudo`:

```bash
sudo python3 chromatek_test.py
```

## Usage

### Basic Example

```python
from chromatek_switch import ChromatekSwitch

# Create switch controller
with ChromatekSwitch() as switch:
    # Turn on LED (white)
    switch.turn_on()

    # Set specific color (red)
    switch.set_color(255, 0, 0)

    # Turn off
    switch.turn_off()
```

### Color Control

```python
with ChromatekSwitch() as switch:
    # Turn on with specific color
    switch.turn_on(red=0, green=255, blue=0)  # Green

    # Change color
    switch.set_color(255, 0, 255)  # Magenta

    # Adjust brightness (0-255)
    switch.set_brightness(128)  # 50% brightness
```

### Button State Detection

#### Polling Method

```python
with ChromatekSwitch() as switch:
    if switch.get_button_state():
        print("Button is pressed!")
    else:
        print("Button is released!")
```

#### Event-Driven Method

```python
with ChromatekSwitch() as switch:
    def on_press():
        print("Button pressed!")
        switch.set_color(255, 0, 0)  # Red

    def on_release():
        print("Button released!")
        switch.set_color(0, 255, 0)  # Green

    switch.on_button_press(on_press)
    switch.on_button_release(on_release)

    # Keep program running to receive events
    input("Press Enter to exit...\n")
```

## API Reference

### ChromatekSwitch Class

#### Methods

- **`__init__(brightness=255)`**
  - Initialize the switch controller
  - `brightness`: LED brightness (0-255)

- **`set_color(red, green, blue)`**
  - Set LED to specific RGB color
  - Each color channel: 0-255

- **`turn_on(red=255, green=255, blue=255)`**
  - Turn on LED (default: white)
  - Optional: specify RGB values

- **`turn_off()`**
  - Turn off LED (set to black)

- **`set_brightness(brightness)`**
  - Adjust LED brightness
  - `brightness`: 0-255

- **`get_button_state()`**
  - Read current button state
  - Returns: `True` if pressed, `False` if released

- **`on_button_press(callback)`**
  - Register callback for button press events
  - `callback`: Function to call when pressed

- **`on_button_release(callback)`**
  - Register callback for button release events
  - `callback`: Function to call when released

- **`cleanup()`**
  - Clean up GPIO resources
  - Automatically called when using context manager

## Test Suite

Run the comprehensive test suite to verify functionality:

```bash
sudo python3 chromatek_test.py
```

The test suite includes:
1. Basic LED control (on/off)
2. Color changing (multiple colors)
3. Brightness control (fade in/out)
4. Button state polling
5. Event-driven button handling
6. Interactive toggle mode

## Troubleshooting

### Permission Errors

If you get permission errors accessing GPIO:
```bash
# Run with sudo
sudo python3 your_script.py

# Or add user to gpio group
sudo usermod -a -G gpio $USER
sudo reboot
```

### LED Not Lighting Up

1. Verify 5V power connection
2. Check GPIO 18 connection (must be PWM-capable pin)
3. Ensure ground connections are secure
4. Try adjusting brightness: `switch.set_brightness(255)`

### Button Not Responding

1. Verify GPIO 23 connection
2. Check Common (C) to GND connection
3. Test with polling method first before event-driven
4. Ensure proper debouncing (200ms default)

### Import Errors

If `rpi_ws281x` fails to import:
```bash
# Install build dependencies
sudo apt-get install gcc make build-essential python3-dev scons swig

# Reinstall library
sudo pip3 install rpi_ws281x
```

## Notes

- **Root Access**: The WS2812B protocol requires precise timing, so root access (`sudo`) is typically needed
- **PWM Conflict**: GPIO 18 uses hardware PWM. Avoid using other PWM features simultaneously
- **Debouncing**: Button events include 200ms debounce time to prevent false triggers
- **Single LED**: This configuration assumes one RGB LED in the switch (LED_COUNT=1)

## License

This project is provided as-is for controlling Chromatek RGB switches with Raspberry Pi.
