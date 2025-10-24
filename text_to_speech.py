# -*- coding: utf-8 -*-
"""
Handles Text-to-Speech (TTS) functionality using Deepgram's WebSocket API
and PyAudio for audio playback.
"""
import os
import pyaudio
import queue
import threading
import json
import time
import websockets # Import the main library
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError # Import specific exceptions
from websockets.sync.client import connect
from dotenv import load_dotenv
# --- Constants ---
DEFAULT_TOKEN = os.getenv("GOOGLE_API_KEY") # Default Deepgram API token (Consider moving to environment variables or config)
TIMEOUT = 0.050  # Timeout for queue get operation in seconds
FORMAT = pyaudio.paInt16  # Audio format for PyAudio stream
CHANNELS = 1  # Number of audio channels
RATE = 48000  # Sample rate for audio
CHUNK = 8000  # Size of audio chunks for processing and playback
# Example using aura-asteria-en model
DEFAULT_URL = f"wss://api.deepgram.com/v1/speak?encoding=linear16&sample_rate={RATE}&model=aura-asteria-en"
# Default Deepgram WebSocket URL

# --- Global Variables ---
# Note: Extensive use of global variables can make code harder to manage.
# Consider encapsulating this logic within a class for better organization.

audio = None               # PyAudio instance (initialized later)
_queue = queue.Queue()     # Queue to hold audio data chunks for playback
_exit_event = threading.Event() # Event to signal threads to stop gracefully
_socket = None             # WebSocket connection object
_stream = None             # PyAudio output stream object
_playback_thread = None    # Thread for handling audio playback from the queue
_receiver_thread = None    # Thread for receiving audio data from WebSocket

speak_content = True       # Flag to enable/disable speaking (can be toggled)
# llm_processing = None      # Placeholder variable (purpose unclear, removed for now)


# --- Audio Playback Functions ---

def speaker_play_thread():
    """
    Worker thread function that continuously reads audio data from the queue
    and writes it to the PyAudio output stream for playback.
    """
    global _stream # Access global stream object
    print("Playback thread started.")
    while not _exit_event.is_set():
        try:
            # Get audio data from the queue with a timeout
            data = _queue.get(timeout=TIMEOUT)
            if _stream and _stream.is_active(): # Check if stream is valid and active
                _stream.write(data) # Write data to the audio stream
            elif _stream is None or not _stream.is_active():
                 print("Playback thread: Stream is not active or available.")
                 # Optionally break or wait for stream to become active again
                 time.sleep(TIMEOUT) # Wait before checking again
        except queue.Empty:
            # Queue is empty, continue waiting for data
            continue
        except IOError as e:
             print(f"PyAudio stream write error in playback thread: {e}")
             # Decide if the thread should stop on stream errors
             break # Exit thread on stream error
        except Exception as e:
            print(f"Unexpected error in playback thread: {e}")
            # Consider adding more robust error handling or logging
            break # Exit thread on unexpected error
    print("Playback thread finished.")


def speaker_start(rate=RATE, chunk=CHUNK, channels=CHANNELS, output_device_index=None):
    """
    Initializes and starts the PyAudio output stream and the playback thread.

    Args:
        rate (int): Sample rate for the audio stream.
        chunk (int): Buffer size for the audio stream.
        channels (int): Number of audio channels.
        output_device_index (int, optional): Index of the desired output device. Defaults to None (system default).
    """
    global _stream, _playback_thread, audio
    if _stream:
        print("Speaker already started.")
        return

    print("Starting speaker...")
    try:
        if audio is None: # Initialize PyAudio if not already done
             audio = pyaudio.PyAudio()
             print("PyAudio instance created.")

        _stream = audio.open(
            format=FORMAT,
            channels=channels,
            rate=rate,
            input=False,  # This is an output stream
            output=True,
            frames_per_buffer=chunk,
            output_device_index=output_device_index,
        )
        _exit_event.clear() # Reset the exit event
        _playback_thread = threading.Thread(target=speaker_play_thread, daemon=True, name="SpeakerPlaybackThread")
        _playback_thread.start()
        print("Speaker started successfully.")
    except Exception as e:
        print(f"Error starting speaker: {e}")
        if _stream:
             try: _stream.close()
             except: pass
        _stream = None # Ensure stream is None if setup failed

def speaker_stop():
    """
    Stops the playback thread and closes the PyAudio stream gracefully.
    """
    global _stream, _playback_thread
    if not _stream and not (_playback_thread and _playback_thread.is_alive()):
        print("Speaker already stopped or not initialized.")
        return

    print("Stopping speaker...")
    _exit_event.set() # Signal threads to exit

    # Wait for the playback thread to finish
    if _playback_thread and _playback_thread.is_alive():
        _playback_thread.join(timeout=1.0) # Add a timeout to join
        if _playback_thread.is_alive():
             print("Warning: Playback thread did not exit gracefully.")
        _playback_thread = None

    # Close the audio stream
    if _stream:
        try:
            # Check if stream is active before stopping
            if _stream.is_active():
                 _stream.stop_stream()
            _stream.close()
            print("PyAudio output stream closed.")
        except Exception as e:
            print(f"Error closing audio stream: {e}")
        finally:
            _stream = None

    # Clear the queue in case there's leftover data
    speaker_empty_queue()
    print("Speaker stopped.")


