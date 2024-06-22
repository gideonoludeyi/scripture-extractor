import argparse
import os

import google.generativeai as genai
import speech_recognition as sr

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PROMPT = """\
    Listen carefully to the following audio file. List any Bible references explicitly mentioned, in JSON.
    For example:
    [
        {
            "book": "Genesis",
            "chapter": 2,
            "verse": 24
        }
    ]
    If there are no explicitly mentioned Bible references, the JSON should be an empty array.
    """


parser = argparse.ArgumentParser(prog="Scripture Extractor")
parser.add_argument(
    "-f",
    "--file",
    dest="audiofile",
    required=False,
    type=argparse.FileType("rb"),
    default=None,
    help="the audio file from which the scripture references should be extracted. Records audio from microphone if not specified.",
)
parser.add_argument(
    "--api-key",
    dest="api_key",
    required=False,
    type=str,
    default=GOOGLE_API_KEY,
    help="the Google AI Studio API KEY to use for the generative AI request. Defaults to GOOGLE_API_KEY environment variable.",
)


def record_audio_from_microphone(phrase_time_limit=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say Bible verses - you have 10s")
        audio_data = recognizer.listen(source, phrase_time_limit=phrase_time_limit)
        print("Stopped recording")
        return audio_data.get_wav_data()


def main():
    args = parser.parse_args()
    assert (
        args.api_key is not None
    ), "API key required. Either specify the --api-key CLI option or set the GOOGLE_API_KEY environment variable."

    if args.audiofile is not None:
        with args.audiofile as f:
            audio = f.read()
    else:
        audio = record_audio_from_microphone()

    genai.configure(api_key=args.api_key)
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        generation_config=genai.GenerationConfig(response_mime_type="application/json"),
    )
    response = model.generate_content(
        [PROMPT, {"mime_type": "audio/wav", "data": audio}]
    )
    print(response.text)


if __name__ == "__main__":
    main()
