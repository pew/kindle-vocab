# translate kindle vocabulary

Translate your Kindle Vocabulary Builder from the source language into your native language with Google Translate.

1. Copy the `vocab.db` file from your Kindle, it's stored in `/Volumes/Kindle/system/vocabulary/vocab.db` if you mount it on a Mac
2. clone and install the python packages (google translate) from this repo:

```
pip install -U -r requirements.txt
```

## usage

```
usage: application.py [-h] -l LANG [-f FILE] [-o OUTPUT]

Translate your Kindle Vocabulary.

options:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  Language to translate to (DE, EN, FR, etc.)
  -f FILE, --file FILE  Location of your vocab.db file
  -o OUTPUT, --output OUTPUT
                        Location of your output dictionary file
```