def speaker_play(data):
    """
    Adds audio data chunk to the playback queue.

    Args:
        data (bytes): The raw audio data chunk.
    """
    _queue.put(data)

def speaker_empty_queue():
    """
    Clears all items currently in the playback queue.
    """
    cleared_count = 0
    while not _queue.empty():
        try:
            _queue.get_nowait() # Use get_nowait for non-blocking removal
            cleared_count += 1
        except queue.Empty:
            break
        except Exception as e:
            print(f"Error emptying queue: {e}")
            break
    if cleared_count > 0:
        print(f"Speaker queue cleared ({cleared_count} items removed).")


# --- WebSocket Communication Functions ---

def connect_socket(url=DEFAULT_URL, token=DEFAULT_TOKEN):
    """
    Establishes a WebSocket connection to the Deepgram API.

    Args:
        url (str): The WebSocket URL to connect to.
        token (str): The Deepgram API token for authorization.

    Returns:
        bool: True if connection was successful, False otherwise.
    """
    global _socket
    if _socket:
        print("Socket already connected.")
        return True

    print(f"Connecting to WebSocket: {url}")
    try:
        # Use websockets.sync.client.connect
        _socket = connect(url, additional_headers={"Authorization": f"Token {token}"})
        print("WebSocket connected successfully.")
        return True
    except Exception as e:
        print(f"Error connecting to WebSocket: {e}")
        _socket = None # Ensure socket is None if connection failed
        return False

def disconnect_socket():
    """
    Closes the WebSocket connection if it's open.
    """
    global _socket
    if _socket:
        print("Disconnecting WebSocket...")
        try:
            _socket.close()
            print("WebSocket disconnected.")
        except Exception as e:
            print(f"Error disconnecting WebSocket: {e}")
        finally:
            _socket = None

def send_message(prompt):
    """
    Sends text prompt to Deepgram via the WebSocket connection to synthesize speech.

    Args:
        prompt (str): The text to be synthesized into speech.
    """
    global _socket # Access global variables
    if _socket:
        try:
            # Clear any previous state on Deepgram's side (optional but good practice)
            _socket.send(json.dumps({"type": "Clear"}))
            print(f"Sending TTS request: '{prompt[:50]}...'") # Log truncated prompt
            # Send the text to be spoken
            _socket.send(json.dumps({"type": "Speak", "text": prompt}))
            # Flush the connection to ensure the message is sent promptly
            _socket.send(json.dumps({"type": "Flush"}))
        except ConnectionClosedError as e:
             print(f"Error sending message: WebSocket connection closed unexpectedly: {e}")
             disconnect_socket() # Clean up the closed socket reference
        except Exception as e:
            print(f"Error sending message via WebSocket: {e}")
            # Consider attempting to reconnect or handle the error more robustly
    else:
        print("Cannot send message: WebSocket is not connected.")


def receive_audio():
    """
    Worker thread function that listens for incoming messages (audio chunks)
    from the Deepgram WebSocket and puts them into the playback queue.
    """
    global _socket # Access global socket
    print("Audio receiver thread started.")
    speaker_start() # Ensure the speaker is ready before receiving

    try:
        while not _exit_event.is_set():
            if _socket is None:
                print("Receiver thread exiting: WebSocket is not connected.")
                break

            try:
                # Use a timeout for recv to allow checking _exit_event
                message = _socket.recv(timeout=TIMEOUT * 2)

                if message is None: # Handle potential None return on timeout/closure
                    # If recv times out, just continue the loop to check _exit_event
                    continue

                if isinstance(message, str):
                    # Handle text messages (e.g., metadata, errors) from Deepgram
                    try:
                        data = json.loads(message)
                        msg_type = data.get('type')
                        if msg_type == 'Metadata':
                             print(f"Received Metadata: {data}")
                        elif msg_type == 'SpeechEnded':
                             print("Received SpeechEnded signal.")
                        elif msg_type == 'Error':
                             print(f"Received Error from Deepgram: {data.get('description', 'Unknown error')}")
                        else:
                             print(f"Received text message: {message}")
                    except json.JSONDecodeError:
                         print(f"Received non-JSON text message: {message}")
                elif isinstance(message, bytes):
                    # Handle binary audio data
                    speaker_play(message)
                else:
                    print(f"Received unexpected message type: {type(message)}")

            except TimeoutError: # Specific exception for websockets timeout
                 continue # No message received within timeout, continue loop check
            except ConnectionClosedOK:
                 print("WebSocket connection closed normally by server.")
                 break
            except ConnectionClosedError as e:
                 print(f"WebSocket connection closed with error: {e}")
                 break
            except Exception as e:
                # Catch other potential errors during receive
                print(f"Error receiving audio: {e}")
                # Decide if the loop should break based on the error type
                if isinstance(e, (BrokenPipeError, ConnectionResetError)):
                    print("Unrecoverable connection error during receive. Exiting receiver thread.")
                    break # Likely unrecoverable connection issue
                time.sleep(0.1) # Short pause before retrying on other errors

    except Exception as e:
        # Catch errors happening outside the inner receive loop (e.g., during speaker_start)
        print(f"Critical error in receive_audio function: {e}")
    finally:
        print("Audio receiver thread stopping.")
        speaker_stop() # Ensure speaker is stopped when receiver exits
        # Do not disconnect socket here, let shutdown_tts handle it


