'''
Translator app
'''
#pylint: disable=broad-except

# Import namespaces
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speech_sdk

# Supported languages and correspondings voices
languages = {
    "fr": ["French", "fr-FR-HenriNeural"],
    "es": ["Spanish", "es-ES-ElviraNeural"],
    "hi": ["Hindi", "hi-IN-MadhurNeural"],
    "lt": ["Lithuanian", "lt-LT-OnaNeural"],
    "pt": ["Portuguese", "pt-PT-RaquelNeural"]
}


def main():
    '''Main function'''
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_region)
        translation_config.speech_recognition_language = 'en-US'

        for language in languages:
            translation_config.add_target_language(language)

        print('Ready to translate from',translation_config.speech_recognition_language)

        # Configure speech
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)

        # Get user input
        target_language = ''
        while target_language != 'quit':
            print ("\nEnter a target language")
            for language_item in languages.items():
                print (f" {language_item[0]} = {language_item[1][0]}")
            target_language = input ("\nEnter anything else to stop\n").lower()
            if target_language in translation_config.target_languages:
                get_translate(speech_config, translation_config, target_language)
            else:
                target_language = 'quit'

    except Exception as ex:
        print(ex)


def get_translate(speech_config, translation_config, target_language):
    '''Translate function'''
    translation = ''

    # Translate speech
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config)
    print("Speak now...")
    result = translator.recognize_once_async().get()
    print(f"Translating {result.text}")
    translation = result.translations[target_language]
    print(translation)

    # Synthesize translation
    speech_config.speech_synthesis_voice_name = languages[target_language][1]
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)
        print(speak.error_details)

if __name__ == "__main__":
    main()
