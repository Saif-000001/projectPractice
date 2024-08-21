from TTS.api import TTS

def text_to_audio(text, lang):
    lang_to_model = {       
        'en': 'tts_models/en/ljspeech/fast_pitch',
        'fr': 'tts_models/fr/mai/tacotron2-DDC',
        'de': 'tts_models/de/thorsten/tacotron2-DDC',
        'es': 'tts_models/es/mai/tacotron2-DDC',
        'it': 'tts_models/it/mai_female/glow-tts',
        'nl': 'tts_models/nl/mai/tacotron2-DDC',
        'pt': 'tts_models/pt/cv/vits',
        'pl': 'tts_models/pl/mai_female/vits',
        'tr': 'tts_models/tr/common-voice/glow-tts',
        'ja': 'tts_models/ja/kokoro/tacotron2-DDC',
        'zh-cn': 'tts_models/zh-CN/baker/tacotron2-DDC-GST',
        'bn': 'tts_models/bn/custom/vits-male',  # Updated Bengali model
        'bg': 'tts_models/bg/cv/vits',
        'cs': 'tts_models/cs/cv/vits',
        'da': 'tts_models/da/cv/vits',
        'et': 'tts_models/et/cv/vits',
        'ga': 'tts_models/ga/cv/vits',
        'el': 'tts_models/el/cv/vits',
        'fi': 'tts_models/fi/css10/vits',
        'hr': 'tts_models/hr/cv/vits',
        'hu': 'tts_models/hu/css10/vits',
        'lt': 'tts_models/lt/cv/vits',
        'lv': 'tts_models/lv/cv/vits',
        'mt': 'tts_models/mt/cv/vits',
        'ro': 'tts_models/ro/cv/vits',
        'sk': 'tts_models/sk/cv/vits',
        'sl': 'tts_models/sl/cv/vits',
        'sv': 'tts_models/sv/cv/vits',
        'uk': 'tts_models/uk/mai/vits',
        'ca': 'tts_models/ca/custom/vits',
        'fa': 'tts_models/fa/custom/glow-tts',
        'be': 'tts_models/be/common-voice/glow-tts'
    }
    
    model_name = lang_to_model.get(lang, 'tts_models/multilingual/multi-dataset/your_tts')
    
    try:
        tts = TTS(model_name=model_name)
        output_file = f"Audio_{lang}.wav"
        tts.tts_to_file(text=text, file_path=output_file)
        print(f"Audio file created: {output_file}")
        return output_file
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
# bengali_text = "বাংলা বই এর বিশাল সংগ্রহশালায় আপনাকে স্বাগতম। কর্মব্যস্ত জীবনে সাহিত্যরস খুঁজে পেতে বই"

japani_text = "あなたはベンガル語の本の膨大なコレクションの中にいます。忙しい芸術文学を見つけるための本"

p = text_to_audio(japani_text, 'ja')
if p:
    print(f"Output file: {p}")
else:
    print("Failed to create audio file")