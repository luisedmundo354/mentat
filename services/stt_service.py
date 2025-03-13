import numpy as np
import speech_recognition as sr
import whisper
from datetime import datetime, timedelta, timezone
from queue import Queue
import threading
import time

def start_transcription(output_queue: Queue):
    """
    Starts a background thread that continuously records audio, processes it with Whisper,
    and puts the transcribed text into output_queue.
    """
    def transcription_thread():
        data_queue = Queue()

        # Set up the speech recognizer
        recorder = sr.Recognizer()
        recorder.energy_threshold = 1000
        recorder.dynamic_energy_threshold = False

        # Load the Whisper model (using "base.en")
        audio_model = whisper.load_model("base.en")
        record_timeout = 2  # seconds
        phrase_timeout = 3  # seconds
        phrase_time = None

        print("Model loaded...")

        # Define the callback function before using it
        def record_callback(_, audio: sr.AudioData):
            # When recording is finished, put the raw data into the thread-safe queue.
            data = audio.get_raw_data()
            data_queue.put(data)
        
        # Open the microphone using a context manager so its stream stays active.
        with sr.Microphone(sample_rate=16000) as source:
            print("Adjusting for ambient noise...")
            recorder.adjust_for_ambient_noise(source)
            print("Ambient noise adjustment complete.")
            
            # Start background listening. The returned function can be used to stop listening.
            stop_listening = recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
            
            print("Model loaded. Starting transcription...\n")

            # Process audio continuously while the microphone is open.
            while True:
                try:
                    now = datetime.now(timezone.utc)
                    if not data_queue.empty():
                        if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                            # A complete phrase might be ready.
                            # (Your logic here, if needed)
                            pass
                        phrase_time = now

                        # Retrieve and combine all data from the queue safely
                        audio_chunks = []
                        while not data_queue.empty():
                            audio_chunks.append(data_queue.get())
                        audio_data = b''.join(audio_chunks)

                        # Convert byte data to a normalized numpy array (float32)
                        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                        # Transcribe the audio using Whisper
                        result = audio_model.transcribe(audio_np, fp16=False, temperature=0.0)
                        text = result.get('text', '').strip()

                        # Optionally filter out repeated or unwanted phrases
                        if any(sub in text for sub in ['!!!!!', 'a little bit of a little bit of', 
                                                        "I'm sorry.I'm sorry.I'm sorry.", 'Okay. Okay. Okay']):
                            continue

                        # Put the transcription into the output queue
                        output_queue.put(text)
                except Exception as e:
                    print("Error in transcription thread:", e)

    thread = threading.Thread(target=transcription_thread, daemon=True)
    thread.start()

def start_file_transcription(output_queue: Queue, file_path: str):
    """
    Starts a background thread that processes a pre-recorded audio file in chunks,
    transcribes each chunk using Whisper, and puts the transcribed text into output_queue.

    This function simulates live transcription by reading fixed-duration chunks from the file.
    """
    def transcription_thread():
        # Set up the speech recognizer for file processing.
        recorder = sr.Recognizer()
        # Load the Whisper model (using "base.en")
        audio_model = whisper.load_model("base.en")
        record_timeout = 2  # seconds per audio chunk

        print("Model loaded for file transcription...")

        try:
            with sr.AudioFile(file_path) as source:
                # (Optional) Adjust for ambient noise if needed.
                # recorder.adjust_for_ambient_noise(source)

                # Continuously read and transcribe audio chunks until the file is exhausted.
                while True:
                    # Read a chunk of audio from the file.
                    audio_data = recorder.record(source, duration=record_timeout)
                    # If no frames are returned, we have reached the end of the file.
                    if not audio_data.frame_data:
                        break

                    # Convert the audio data to raw bytes.
                    data = audio_data.get_raw_data()

                    # Convert byte data to a normalized numpy array (float32)
                    audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

                    # Transcribe the audio using Whisper
                    result = audio_model.transcribe(audio_np, fp16=False, temperature=0.0)
                    text = result.get('text', '').strip()

                    # Optionally filter out repeated or unwanted phrases.
                    if any(sub in text for sub in ['!!!!!', 'a little bit of a little bit of', 
                                                    "I'm sorry.I'm sorry.I'm sorry.", 'Okay. Okay. Okay']):
                        continue

                    # Put the transcription into the output queue.
                    output_queue.put(text)
                    
                    # Sleep for the duration of the chunk to simulate live transcription.
                    time.sleep(record_timeout)
        except Exception as e:
            print("Error in file transcription thread:", e)
            
    thread = threading.Thread(target=transcription_thread, daemon=True)
    thread.start()