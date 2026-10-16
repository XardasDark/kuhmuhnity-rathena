#!/usr/bin/env python3
"""
KuhMuhWeide – erzeugt db/import/item_randomopt_group.yml aus affixe.csv

Aufruf (Windows):   py tools\\kuhmuhnity\\gen_gruppen.py <kapitel>      z. B.  ... 1
Aufruf (Linux):     python3 tools/kuhmuhnity/gen_gruppen.py <kapitel>

Schreibt direkt nach db/import/item_randomopt_group.yml im Repo.

Benoetigt nur Python 3, keine Zusatzpakete.

affixe.csv (Trennzeichen ;, laesst sich in Excel bearbeiten):
  Id       rAthena-/Client-ID – nicht aendern
  Option   Konstante aus item_randomopt_db.yml – nicht aendern
  Kapitel  ab welchem Kapitel das Affix wuerfelt (0 = nie)
  Min/Max  Wertebereich fuer die unterste Stufe (Monster Lv 1-20)
  Chance   1-10000; 3700 = Standard. Kleiner = seltener
  Effekt   nur zur Info

Hoehere Stufen werden automatisch skaliert (siehe STUFEN unten).
"""
import csv, os, sys

KAPITEL = int(sys.argv[1]) if len(sys.argv) > 1 else 1
HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "affixe.csv")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "db", "import", "item_randomopt_group.yml"))

# Gruppe: (Multiplikator auf Min/Max, Art)
STUFEN = [
    ("AFFIX_T1",   1.0, "normal"),   # Monster Lv 1-20
    ("AFFIX_T2",   1.5, "normal"),   # Monster Lv 21-40
    ("AFFIX_T3",   2.0, "normal"),   # Monster Lv 41-60
    ("AFFIX_T4",   2.5, "normal"),   # Monster Lv 61+
    ("AFFIX_BOSS", 2.5, "boss"),     # immer 4 Affixe
    ("AFFIX_MVP",  3.0, "mvp"),      # immer 5 Affixe
]
NORMAL_VERSUCHE = 3   # bis zu 3 Affixe; bei Chance 3700 -> 75 % mindestens eins

rows = []
with open(CSV, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        k = int(r["Kapitel"])
        if 1 <= k <= KAPITEL:
            rows.append(r)

if not rows:
    sys.exit("Keine Affixe fuer dieses Kapitel aktiv.")

def scaled(r, mult):
    lo, hi = int(r["Min"]), int(r["Max"])
    if lo == hi == 1 and "getrandomoptinfo" not in r["Effekt"]:
        return 1, 1                      # reiner Schalter (z. B. Element), nicht skalieren
    lo2 = max(1, round(lo * mult))
    hi2 = max(lo2, round(hi * mult))
    return lo2, hi2

def entry(r, mult, chance, indent):
    lo, hi = scaled(r, mult)
    p = " " * indent
    return (f"{p}- Option: {r['Option']}\n"
            f"{p}  MinValue: {lo}\n"
            f"{p}  MaxValue: {hi}\n"
            f"{p}  Chance: {chance}\n")

out = []
out.append("# KuhMuhWeide – Affix-Pools (AUTOMATISCH ERZEUGT aus affixe.csv)\n")
out.append(f"# Aktives Kapitel: {KAPITEL}  |  aktive Affixe: {len(rows)}\n")
out.append("# Nicht von Hand bearbeiten – affixe.csv aendern und gen_gruppen.py erneut ausfuehren.\n\n")
out.append("Header:\n  Type: RANDOM_OPTION_GROUP\n  Version: 1\n\nBody:\n")

for gid, (name, mult, art) in enumerate(STUFEN, start=1):
    out.append(f"  - Id: {gid}\n    Group: {name}\n")
    if art == "normal":
        out.append(f"    MaxRandom: {NORMAL_VERSUCHE}\n    Random:\n")
        for r in rows:
            out.append(entry(r, mult, int(r["Chance"]), 6))
    else:
        n = 4 if art == "boss" else 5
        out.append("    Slots:\n")
        for s in range(1, n + 1):
            out.append(f"      - Slot: {s}\n        Options:\n")
            for r in rows:
                out.append(entry(r, mult, 10000, 10))

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("".join(out))

print(f"Kapitel {KAPITEL}: {len(rows)} aktive Affixe -> {OUT}")
