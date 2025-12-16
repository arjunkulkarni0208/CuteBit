import ollama
import json
import speech_recognition as sr
import serial
import time
from time import sleep

# --- SERIAL SETUP (Standard Industry Way) ---
try:
    # timeout=1 prevents hanging if Arduino disconnects
    car = serial.Serial("COM11", 115200, timeout=1)
    time.sleep(2) # CRITICAL: Wait for Arduino to reboot after connection
    print("✅ Connected to CuteBit via Serial")
except:
    print("⚠️ Arduino not connected. Running in simulation mode.")
    car = None

SYSTEM_PROMPT = """
You are CuteBit, a helpful robot. Reply in JSON ONLY.
Format: {"response": "text", "action": "move_cmd", "emotion": "emote_cmd"}
Actions: stop, forward, backward, left, right
Emotions: happy, angry, tired, neutral
"""

def send_robot_command(action_id, emotion_id):
    """
    Sends a formatted string "action,emotion\n" directly to Arduino.
    Example: "1,2\n"
    """
    if car:
        # Create string "1,2\n"
        command = f"{action_id},{emotion_id}\n"
        # Encode to bytes and write
        car.write(command.encode('utf-8'))
        print(f"📤 Sent: {command.strip()}")
    else:
        print(f"🚫 Simulating: {action_id}, {emotion_id}")

def execute_logic(action, emotion):
    # Map text to numbers
    move_map = {"stop": 0, "forward": 1, "right": 2, "left": 3, "backward": 4}
    emotion_map = {"neutral": 0, "happy": 1, "angry": 2, "tired": 3}

    m_val = move_map.get(action, 0)
    e_val = emotion_map.get(emotion, 0)

    send_robot_command(m_val, e_val)

def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        # Reduce background noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print(f"User: {text}")
            return text
        except:
            return ""

def main():
    # Initial handshake
    execute_logic("stop", "happy")

    while True:
        user_input = listen_to_mic()
        if not user_input: continue
        if "exit" in user_input.lower(): break

        # --- AI THINKING ---
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_input},
        ])

        try:
            # Parse JSON
            content = response['message']['content']
            clean_json = content.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_json)

            print(f"🤖 CuteBit: {data['response']}")

            # Execute
            execute_logic(data.get('action', 'stop'), data.get('emotion', 'happy'))

            # Simple duration logic for movement
            if data.get('action') != "stop":
                sleep(2)
                execute_logic("stop", data.get('emotion', 'happy'))

        except:
            print("❌ AI Error")

if __name__ == "__main__":
    main()