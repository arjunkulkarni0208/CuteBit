from faster_whisper import WhisperModel
import speech_recognition as sr

# 1. Load Model onto GPU (Run this ONCE at top of code)
# 'tiny.en' is instant. 'base.en' is very accurate.
print("Loading Whisper Model...")
model = WhisperModel("base.en", device="cuda", compute_type="float16")
print("✅ Whisper Loaded on GPU")

def listen_fast():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        # FAST SETTINGS:
        r.energy_threshold = 300  # Adjust based on mic sensitivity
        r.pause_threshold = 0.6   # Stop listening after 0.6 s of silence (Default is 0.8)
        r.dynamic_energy_threshold = False # Faster if you manually set a threshold

        try:
            # limited timeout prevents hanging
            audio = r.listen(source, timeout=5, phrase_time_limit=4)

            # Save to a temporary file (Whisper needs a file or byte stream)
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Transcribe locally on GPU
            segments, info = model.transcribe("temp.wav", beam_size=5)
            text = " ".join([segment.text for segment in segments])

            print(f"User: {text}")
            return text
        except Exception as e:
            print(e)
            return ""