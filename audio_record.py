import pyaudio
import numpy as np
import soundfile as sf
import os
from threading import Timer
from openai import OpenAI

# OpenAI authentication
client = OpenAI(api_key='**********OPENAI_API_KEY**********')  

def record_audio_fixed_duration(duration=5, output_filename='audio_sample.wav'):
    """
    Records audio for a specified duration and saves it as a WAV file.

    This function initializes the PyAudio stream, records audio in chunks for the
    specified duration, and then saves the recorded audio to a specified file. The
    audio is recorded in mono channel with a sample rate of 16 kHz and 16-bit format.

    Parameters:
    duration (int): The duration of the recording in seconds. Default is 5 seconds.
    output_filename (str): The name of the WAV file where the recording will be saved.
                           Default is 'audio_sample.wav'.

    Returns:
    str: The filename of the saved audio if recording was successful, otherwise None.
    """
    FORMAT = pyaudio.paInt16  # Audio format (16 bits)
    CHANNELS = 1              # Number of channels (mono)
    RATE = 16000              # Sample rate (16 kHz)
    CHUNK = 1024              # Buffer size

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open the audio stream
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    def stop_recording():
        nonlocal recording
        recording = False
        print("Stopping recording...")

    recording = True
    frames = []

    print("Recording...")

    # Schedule the recording to stop after 'duration' seconds
    t = Timer(duration, stop_recording)
    t.start()

    while recording:
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))

    t.join()  # Wait for the timer to finish

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert frames to a numpy array
    audio_data = np.hstack(frames)

    # Save the audio to a temporary WAV file
    sf.write(output_filename, audio_data, RATE)

    # Verify that the file was saved correctly
    if os.path.exists(output_filename):
        print(f"Audio file saved as {output_filename}")
    else:
        print("Error saving audio file")
        return None

    return output_filename

def create_transcription(audio_file):
    """
    Creates a transcription of an audio file using OpenAI Whisper.

    This function opens the specified audio file, sends it to the OpenAI API for
    transcription, and returns the response containing the transcription text.

    Parameters:
    audio_file (str): The name of the WAV audio file to be transcribed.

    Returns:
    dict: The response from the OpenAI API with the transcription of the audio.
    """
    with open(audio_file, "rb") as file:
        # Create transcription using OpenAI Whisper
        whisper_prompt = """You are an assistant whose task is to help the user programming in Python. 
        You will get an audio message in English. The output should be a transcription of the audio message also in English.
        """
        response = client.audio.transcriptions.create(model="whisper-1", file=file, prompt=whisper_prompt)
    return response

def audio_input():
    """
    Main function to record audio and create its transcription.

    This function coordinates the recording of audio for a fixed duration and
    then creates a transcription of the recorded audio using OpenAI Whisper.
    It first calls the `record_audio_fixed_duration` function to record the audio
    and save it as a WAV file. If the recording is successful, it then calls
    `create_transcription` to obtain the transcription of the recorded audio
    and prints the transcription result.
    """
    output_filename = record_audio_fixed_duration()
    if output_filename:
        transcription_response = create_transcription(output_filename)
        return transcription_response.text

