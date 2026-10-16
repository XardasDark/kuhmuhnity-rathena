# KuhMuhnity – rAthena (Pre-Renewal)

Eigener Fork von [rAthena](https://github.com/rathena/rathena) für den KuhMuhWeide-Server
im Stil von Ragnarok Zero.

## Branches

| Branch   | Zweck |
|----------|-------|
| `master` | unverändertes rAthena – nur über **Sync fork** auf GitHub aktualisieren |
| `dev`    | Entwicklung und Tests – hier landen alle neuen Änderungen zuerst |
| `prod`   | Live-Server – nur getestete Stände aus `dev` |

Ablauf:

1. Änderung auf `dev` committen.
2. DEV-Server neu starten (`AUTO_UPDATE=1` zieht den neuen Stand) und testen.
3. Wenn alles passt: `dev` in `prod` mergen (Pull Request `dev` → `prod` auf GitHub).
4. PROD-Server neu starten.

rAthena-Updates: `master` per **Sync fork** aktualisieren, dann `master` in `dev` mergen,
testen, danach wie oben nach `prod`.

## Was hier angepasst ist

| Datei | Inhalt |
|-------|--------|
| `conf/import/battle_conf.txt` | Raten (2x EXP/Drops, Karten/MVP 1x), Party-Bonus, Monster-Anzeige |
| `conf/import/*_conf.txt` | binden die vom Panel erzeugten `ptero_*.txt` ein – Panel-Variablen stehen dort |
| `db/import/job_stats.yml` | Level-Cap Kapitel 1 (Base 50) |
| `npc/scripts_custom.conf` | Kapitel 1: Jobwechsel-NPCs außer erster Klasse entfernt (`delnpc`) |
| `db/import/item_randomopt_db.yml` | alle 249 Affix-Definitionen |
| `db/import/item_randomopt_group.yml` | Affix-Pools (erzeugt aus `tools/kuhmuhnity/affixe.csv`) |
| `db/import/mob_db.yml` | Affix-Gruppe für jeden Ausrüstungsdrop |

Die `conf/import/ptero_*.txt` enthalten Zugangsdaten, werden bei jedem Start vom Panel
neu geschrieben und sind per `.gitignore` ausgeschlossen.

## Werkzeuge (`tools/kuhmuhnity/`)

- `affixe.csv` – alle Affixe mit Kapitel, Wertebereich und Chance (Excel, Trennzeichen `;`)
- `gen_gruppen.py <kapitel>` – erzeugt `db/import/item_randomopt_group.yml` (nur Python 3)
- `gen_mobdrops.py . db/import` – erzeugt `db/import/mob_db.yml` neu (benötigt PyYAML)
