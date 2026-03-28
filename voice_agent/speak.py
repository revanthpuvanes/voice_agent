import os
import uuid
import time
import pyttsx3


def speak_text(text: str, output_dir: str = "outputs/audio") -> str:
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.wav"
    output_path = os.path.abspath(os.path.join(output_dir, filename))

    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

    # Wait briefly for file system flush
    for _ in range(20):
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return output_path
        time.sleep(0.2)

    raise FileNotFoundError(f"TTS audio file was not created correctly: {output_path}")