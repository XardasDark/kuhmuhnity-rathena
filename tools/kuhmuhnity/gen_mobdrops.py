#!/usr/bin/env python3
"""Weist jedem Ausruestungsdrop (Pre-Renewal) die passende Affix-Gruppe zu.

Ausgabe: <ausgabeordner>/mob_db.yml
  normale Monster -> AFFIX_T1..T4 nach Level, Bosse -> AFFIX_BOSS, MVPs -> AFFIX_MVP

Benoetigt PyYAML (pip install pyyaml).
Aufruf im Repo:  python3 tools/kuhmuhnity/gen_mobdrops.py . db/import
"""
import sys, os, yaml

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def tier_for_level(lv):
    if lv <= 20: return "AFFIX_T1"
    if lv <= 40: return "AFFIX_T2"
    if lv <= 60: return "AFFIX_T3"
    return "AFFIX_T4"

# ---------------------------------------------------------------------------
def dump(path, header_type, version, body, comment):
    with open(path, "w", encoding="utf-8") as f:
        f.write(comment)
        f.write(yaml.safe_dump({"Header": {"Type": header_type, "Version": version}, "Body": body},
                               sort_keys=False, allow_unicode=True, width=200))

# 3) Ausruestung bestimmen (Waffen und Ruestungen inkl. Kopf, Umhang, Schuhe, Accessoires, Schilde)
equip = set()
for fn in ["db/pre-re/item_db_equip.yml"]:
    data = yaml.load(open(f"{SRC}/{fn}", encoding="utf-8"), Loader=yaml.CSafeLoader if hasattr(yaml, "CSafeLoader") else yaml.SafeLoader)
    for it in data.get("Body") or []:
        if it.get("Type") in ("Weapon", "Armor"):
            equip.add(it["AegisName"])

mobs = yaml.load(open(f"{SRC}/db/pre-re/mob_db.yml", encoding="utf-8"),
                 Loader=yaml.CSafeLoader if hasattr(yaml, "CSafeLoader") else yaml.SafeLoader)["Body"]

body, stats = [], {"mobs": 0, "drops": 0}
for m in mobs:
    is_mvp = bool((m.get("Modes") or {}).get("Mvp"))
    is_boss = m.get("Class") == "Boss"
    group = "AFFIX_MVP" if is_mvp else "AFFIX_BOSS" if is_boss else tier_for_level(int(m.get("Level", 1)))
    out = {"Id": m["Id"]}
    for key in ("Drops", "MvpDrops"):
        lst = []
        for idx, d in enumerate(m.get(key) or []):
            if d["Item"] in equip:
                e = {"Index": idx, "Item": d["Item"], "Rate": d["Rate"]}
                if d.get("StealProtected"):
                    e["StealProtected"] = True
                e["RandomOptionGroup"] = group
                lst.append(e)
        if lst:
            out[key] = lst
            stats["drops"] += len(lst)
    if len(out) > 1:
        body.append(out)
        stats["mobs"] += 1

dump(f"{OUT}/mob_db.yml", "MOB_DB", 5, body,
     "# KuhMuhWeide – Affixe auf Ausruestungsdrops (automatisch erzeugt)\n"
     "# Ueberschreibt nur die Ausruestungs-Eintraege (per Index) und haengt\n"
     "# die passende RandomOptionGroup an. Alle anderen Drops bleiben unveraendert.\n\n")

print(f"{len(equip)} Ausruestungsitems, {stats['mobs']} Monster, {stats['drops']} Drops mit Affixen")
