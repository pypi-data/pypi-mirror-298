# OVOS Wav2Vec2 STT

## Description

OVOS plugin for [Wav2Vec2](https://ai.meta.com/blog/wav2vec-20-learning-the-structure-of-speech-from-raw-audio/)

## Install

`pip install ovos-stt-plugin-wav2vec`

## Configuration

```json
  "stt": {
    "module": "ovos-stt-plugin-wav2vec",
    "ovos-stt-plugin-wav2vec": {
        "model": "proxectonos/Nos_ASR-wav2vec2-large-xlsr-53-gl-with-lm"
    }
  }
```

`"model"` can be any  [compatible wav2vec2](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=likes&search=%2Fwav2vec2) model from hugging face, if not set, it will be automatically selected based on language

### Models

> If your language is not supported you can use `"facebook/mms-1b-all"`, but in that case check out the dedicated plugin [ovos-stt-plugin-mms](https://github.com/OpenVoiceOS/ovos-stt-plugin-mms)

Supported languages: `'ab'`, `'ar'`, `'as'`, `'ba'`, `'bas'`, `'bg'`, `'bn'`, `'br'`, `'ca'`, `'cnh'`, `'cv'`, `'cy'`,
`'cz'`, `'da'`, `'de'`, `'el'`, `'en'`, `'eo'`, `'es'`, `'fa'`, `'fi'`, `'fr'`, `'ga'`, `'gl'`,  `'gn'`, `'ha'`, `'he'`,
`'hi'`, `'hk'`, `'hu'`, `'hy'`, `'ia'`, `'id'`, `'it'`, `'jp'`,  `'jv'`, `'ka'`, `'ko'`, `'ku'`, `'ky'`, `'lb'`, `'lg'`,
`'lt'`, `'ml'`, `'mn'`, `'mr'`, `'mt'`, `'ne'`, `'nl'`, `'or'`, `'pa'`, `'pl'`, `'pt'`, `'rm-sursilv'`, `'rm-vallader'`, 
`'ro'`, `'ru'`, `'sah'`, `'sk'`, `'sl'`, `'su'`, `'sv'`, `'sw'`, `'ta'`, `'te'`, `'tr'`, `'tt'`, `'uk'`, `'ur'`, `'vi'`, `'zh'`


```python
LANG2MODEL = {
    "gl": "proxectonos/Nos_ASR-wav2vec2-large-xlsr-53-gl-with-lm",

    "pt": "jonatasgrosman/wav2vec2-large-xlsr-53-portuguese",
    "en": "jonatasgrosman/wav2vec2-large-xlsr-53-english",
    "zh": "jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn",
    "ru": "jonatasgrosman/wav2vec2-large-xlsr-53-russian",
    "it": "jonatasgrosman/wav2vec2-large-xlsr-53-italian",
    "es": "jonatasgrosman/wav2vec2-large-xlsr-53-spanish",
    "fr": "jonatasgrosman/wav2vec2-large-xlsr-53-french",
    "de": "jonatasgrosman/wav2vec2-large-xlsr-53-german",
    "nl": "jonatasgrosman/wav2vec2-large-xlsr-53-dutch",
    "jp": "jonatasgrosman/wav2vec2-large-xlsr-53-japanese",
    "pl": "jonatasgrosman/wav2vec2-large-xlsr-53-polish",
    "hu": "jonatasgrosman/wav2vec2-large-xlsr-53-hungarian",
    "ar": "jonatasgrosman/wav2vec2-large-xlsr-53-arabic",
    "fi": "jonatasgrosman/wav2vec2-large-xlsr-53-finnish",
    "fa": "jonatasgrosman/wav2vec2-large-xlsr-53-persian",
    "el": "jonatasgrosman/wav2vec2-large-xlsr-53-greek",

    "ia": "infinitejoy/wav2vec2-large-xls-r-300m-interlingua",
    "cnh": "infinitejoy/wav2vec2-large-xls-r-300m-hakha-chin",
    "ta": "infinitejoy/wav2vec2-large-xls-r-300m-tamil-cv8",
    "or": "infinitejoy/wav2vec2-large-xls-r-300m-odia",
    "gn": "infinitejoy/wav2vec2-large-xls-r-300m-guarani",
    "cy": "infinitejoy/wav2vec2-large-xls-r-300m-welsh",
    "ur": "infinitejoy/wav2vec2-large-xls-r-300m-urdu",
    "ab": "infinitejoy/wav2vec2-large-xls-r-300m-abkhaz",
    "ba": "infinitejoy/wav2vec2-large-xls-r-300m-bashkir",
    "bas": "infinitejoy/wav2vec2-large-xls-r-300m-basaa",
    "sah": "infinitejoy/wav2vec2-large-xls-r-300m-sakha",
    "mr": "infinitejoy/wav2vec2-large-xls-r-300m-marathi-cv8",
    "lt": "infinitejoy/wav2vec2-large-xls-r-300m-lithuanian",
    "ha": "infinitejoy/wav2vec2-large-xls-r-300m-hausa",
    "br": "infinitejoy/wav2vec2-large-xls-r-300m-breton",
    "cv": "infinitejoy/wav2vec2-large-xls-r-300m-chuvash",
    "hy": "infinitejoy/wav2vec2-large-xls-r-300m-armenian",
    "mt": "infinitejoy/wav2vec2-large-xls-r-300m-maltese",
    "as": "infinitejoy/wav2vec2-large-xls-r-300m-assamese",
    "tt": "infinitejoy/wav2vec2-large-xls-r-300m-tatar",
    "ky": "infinitejoy/wav2vec2-large-xls-r-300m-kyrgyz",
    "ga": "infinitejoy/wav2vec2-large-xls-r-300m-irish",
    "ka": "infinitejoy/wav2vec2-large-xls-r-300m-georgian",
    "sk": "infinitejoy/wav2vec2-large-xls-r-300m-slovak",
    "sl": "infinitejoy/wav2vec2-large-xls-r-300m-slovenian",
    "mn": "infinitejoy/wav2vec2-large-xls-r-300m-mongolian",
    "ro": "infinitejoy/wav2vec2-large-xls-r-300m-romanian",
    "ku": "infinitejoy/wav2vec2-large-xls-r-300m-kurdish",
    "bg": "infinitejoy/wav2vec2-large-xls-r-300m-bulgarian",
    "hi": "infinitejoy/wav2vec2-large-xls-r-300m-hindi",
    "rm-vallader": "infinitejoy/wav2vec2-large-xls-r-300m-romansh-vallader",
    "rm-sursilv": "infinitejoy/wav2vec2-large-xls-r-300m-romansh-sursilvan",
    # "fi": "infinitejoy/wav2vec2-large-xls-r-300m-finnish",
    # "hu": "infinitejoy/wav2vec2-large-xls-r-300m-hungarian",
    # "el": "infinitejoy/wav2vec2-large-xls-r-300m-greek",
    # "gl": "infinitejoy/wav2vec2-large-xls-r-300m-galician",
    # "ar": "infinitejoy/wav2vec2-large-xls-r-300m-arabic",
    # "id": "infinitejoy/wav2vec2-large-xls-r-300m-indonesian",

    "id": "indonesian-nlp/wav2vec2-large-xlsr-indonesian",
    "lg": "indonesian-nlp/wav2vec2-luganda",
    "jv": "indonesian-nlp/wav2vec2-indonesian-javanese-sundanese",
    "su": "indonesian-nlp/wav2vec2-indonesian-javanese-sundanese",

    "da": "vachonni/wav2vec2-large-xls-r-300m-dansk-CV-80",
    "ml": "Bluecast/wav2vec2-Malayalam",
    "hk": "voidful/wav2vec2-large-xlsr-53-hk",
    "ko": "kresnik/wav2vec2-large-xlsr-korean",
    "vi": "nguyenvulebinh/wav2vec2-base-vietnamese-250h",
    "bn": "arijitx/wav2vec2-large-xlsr-bengali",
    "eo": "cpierse/wav2vec2-large-xlsr-53-esperanto",
    "lb": "Lemswasabi/wav2vec2-large-xlsr-53-842h-luxembourgish-14h-with-lm",
    "te": "anuragshas/wav2vec2-large-xlsr-53-telugu",
    "tr": "mpoyraz/wav2vec2-xls-r-300m-cv7-turkish",
    "ne": "gagan3012/wav2vec2-xlsr-nepali",
    "he": "imvladikon/wav2vec2-large-xlsr-53-hebrew",
    "sv": "KBLab/wav2vec2-large-xlsr-53-swedish",
    "ca": "PereLluis13/wav2vec2-xls-r-1b-ca-lm",
    "cz": "arampacha/wav2vec2-large-xlsr-czech",
    "sw": "alokmatta/wav2vec2-large-xlsr-53-sw",
    "uk": "arampacha/wav2vec2-xls-r-1b-uk",
    "pa": "kingabzpro/wav2vec2-large-xlsr-53-punjabi",
}
```

## Credits

<img src="img.png" width="128"/>

> This plugin was funded by the Ministerio para la Transformación Digital y de la Función Pública and Plan de Recuperación, Transformación y Resiliencia - Funded by EU – NextGenerationEU within the framework of the project ILENIA with reference 2022/TL22/00215337

<img src="img_1.png" width="64"/>

> O [Proxecto Nós](https://github.com/proxectonos) é un proxecto da Xunta de Galicia cuxa execución foi encomendada á Universidade de Santiago de Compostela, a través de dúas entidades punteiras de investigación en intelixencia artificial e tecnoloxías da linguaxe: o ILG (Instituto da Lingua Galega) e o CiTIUS (Centro Singular de Investigación en Tecnoloxías Intelixentes).