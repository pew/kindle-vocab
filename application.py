import sys
import os
import argparse
import sqlite3

parser = argparse.ArgumentParser(description="Translate your Kindle Vocabulary.")
parser.add_argument(
    "-l",
    "--lang",
    required=True,
    type=str,
    help="Language to translate to (DE, EN, FR, etc.)",
)
parser.add_argument(
    "-i",
    "--input",
    type=str,
    default="vocab.db",
    help="Location of your vocab.db file",
)
parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="dictionary.db",
    help="Location of your output dictionary file",
)
parser.add_argument(
    "-e", "--engine", type=str, default="google", help="choose between deepl and google"
)

args = parser.parse_args()

if args.engine.lower() == "deepl":
    import deepl

    translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
    engine = "deepl"

if not args.engine or args.engine.lower() == "google":
    from googletrans import Translator

    translator = Translator()
    engine = "google"

if args.input and not os.path.isfile(args.input):
    print("{} not found".format(args.input))
    sys.exit(1)


def read_words():
    to_translate = []
    if args.input and os.path.isfile(args.input):
        con = sqlite3.connect(args.input)
    else:
        con = sqlite3.connect("vocab.db")
    cur = con.cursor()

    # use GROUP BY to remove duplicates
    for w, l in cur.execute(
        "SELECT LOWER(word), LOWER(lang) FROM words GROUP BY LOWER(word)"
    ):
        # account for en-US, de-DE, only take the first (en, de)
        if "-" in l:
            l = l[:2]
        to_translate.append({"word": w, "lang": l})
    con.close()
    return to_translate


def translate_google(text, source_lang, target_lang="en"):
    result = translator.translate(text, src=source_lang, dest=target_lang)
    return result.text


def translate_deepl(text, source_lang, target_lang="en-US"):
    result = translator.translate_text(
        text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text


if __name__ == "__main__":
    if args.output:
        con = sqlite3.connect(args.output)
    else:
        con = sqlite3.connect("dictionary.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS dictionary (original TEXT, translated TEXT)"
    )

    translated_words = []
    words = read_words()
    for word_pair in words:
        try:
            if engine == "deepl":
                result = translate_deepl(
                    word_pair["word"],
                    source_lang=word_pair["lang"],
                    target_lang=args.lang,
                )
            if engine == "google":
                result = translate_google(
                    word_pair["word"],
                    source_lang=word_pair["lang"],
                    target_lang=args.lang,
                )
        except TypeError:
            pass
        else:
            cur.execute(
                """INSERT INTO dictionary (original, translated) VALUES(?, ?)""",
                (word_pair["word"], result),
            )
            con.commit()
            print("added {} - {}".format(word_pair["word"], result))
