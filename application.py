import sqlite3
from googletrans import Translator

translator = Translator()


def read_words():
    to_translate = []
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
                word_pair["word"], src=word_pair["lang"], dest="de"
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
