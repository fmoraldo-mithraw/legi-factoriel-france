# Feuille de route (travail en fond, une étape par session)

Chaque session planifiée reprend la première case non cochée, la fait, coche, commit, push.

- [x] 0. Squelette, ingestion LEGI en flux vers SQLite (`scripts/ingest.py`)
- [x] 1. Audit des références mortes : articles EN VIGUEUR dont les liens CITATION pointent
      vers un article/texte ABROGÉ (`scripts/audit_refs_mortes.py`) → `rapports/refs_mortes_*.csv`
      *Fait le 13/11/2026 : 10 323 signalements, voir `rapports/refs_mortes_2026-11-13.md`.
      Piste : rapprocher chaque cible abrogée de son successeur (liens TRANSFERE/CODIFICATION) pour proposer la correction.*
- [ ] 2. Références textuelles non liées : regex « article X de la loi n° … » dans les contenus
      en vigueur, résolution vers LEGI, détection des cibles abrogées
- [ ] 3. Doublons : articles en vigueur quasi identiques dans des codes différents (shingles/MinHash)
- [ ] 4. Dispositions sans objet : renvois à des décrets d'application jamais pris
      (« un décret en Conseil d'État fixe… » sans texte d'application lié), dates/délais échus
- [ ] 5. Contrôle de constitutionnalité : croiser la base CONSTIT (décisions DC/QPC) avec LEGI
      pour trouver les dispositions déclarées non conformes (abrogation différée) qui
      apparaîtraient encore en vigueur après la date d'effet
- [ ] 6. Pilote de réécriture à droit constant sur un code (proposition, à relire par juristes)
- [ ] 7. Mise à jour périodique avec les dumps incrémentaux LEGI_*.tar.gz
