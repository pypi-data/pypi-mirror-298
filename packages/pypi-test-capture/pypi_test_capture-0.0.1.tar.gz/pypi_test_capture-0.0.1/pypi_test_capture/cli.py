from openai import OpenAI
import pyaudio
import typing as tp
from uuid import uuid4

# Settings for audio streaming
FORMAT = pyaudio.paInt16  # Audio format (16-bit per sample)
CHANNELS = 1              # Mono audio
RATE = 44100              # Sample rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
ai = OpenAI()
# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open a stream to record
stream = audio.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

def run_stream() -> tp.Generator[bytes, None, None]:
	"""Generator that yields audio data from the microphone in real-time."""
	print("Streaming microphone input...")
	data: bytes = b''
	try:
		i = 0
		binary_data = b''
		while True:
			# Read data from the microphone stream
			data=stream.read(CHUNK)
			binary_data += data
			if len(binary_data) >= 44100 * 2:
				yield binary_data
				binary_data = b''
			i += 1
			while 1 % 100 == 0:
				yield binary_data
				binary_data = b''
			
	except KeyboardInterrupt:
		print("Stopped streaming.")
	finally:
		# Stop and close the stream
		stream.stop_stream()
		stream.close()
	

def generator_to_file(generator: tp.Generator[bytes, None, None]) -> str:
	"""Write the audio data from the generator to a file."""
	file_id = str(uuid4())
	with open(f"{file_id}.wav", "wb") as f:
		for data in generator:
			f.write(data)
	return file_id

def transcribe_generator(generator: tp.Generator[bytes, None, None]) -> tp.Generator[str, None, None]:
	"""Transcribe the audio data from the generator."""
	for chunk in generator:
		response = ai.audio.transcriptions.create(
			model="whisper-3-large",
			file=chunk,
			response_format="text"
		)
		yield response.text

def main():
	while True:
		for text in transcribe_generator(run_stream()):
			print(text, end="", flush=True)