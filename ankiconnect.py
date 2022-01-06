import sqlite3
import requests


def submit(**kwargs):
    r = requests.post(
        "http://127.0.0.1:8765",
        json={
            "action": "addNote",
            "params": {
                "note": {
                    "deckName": "kindle",
                    "modelName": "Basic",
                    "fields": {"Front": kwargs.get("front"), "Back": kwargs.get("back")},
                }
            },
        },
    )
    print(r.json())


con = sqlite3.connect("dictionary.db")
cur = con.cursor()

for o, t in cur.execute("SELECT original, translated FROM dictionary"):
    submit(front=o,back=t)
