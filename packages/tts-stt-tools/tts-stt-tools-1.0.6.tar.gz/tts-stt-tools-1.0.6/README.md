# TTS-STT Tools

`tts-stt-tools` is a Python package designed to facilitate seamless **Text-to-Speech (TTS)** and **Speech-to-Text (STT)** conversions. With customizable voice models and simple commands, it offers an easy way to convert text into audio and manage audio-to-text transcriptions.

## Features

- **Text-to-Speech (TTS)**: Convert text into audio using various customizable voice models.
- **Speech-to-Text (STT)**: Transcribe audio files to text using speech recognition models.
- **Voice Model Support**: Choose from a variety of pre-defined voice models for TTS.
- **File Management**: Efficiently manage output files like `.wav` or `.log` for processing and cleanup.

## Installation

Follow these steps to install the `tts-stt-tools` package and its dependencies:

### Step 1: Create and activate a virtual environment

```bash
python3 -m venv testEnv1
source testEnv1/bin/activate
```

### Step 2: Install the package

Inside the virtual environment, install the package:

```bash
pip install --editable .
```

## Usage

The following sections demonstrate how to use both TTS and STT functionalities, including specifying models and handling output files.

### Text-to-Speech (TTS)

Convert text to speech and save it as an audio file using different voice models.

#### Example 1: Using HiFi TTS (Low Quality)

```python
from tts_stt_tools import process_text_to_speech

text = """
Part three

November 10–Present

CHAPTER 14
• Monday, November 10
On Monday morning, Maxine is startled...
"""
process_text_to_speech(text, voice_model='en_US/hifi-tts_low', filename='output1.wav')
```

#### Example 2: Using CMU Arctic (Low Quality)

```python
process_text_to_speech(text, voice_model='en_US/cmu-arctic_low', filename='output2.wav')
```

#### Example 3: Using LJSpeech (Low Quality)

```python
process_text_to_speech(text, voice_model='en_US/ljspeech_low', filename='output3.wav')
```

#### Example 4: Using M-AILABS (Low Quality)

```python
process_text_to_speech(text, voice_model='en_US/m-ailabs_low', filename='output4.wav')
```

#### Example 5: Using VCTK (Low Quality)

```python
process_text_to_speech(text, voice_model='en_US/vctk_low', filename='output5.wav')
```

#### Example 6: Using A-Pope (Low Quality)

```python
process_text_to_speech(text, voice_model='en_UK/apope_low', filename='output6.wav')
```

### Speech-to-Text (STT)

Convert a `.wav` audio file into text using the specified STT model.

#### Example 1: Using Vosk Model

```python
from tts_stt_tools import process_speech_to_text

mp3_path = "output1.wav"
output_directory = ""  # Optional: specify if needed
model_path = "vosk-model-small-en-us-0.15"

result = process_speech_to_text(mp3_path, output_directory, model_path)
print(result)
```

### Running Tests

Unit tests are included to ensure the correct behavior of TTS and STT processes. The tests create `.wav` files for various voice models, verifying that the output files exist after processing.

1. **Setup**: The virtual environment is configured, and dependencies are installed.
2. **Testing**: Each TTS model is validated to ensure audio files are generated.
3. **Cleanup**: Resources like `.wav` files and temporary directories are removed after testing.

To run the tests, simply use:

```bash
pytest
```

The tests will:
- Convert text into speech using different TTS voice models.
- Convert audio files back into text using the Vosk STT model.

### Cleanup After Testing

To clean up resources such as temporary files and directories after the tests, use:

```bash
deactivate
rm -r testEnv1
rm -r *.log *.wav
rm -r vosk-model-*
```

---

This updated documentation reflects the test cases and ensures users have a clear understanding of the TTS-STT workflow with examples.
