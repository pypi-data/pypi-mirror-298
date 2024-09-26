from gtts import gTTS
from gtts.lang import tts_langs
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils.log import LOG

# Live list of languages
# Cached list of supported languages (2021-02-09)
_default_langs = {'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic',
                  'hy': 'Armenian', 'bn': 'Bengali', 'bs': 'Bosnian',
                  'ca': 'Catalan', 'hr': 'Croatian', 'cs': 'Czech',
                  'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
                  'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino',
                  'fi': 'Finnish', 'fr': 'French', 'de': 'German',
                  'el': 'Greek', 'gu': 'Gujarati', 'hi': 'Hindi',
                  'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian',
                  'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese',
                  'kn': 'Kannada', 'km': 'Khmer', 'ko': 'Korean',
                  'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian',
                  'ml': 'Malayalam', 'mr': 'Marathi',
                  'my': 'Myanmar (Burmese)', 'ne': 'Nepali',
                  'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
                  'ro': 'Romanian', 'ru': 'Russian', 'sr': 'Serbian',
                  'si': 'Sinhala', 'sk': 'Slovak', 'es': 'Spanish',
                  'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
                  'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish',
                  'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
                  'cy': 'Welsh', 'zh': 'Chinese (Mandarin/China)'
                  }

_supported_langs = None


def get_supported_langs():
    """Get dict of supported languages.

    Tries to fetch remote list, if that fails a local cache will be used.

    Returns:
        (dict): Lang code to lang name map.
    """
    global _supported_langs
    if not _supported_langs:
        try:
            _supported_langs = tts_langs()
        except Exception:
            LOG.warning('Couldn\'t fetch upto date language codes')
    return _supported_langs or _default_langs


class GoogleTranslateTTS(TTS):
    def __init__(self, *args, **kwargs):
        self._google_lang = None
        super().__init__(*args, **kwargs, audio_ext="mp3",
                         validator=GoogleTTSValidator(self))

    @property
    def google_lang(self):
        """Property containing a converted language code suitable for gTTS."""
        supported_langs = get_supported_langs()
        if not self._google_lang:
            if self.lang.lower() in supported_langs:
                self._google_lang = self.lang.lower()
            elif self.lang[:2].lower() in supported_langs:
                self._google_lang = self.lang[:2]
        return self._google_lang or self.lang.lower()

    def get_tts(self, sentence, wav_file, lang=None):
        """Fetch tts audio using gTTS.

        Args:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        if lang:
            supported_langs = get_supported_langs()
            if lang not in supported_langs:
                if lang.split('-')[0] in supported_langs:
                    lang = lang.split('-')[0]
                else:
                    lang = self.google_lang
        else:
            lang = self.google_lang
        tts = gTTS(text=sentence, lang=lang)
        tts.save(wav_file)
        return (wav_file, None)  # No phonemes


class GoogleTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(GoogleTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.google_lang
        if lang.lower() not in get_supported_langs():
            raise ValueError("Language not supported by gTTS: {}".format(lang))

    def validate_connection(self):
        try:
            gTTS(text='Hi').save(self.tts.filename)
        except Exception:
            raise Exception(
                'GoogleTTS server could not be verified. Please check your '
                'internet connection.')

    def get_tts_class(self):
        return GoogleTranslateTTS

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(get_supported_langs())


lang2gender = {"en": "female"}  # TODO add gender per lang
GoogleTranslateTTSPluginConfig = {
    lang: [{"lang": lang,
            "meta": {
                "gender": lang2gender.get(lang, ""),
                "priority": 55,
                "display_name": f"Google Translate ({lang})",
                "offline": False}
            }]
    for lang in get_supported_langs()}

if __name__ == "__main__":
    print(GoogleTranslateTTSPluginConfig)
    e = GoogleTranslateTTS()

    ssml = """Hello world"""
    e.get_tts(ssml, "gtts.mp3")
