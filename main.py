import ollama
import json
import speech_recognition as sr
from cvzone.SerialModule import SerialObject
from time import sleep
from tts import talk

# --- HARDWARE SETUP ---

car = SerialObject("COM11", 115200, digits=2) # Note: digits=2 for [move, emotion]


# --- SYSTEM PROMPT ---
# This tells the AI who it is and how to control the body.
SYSTEM_PROMPT = """
You are CuteBit, a helpful and expressive robot assistant. 
You control a physical body with motors and a face.
You MUST reply in valid JSON format ONLY. 
Do not write normal text outside the JSON.

The JSON format is:
{
    "response": "Your verbal reply to the user here.",
    "action": "move_command",
    "emotion": "emotion_command"
}

Available "action" values: "stop", "forward", "backward", "left", "right"
Available "emotion" values: "happy", "angry", "default", "tired"

Example: If user says "Come here!", you reply:
{"response": "Coming to you!", "action": "forward", "emotion": "happy"}
"""

def execute_robot_command(action, emotion):
    # Map text commands to your Arduino numbers
    move_map = {"stop": 0, "forward": 1, "right": 2, "left": 3, "backward": 4}
    emotion_map = {"happy": 0, "angry": 1, "default": 2, "tired": 3}

    m_val = move_map.get(action, 0)
    e_val = emotion_map.get(emotion, 0)
    pack = [int(m_val), int(e_val)]
    print(f"🤖 ACTING: Move={action} ({m_val}), Face={emotion} ({e_val})")
    car.sendData(pack)
    print("Sent")

def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"User said: {text}")
        return text
    except:
        return ""

def main():
    sleep(1)
    talk("Hi. Cute Bit is awake!")
    print("CuteBit is awake!")

    # Send initial 'Stop' and 'Happy'
    execute_robot_command("stop", "happy")

    while True:
        user_input = listen_to_mic()

        if not user_input:
            continue

        if "exit" in user_input.lower():
            break

        # --- THINKING (Ollama) ---
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_input},
        ])

        ai_content = response['message']['content']

        # --- PARSING & ACTING ---
        try:
            # Clean up potential markdown formatting from LLM
            clean_json = ai_content.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_json)

            talk(data['response'])
            print(f"CuteBit: {data['response']}")

            # 2. Move & Emote
            execute_robot_command(data.get('action', 'stop'), data.get('emotion', 'happy'))

            # 3. Simple logic to stop after moving (so it doesn't crash)
            if data.get('action') in ["forward", "backward", "left", "right"]:
                sleep(3) # Move for 3 seconds
                execute_robot_command("stop", data.get('emotion', 'happy'))

        except json.JSONDecodeError:
            print("Error: AI didn't output valid JSON.")
            print("Raw output:", ai_content)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCaught KeyboardInterrupt")
        exit()