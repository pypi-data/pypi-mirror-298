# OVOS MMS STT

OVOS plugin for [The Massively Multilingual Speech (MMS) project](https://huggingface.co/docs/transformers/main/en/model_doc/mms)

## Description

> Expanding the language coverage of speech technology has the potential to improve access to information for many more people. However, current speech technology is restricted to about one hundred languages which is a small fraction of the over 7,000 languages spoken around the world. The Massively Multilingual Speech (MMS) project increases the number of supported languages by 10-40x, depending on the task. The main ingredients are a new dataset based on readings of publicly available religious texts and effectively leveraging self-supervised learning. We built pre-trained wav2vec 2.0 models covering 1,406 languages, a single multilingual automatic speech recognition model for 1,107 languages, speech synthesis models for the same number of languages, as well as a language identification model for 4,017 languages. Experiments show that our multilingual speech recognition model more than halves the word error rate of Whisper on 54 languages of the FLEURS benchmark while being trained on a small fraction of the labeled data.

The equivalent TTS models can be used via [ovos-tts-plugin-coqui](https://github.com/OpenVoiceOS/ovos-tts-plugin-coqui) fairseq models

## Install

`pip install ovos-stt-plugin-mms`

## Configuration

```json
"stt": {
    "module": "ovos-stt-plugin-mms",
    "ovos-stt-plugin-mms": {
      "model": "facebook/mms-1b-all"
    }
}
```

valid models: `facebook/mms-1b-all`, `facebook/mms-1b-l1107`, `facebook/mms-1b-fl102`


## Credits

<img src="img.png" width="128"/>

> This plugin was funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with reference 2022/TL22/00215337
