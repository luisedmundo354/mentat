# transcription.py
import numpy as np
import speech_recognition as sr
import whisper
from datetime import datetime, timedelta
from queue import Queue
import threading

def start_transcription(output_queue: Queue):
    """
    Starts a background thread that continuously records audio, processes it with Whisper,
    and puts the transcribed text into output_queue.
    """
    def transcription_thread():
        phrase_time = None
        data_queue = Queue()

        # Set up the speech recognizer
        recorder = sr.Recognizer()
        recorder.energy_threshold = 1000
        recorder.dynamic_energy_threshold = False

        # Load the Whisper model (using "base.en")
        audio_model = whisper.load_model("base.en")

        record_timeout = 2
        phrase_timeout = 3
        print("Model loaded...")

        # Open the microphone using a context manager so its stream is active.
        with sr.Microphone(sample_rate=16000) as source:
            print("Adjusting for ambient noise...")
            recorder.adjust_for_ambient_noise(source)
            print("Ambient noise adjustment complete.")

            # Now the microphone stream is open, you can start background listening.
            recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)


        def record_callback(_, audio: sr.AudioData):
            # When recording is finished, put the raw data into the thread-safe queue.
            data = audio.get_raw_data()
            data_queue.put(data)

        # Start listening in the background (this returns immediately)
        recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
        print("Model loaded. Starting transcription...\n")

        while True:
            try:
                now = datetime.datetime.now(datetime.timezone.utc)
                if not data_queue.empty():
                    # Optionally check for phrase completion based on timeout
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        # A complete phrase might be ready
                        pass
                    phrase_time = now

                    # Combine all audio data from the queue
                    audio_data = b''.join(data_queue.queue)
                    data_queue.queue.clear()

                    # Convert byte data to numpy float32 array (normalized)
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    # Transcribe the audio
                    result = audio_model.transcribe(audio_np, fp16=False, temperature=0.0)
                    text = result.get('text', '').strip()

                    # Filter out unwanted repeated phrases if needed
                    if any(sub in text for sub in ['!!!!!', 'a little bit of a little bit of', 
                                                    "I'm sorry.I'm sorry.I'm sorry.", 'Okay. Okay. Okay']):
                        continue

                    # Put the transcription text into the output queue
                    output_queue.put(text)
            except Exception as e:
                print("Error in transcription thread:", e)

    thread = threading.Thread(target=transcription_thread, daemon=True)
    thread.start()