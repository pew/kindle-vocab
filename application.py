import sys
import os
import argparse
import sqlite3

from googletrans import Translator

parser = argparse.ArgumentParser(description="Translate your Kindle Vocabulary.")
parser.add_argument(
    "-l",
    "--lang",
    required=True,
    type=str,
    help="Language to translate to (DE, EN, FR, etc.)",
)
parser.add_argument(
    "-f",
    "--file",
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

args = parser.parse_args()

if args.file and not os.path.isfile(args.file):
    print("{} not found".format(args.file))
    sys.exit(1)

translator = Translator()


def read_words():
    to_translate = []
    if args.file and os.path.isfile(args.file):
        con = sqlite3.connect(args.file)
    else:
        con = sqlite3.connect("vocab.db")
    cur = con.cursor()

    # use GROUP BY to remove duplicates
    for w, l in cur.execute("SELECT word, lang FROM words GROUP BY word"):
        # account for en-US, de-DE, only take the first (en, de)
        if "-" in l:
            l = l[:2]
        to_translate.append({"word": w.lower(), "lang": l.lower()})
    con.close()
    return to_translate


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
            result = translator.translate(
                word_pair["word"], src=word_pair["lang"], dest=args.lang
            )
        except TypeError:
            pass
        else:
            cur.execute(
                """INSERT INTO dictionary (original, translated) VALUES(?, ?)""",
                (word_pair["word"], result.text),
            )
            con.commit()
            print("added {}".format(word_pair["word"]))