# --- Main Application Logic ---

def speak(prompt):
    """
    High-level function to make the system speak the given text.
    Clears the audio queue and sends the text to Deepgram for TTS.

    Args:
        prompt (str): The text to speak.
    """
    global speak_content
    if not _socket:
         print("Cannot speak: TTS not initialized or connection lost.")
         # Optionally try to re-initialize here
         # if not initialize_tts(): return # Exit if re-init fails
         return

    if speak_content:
        print("-" * 20)
        print(f"Speak request: '{prompt[:50]}...'")
        speaker_empty_queue()  # Ensure the queue is cleared before starting new audio
        send_message(prompt)
    else:
        print("Speaking is disabled.")

def initialize_tts():
    """
    Connects to the WebSocket and starts the audio receiving thread.

    Returns:
        bool: True if initialization was successful, False otherwise.
    """
    global _receiver_thread, audio
    print("Initializing TTS...")
    if audio is None:
        try:
            audio = pyaudio.PyAudio() # Initialize PyAudio instance here
            print("PyAudio instance created for TTS.")
        except Exception as e:
            print(f"Failed to initialize PyAudio: {e}")
            return False

    if not connect_socket(): # Establish WebSocket connection
        print("Initialization failed: Could not connect to WebSocket.")
        return False

    # Start the audio receiving thread only if the socket connection was successful
    if _socket:
        # Ensure previous thread is cleaned up if re-initializing
        if _receiver_thread and _receiver_thread.is_alive():
             print("Warning: Previous receiver thread still alive during re-initialization.")
             # Attempt to stop it cleanly first
             _exit_event.set()
             _receiver_thread.join(timeout=0.5)

        _exit_event.clear() # Ensure event is clear for the new thread
        _receiver_thread = threading.Thread(target=receive_audio, daemon=True, name="TTSReceiverThread")
        _receiver_thread.start()
        print("TTS initialized successfully.")
        return True
    else:
        # connect_socket already printed the error
        return False


def shutdown_tts():
    """
    Gracefully shuts down the TTS system: stops threads and disconnects.
    """
    global audio
    print("Shutting down TTS system...")
    _exit_event.set() # Signal all threads to stop

    # Wait for the receiver thread to finish
    if _receiver_thread and _receiver_thread.is_alive():
        print("Waiting for receiver thread to finish...")
        _receiver_thread.join(timeout=2.0) # Wait with timeout
        if _receiver_thread.is_alive():
            print("Warning: Receiver thread did not exit gracefully.")
        _receiver_thread = None

    disconnect_socket() # Disconnect WebSocket

    # speaker_stop() should be called by receive_audio's finally block,
    # but call it here again just in case receive_audio failed to start/run
    # or if the playback thread was started independently.
    if _stream or (_playback_thread and _playback_thread.is_alive()):
         speaker_stop()

    # Terminate PyAudio instance
    if audio:
        try:
            audio.terminate()
            print("PyAudio instance terminated.")
            audio = None
        except Exception as e:
             print(f"Error terminating PyAudio: {e}")

    print("TTS system shut down.")


# --- Main Execution ---

if __name__ == "__main__":
    print("Starting TTS example...")

    if initialize_tts():
        try:
            # Example usage
            speak("Hello! This is a test of the text-to-speech system using Deepgram.")
            print("Waiting for audio to finish playing (approx 5 seconds)...")
            time.sleep(5)

            speak("Here is another sentence, testing the queue clearing and subsequent playback.")
            print("Waiting for audio to finish playing (approx 6 seconds)...")
            time.sleep(6)

            print("\nTesting speaking disabled:")
            speak_content = False
            speak("This message should not be spoken.")
            time.sleep(1)
            speak_content = True
            speak("Speaking should now be enabled again.")
            print("Waiting for audio to finish playing (approx 4 seconds)...")
            time.sleep(4)


        except KeyboardInterrupt:
            print("\nKeyboard interrupt received.")
        finally:
            # Gracefully shut down the system
            shutdown_tts()
    else:
        print("TTS initialization failed. Exiting.")

    print("TTS example finished.")
