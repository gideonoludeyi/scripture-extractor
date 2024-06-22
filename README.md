# Scripture Extractor
Extracts scripture references from audio.

## Getting Started
### Activate environment
##### macOS and Linux
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
```
##### Windows
```sh
$ python -m venv .venv
$ .venv\Scripts\activate
```
### Install dependencies
```sh
(.venv) $ pip install -r requirements.txt
```
### Extract from live audio recording
```sh
(.venv) $ python main.py --api-key=<GOOGLE_API_KEY>
```
### Extract from audio file
```sh
(.venv) $ python main.py --api-key=<GOOGLE_API_KEY> --file /path/to/audio
```
### CLI Help
```sh
$ python main.py --help
```
