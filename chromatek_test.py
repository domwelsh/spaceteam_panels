"""
Test script for Chromatek RGB Push Button Switch
Demonstrates various ways to control the switch
"""

import time
from chromatek_switch import ChromatekSwitch


def example_basic_control():
    """Example 1: Basic LED control"""
    print("Example 1: Basic LED Control")
    print("-" * 40)

    with ChromatekSwitch() as switch:
        # Turn on white
        print("Turning on (white)...")
        switch.turn_on()
        time.sleep(2)

        # Turn off
        print("Turning off...")
        switch.turn_off()
        time.sleep(1)


def example_color_changing():
    """Example 2: Change LED colors"""
    print("\nExample 2: Color Changing")
    print("-" * 40)

    with ChromatekSwitch() as switch:
        colors = [
            ("Red", 255, 0, 0),
            ("Green", 0, 255, 0),
            ("Blue", 0, 0, 255),
            ("Yellow", 255, 255, 0),
            ("Cyan", 0, 255, 255),
            ("Magenta", 255, 0, 255),
            ("Orange", 255, 165, 0),
            ("Purple", 128, 0, 128),
        ]

        for name, r, g, b in colors:
            print(f"Setting color to {name}...")
            switch.set_color(r, g, b)
            time.sleep(1)

        print("Turning off...")
        switch.turn_off()


def example_brightness_control():
    """Example 3: Brightness control"""
    print("\nExample 3: Brightness Control")
    print("-" * 40)

    with ChromatekSwitch() as switch:
        switch.turn_on(0, 0, 255)  # Blue

        # Fade down
        print("Fading down...")
        for brightness in range(255, 0, -25):
            switch.set_brightness(brightness)
            time.sleep(0.2)

        # Fade up
        print("Fading up...")
        for brightness in range(0, 255, 25):
            switch.set_brightness(brightness)
            time.sleep(0.2)

        switch.turn_off()


def example_button_polling():
    """Example 4: Read button state by polling"""
    print("\nExample 4: Button State Polling")
    print("-" * 40)
    print("Press the button (will check for 10 seconds)...")

    with ChromatekSwitch() as switch:
        switch.turn_on(255, 255, 0)  # Yellow indicator

        start_time = time.time()
        last_state = False

        while time.time() - start_time < 10:
            current_state = switch.get_button_state()

            # Detect state changes
            if current_state != last_state:
                if current_state:
                    print("Button PRESSED!")
                    switch.set_color(0, 255, 0)  # Green when pressed
                else:
                    print("Button RELEASED!")
                    switch.set_color(255, 255, 0)  # Yellow when released
                last_state = current_state

            time.sleep(0.1)

        switch.turn_off()


def example_button_events():
    """Example 5: Event-driven button handling"""
    print("\nExample 5: Event-Driven Button Handling")
    print("-" * 40)
    print("Press the button (will listen for 15 seconds)...")

    press_count = [0]  # Use list to modify in nested function

    def on_press():
        press_count[0] += 1
        print(f"Button pressed! (Total presses: {press_count[0]})")
        switch.set_color(255, 0, 0)  # Red on press

    def on_release():
        print("Button released!")
        switch.set_color(0, 255, 0)  # Green on release

    with ChromatekSwitch() as switch:
        switch.on_button_press(on_press)
        switch.on_button_release(on_release)

        # Initial state
        switch.set_color(0, 255, 0)

        # Wait for events
        time.sleep(15)

        print(f"\nTotal button presses: {press_count[0]}")
        switch.turn_off()


def example_interactive_toggle():
    """Example 6: Toggle LED on button press"""
    print("\nExample 6: Interactive Toggle")
    print("-" * 40)
    print("Press button to toggle LED color (will run for 20 seconds)...")

    led_state = [False]  # Use list to modify in nested function

    def toggle_led():
        led_state[0] = not led_state[0]
        if led_state[0]:
            switch.set_color(0, 255, 255)  # Cyan
            print("LED: ON (Cyan)")
        else:
            switch.turn_off()
            print("LED: OFF")

    with ChromatekSwitch() as switch:
        switch.on_button_press(toggle_led)
        switch.turn_off()

        time.sleep(20)


def main():
    """Run all examples"""
    print("=" * 40)
    print("Chromatek RGB Switch Test Suite")
    print("=" * 40)

    try:
        # Run individual examples
        example_basic_control()
        time.sleep(1)

        example_color_changing()
        time.sleep(1)

        example_brightness_control()
        time.sleep(1)

        example_button_polling()
        time.sleep(1)

        example_button_events()
        time.sleep(1)

        example_interactive_toggle()

        print("\n" + "=" * 40)
        print("All tests completed!")
        print("=" * 40)

    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
