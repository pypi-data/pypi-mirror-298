# ------------------------------------
# Copyright (c) PauloCesar-dev404.
# Licensed under the MIT License.
#
# create ssml using this class
# version: 0.3
# https://learn.microsoft.com/pt-br/azure/ai-services/speech-service/speech-synthesis-markup-structure
# https://learn.microsoft.com/pt-br/azure/ai-services/speech-service/speech-synthesis-markup-voice
#
#
from typing import List, Dict, Optional


class SSMLBuilder:
    def __init__(self, lang: str = "en-US"):
        """
        Inicializa o construtor SSML com idioma padrão e configurações vazias.
        :param lang: Código do idioma para o SSML.
        """
        self.lang = lang
        self.voices: List[Dict[str, str]] = []

    def add_voice(self, name: str, effect: str = "default"):
        """
        Adiciona um novo bloco de voz.
        :param name: Nome da voz.
        :param effect:
        """
        self.voices.append({
            "name": name,
            "effect": effect,
            "elements": []
        })

    def add_voice_element(self, voice_index: int, text: str, volume: Optional[str] = None,
                          rate: Optional[str] = None, pitch: Optional[str] = None, time: Optional[str] = None):
        """
        Adiciona elementos ao bloco de voz especificado.
        :param voice_index: Índice do bloco de voz.
        :param text: Texto a ser incluído.
        :param volume: Volume da fala (opcional).
        :param rate: Taxa da fala (opcional).
        :param pitch: Tom da fala (opcional).
        :param time: Tempo de pausa (opcional).
        """
        if voice_index >= len(self.voices):
            raise IndexError("Índice de voz fora do intervalo")

        prosody_attributes = []
        if volume:
            prosody_attributes.append(f'volume="{volume}"')
        if rate:
            prosody_attributes.append(f'rate="{rate}"')
        if pitch:
            prosody_attributes.append(f'pitch="{pitch}"')

        prosody_tag = f'<prosody {" ".join(prosody_attributes)}>' if prosody_attributes else ''
        prosody_end_tag = '</prosody>' if prosody_attributes else ''

        text_with_pause = text
        if time:
            text_with_pause = f'<break time="{time}"/> {text_with_pause}'

        self.voices[voice_index]["elements"].append(f"{prosody_tag}{text_with_pause}{prosody_end_tag}")

    def add_silence(self, voice_index: int, silence_type: str, value: str):
        """
        Adiciona um elemento de silêncio ao bloco de voz.
        :param voice_index: Índice do bloco de voz.
        :param silence_type: Tipo de silêncio.
        :param value: Duração do silêncio.
        """
        if voice_index >= len(self.voices):
            raise IndexError("Índice de voz fora do intervalo")
        silence_element = f'<mstts:silence type="{silence_type}" value="{value}"/>'
        self.voices[voice_index]["elements"].append(silence_element)

    def add_emphasis(self, voice_index: int, text: str, level: str = "moderate"):
        """
        Adiciona ênfase ao texto.
        :param voice_index: Índice do bloco de voz.
        :param text: Texto a ser enfatizado.
        :param level: Nível de ênfase.
        """
        self.voices[voice_index]["elements"].append(f'<emphasis level="{level}">{text}</emphasis>')

    def add_phoneme(self, voice_index: int, text: str, alphabet: str, ph: str):
        """
        Adiciona um fonema ao bloco de voz.
        :param voice_index: Índice do bloco de voz.
        :param text: Texto correspondente.
        :param alphabet: Alfabeto usado.
        :param ph: Representação fonética.
        """
        self.voices[voice_index]["elements"].append(f'<phoneme alphabet="{alphabet}" ph="{ph}">{text}</phoneme>')

    def add_say_as(self, voice_index: int, text: str, interpret_as: str, format_adtional: Optional[str] = None):
        """
        Adiciona um elemento <say-as> ao bloco de voz.
        :param voice_index: Índice do bloco de voz.
        :param text: Texto a ser interpretado.
        :param interpret_as: Como o texto deve ser interpretado.
        :param format_adtional: Formato opcional para o texto.
        """
        format_attr = f' format="{format_adtional}"' if format_adtional else ''
        (self.voices[voice_index]["elements"].
         append(f'<say-as interpret-as="{interpret_as}"{format_attr}>{text}</say-as>'))

    def add_express_as(self, voice_index: int,
                       style: str,
                       styledegree: Optional[str] = None,
                       role: Optional[str] = None):
        """
        Adiciona um elemento <mstts:express-as> ao bloco de voz.
        :param voice_index: Índice do bloco de voz.
        :param style: Estilo de expressão.
        :param styledegree: Grau do estilo (opcional).
        :param role: Papel (opcional).
        """
        express_attributes = [f'style="{style}"']
        if styledegree:
            express_attributes.append(f'styledegree="{styledegree}"')
        if role:
            express_attributes.append(f'role="{role}"')
        (self.voices[voice_index]["elements"]
         .append(f'<mstts:express-as {" ".join(express_attributes)}></mstts:express-as>'))

    def add_audio(self,
                  voice_index: int,
                  src: str,
                  fallback_text: Optional[str] = None,
                  inner_elements: Optional[List[str]] = None):
        """
        Adiciona o elemento <audio> ao bloco de voz.
        :param voice_index: Índice do bloco de voz.
        :param src: Caminho ou URL do áudio.
        :param fallback_text: Texto de fallback.
        :param inner_elements: Elementos internos SSML.
        """
        inner_content = " ".join(inner_elements) if inner_elements else ""
        audio_element = (f'<audio src="{src}">'
                         f'{fallback_text} {inner_content}</audio>')\
            if fallback_text else f'<audio src="{src}">{inner_content}</audio>'
        self.voices[voice_index]["elements"].append(audio_element)

    def build(self) -> str:
        """
        Constrói e retorna o SSML completo.
        """
        voices_tags = '\n'.join(
            '<voice name="{name}" effect="{effect}">{elements}</voice>'.format(
                name=voice["name"],
                effect=voice["effect"],
                elements='\n'.join(voice["elements"])
            )
            for voice in self.voices
        )

        return """
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
            xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{lang}">
            {voices_tags}
        </speak>
        """.format(
            lang=self.lang,
            voices_tags=voices_tags
        )
