# ailia AI Speech Python API

!! CAUTION !!
“ailia” IS NOT OPEN SOURCE SOFTWARE (OSS).
As long as user complies with the conditions stated in [License Document](https://ailia.ai/license/), user may use the Software for free of charge, but the Software is basically paid software.

## About ailia AI Speech

ailia Speech is a library to perform speech recognition using AI. It provides a C API for native applications, as well as a C# API well suited for Unity applications. Using ailia Speech, you can easily integrate AI powered speech recognition into your applications.

## Install from pip

You can install the ailia SDK free evaluation package with the following command.

```
pip3 install ailia_speech
```

## Install from package

You can install the ailia SDK from Package with the following command.

```
python3 bootstrap.py
pip3 install ./
```

## Usage

```python
import ailia
import ailia_speech

import librosa

import os
import urllib.request

# Load target audio
ref_file_path = "demo.wav"
if not os.path.exists(ref_file_path):
	urllib.request.urlretrieve(
		"https://github.com/axinc-ai/ailia-models/raw/refs/heads/master/audio_processing/whisper/demo.wa",
		"demo.wav"
	)
audio_waveform, sampling_rate = librosa.load(ref_file_path, mono=True)

# Infer
speech = ailia_speech.Whisper()
speech.initialize_model(model_path = "./models/", model_type = ailia_speech.AILIA_SPEECH_MODEL_TYPE_WHISPER_MULTILINGUAL_SMALL)
recognized_text = speech.transcribe(audio_waveform, sampling_rate)
print(recognized_text)
```

## API specification

https://github.com/axinc-ai/ailia-sdk

