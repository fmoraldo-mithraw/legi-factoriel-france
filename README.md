# legi-factoriel-france

Audit outillé du droit français consolidé (base **LEGI** de la DILA, données ouvertes),
traité comme une grosse base de code legacy : références mortes, doublons, dispositions
sans objet, dépendances.

**Ce dépôt ne légifère pas.** Il produit des *signalements* que des juristes doivent vérifier.
Supprimer ou réécrire un texte est un choix politique et juridique qui revient aux humains.
Un article qui paraît mort peut être vivant en jurisprudence.

## Utilisation
```
curl -O https://echanges.dila.gouv.fr/OPENDATA/LEGI/Freemium_legi_global_<date>.tar.gz
python3 -I scripts/ingest.py Freemium_legi_global_<date>.tar.gz legi.sqlite   # flux, sans extraction
python3 -I scripts/audit_refs_mortes.py legi.sqlite rapports/
```
La base SQLite (plusieurs Go) n'est pas versionnée ; seuls les scripts et les rapports le sont.

Voir `ROADMAP.md` pour l'avancement et `notes/` pour les notes thématiques.
