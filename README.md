# translate kindle vocabulary

Translate your Kindle Vocabulary Builder from the source language into your native language with Google Translate or DeepL.

1. Copy the `vocab.db` file from your Kindle, it's stored in `/Volumes/Kindle/system/vocabulary/vocab.db` if you mount it on a Mac
2. clone this repo and install the packages

```
pip install -U -r requirements.txt
```

## usage

Google Translate should work out of the box, for DeepL you need an API key (they offer a free tier for up to 500k characters per month)

For **DeepL** you need to set the API key as an environment variable `DEEPL_API_KEY`. Like so:

```
export DEEPL_API_KEY=ABC1234
python application.py -e deepl -l de -i vocab.db -o dictionary.db
```

help menu:

```
usage: application.py [-h] -l LANG [-i INPUT] [-o OUTPUT] [-e ENGINE]

Translate your Kindle Vocabulary.

options:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  Language to translate to (DE, EN, FR, etc.)
  -i INPUT, --input INPUT
                        Location of your vocab.db file
  -o OUTPUT, --output OUTPUT
                        Location of your output dictionary file
  -e ENGINE, --engine ENGINE
                        choose between deepl and google
```
