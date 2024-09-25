class VoiceParser:
    def __init__(self, voice: dict):
        self.__voice = voice

    @property
    def status(self):
        """ststaus voice"""
        return self.__voice.get('Status', '')

    @property
    def voice_type(self):
        return self.__voice.get('VoiceType', '')

    @property
    def sample_rate_hertz(self):
        return self.__voice.get('SampleRateHertz', 0)

    @property
    def locale_name(self):
        return self.__voice.get('LocaleName', '')

    @property
    def gender(self):
        return self.__voice.get('Gender', '')

    @property
    def short_name(self):
        return self.__voice.get('ShortName', '')

    @property
    def display_name(self):
        return self.__voice.get('DisplayName', '')

    @property
    def name(self):
        return self.__voice.get('Name', '')

    @property
    def words_per_minute(self):
        """palavras por minuto"""
        return self.__voice.get('WordsPerMinute', 0)

    @property
    def style_list(self):
        return self.__voice.get('StyleList', [])

    @property
    def get_output_format(self):
        """Obtém o formato de áudio baseado em SampleRateHertz"""
        sample_rate_hertz = int(self.sample_rate_hertz)

        if sample_rate_hertz == 8000:
            return 'riff-8khz-8bit-mono-mulaw'
        elif sample_rate_hertz == 16000:
            return 'riff-16khz-16bit-mono-pcm, audio-16khz-128kbitrate-mono-mp3'
        elif sample_rate_hertz == 24000:
            return 'riff-24khz-16bit-mono-pcm, audio-24khz-96kbitrate-mono-mp3'
        elif sample_rate_hertz == 48000:
            return 'riff-48khz-16bit-mono-pcm, audio-48khz-192kbitrate-mono-mp3'
        else:
            raise ValueError("Taxa de amostragem não suportada ou inválida")


class Voices:
    def __init__(self, voices: list[dict]):
        self.__voices = voices

    def filter_voices_by_locale_name(self, locale_name):
        """
        Filtra a lista de vozes baseadas no nome da localidade (LocaleName).

        Args:

            locale_name (str): Nome da localidade para filtrar.

        Returns:
            list: Lista de vozes que correspondem ao nome da localidade.
        """
        filtered_voices = [voice for voice in self.__voices if voice['LocaleName'] == locale_name]
        return filtered_voices

    def filter_voices_by_voice_name(self, short_name) -> VoiceParser:
        """
        Filtra a lista de vozes baseadas no nome da voz (VoiceName).

        Args:
            short_name (str): Nome da voz para filtrar.

        Returns:
            list: Lista de vozes que correspondem ao nome da voz.
        """
        for voice in self.__voices:
            if voice['ShortName'].lower() == short_name.lower():
                vc = VoiceParser(voice)
                return vc

    def get_all_local_voices(self):
        """
        Retorna todos os nomes de localidades (LocaleName) das vozes disponíveis em ordem alfabética.
        Returns:
            list: Lista ordenada em ordem alfabética com nomes únicos das localidades das vozes.
        """

        locale_names = {voice['LocaleName'] for voice in self.__voices}
        return sorted(locale_names)

    def get_all_multilingual(self):
        """Obtém as vozes multilíngues como dicionários"""
        # Filtra as vozes onde 'LocalName' contém a string 'Multilingual'
        voices_multilingual = [
            voice for voice in self.__voices
            if 'Multilingual' in voice.get('LocalName', '')
        ]
        # Ordena as vozes multilíngues por 'LocalName'
        return sorted(voices_multilingual, key=lambda v: v.get('LocalName', ''))

