import serial
import time

try:
    arduino = serial.Serial("COM11", 9600, timeout=1)

    print("⏳ Waiting for ESP32 to reset...")
    time.sleep(3) # Give it generous time to boot

    # CLEAR the buffer to remove "boot garbage"
    arduino.reset_input_buffer()

    print("📤 Sending: Hello")
    arduino.write(b"Hello\n")

    # Wait a bit for the reply
    time.sleep(2)

    if arduino.in_waiting > 0:
        response = arduino.read(arduino.in_waiting).decode('utf-8', errors='ignore')
        print(f"✅ Received: {response}")
    else:
        print("❌ No response received.")

except Exception as e:
    print(f"Error: {e}")