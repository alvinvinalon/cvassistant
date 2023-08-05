import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig, SpeechSynthesisOutputFormat
from xml.etree import ElementTree as ET

def speak_text(text, speaker, action, style=None):
    speech_config = SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = speaker

    file_name = "outputaudio.mp3"
    file_config = AudioConfig(filename=file_name)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Prepare SSML
    if style:
        ssml = ET.Element("speak", version="1.0")
        ssml.set("xmlns", "http://www.w3.org/2001/10/synthesis")
        ssml.set("xmlns:mstts", "https://www.w3.org/2001/mstts")
        ssml.set("xml:lang", "en-US")
        voice_tag = ET.SubElement(ssml, "voice", name=speaker)
        express_as_tag = ET.SubElement(voice_tag, "mstts:express-as", style=style, styledegree=str(1))
        express_as_tag.text = text
        ssml_text = ET.tostring(ssml, encoding="unicode")
    else:
        ssml_text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US"><voice name="{speaker}">{text}</voice></speak>'

    #print(ssml_text)
    if action == "speak":
        result = synthesizer.speak_ssml_async(ssml_text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with open("outputaudio.mp3", "rb") as f:
                audio_data = f.read()
            print("Speech synthesized")
            return audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("Speech synthesis canceled")
    elif action == "stop":
        synthesizer.stop_speaking()

# Mapping of charaters to voice styles
def get_speaker_voice(character):
    # Set the Speech Speaker based on the character
    speech_speaker = "en-US-JennyNeural"
    if character == "Adam Sandler":
        speech_speaker = "en-US-DavisNeural"                
    elif character == "Eminem":
        speech_speaker = "en-US-DavisNeural"                
    elif character == "Shakespeare":
        speech_speaker = "en-US-DavisNeural"                
    elif character == "Snoop Dogg":
        speech_speaker = "en-US-DavisNeural"                
    elif character == "Spock":
        speech_speaker = "en-US-TonyNeural"                
    elif character == "Yoda":
        speech_speaker = "en-US-ChristopherNeural"
    
    return speech_speaker