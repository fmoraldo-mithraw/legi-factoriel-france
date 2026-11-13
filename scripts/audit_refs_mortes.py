#!/usr/bin/env python3
"""Étape 1 : articles en vigueur qui citent un article abrogé (sans version en vigueur du même numéro).

Usage: python3 -I scripts/audit_refs_mortes.py legi.sqlite rapports/
"""
import csv, sqlite3, sys, os, datetime, re

def norm(x):
    return re.sub(r'[\s.\u00a0*]', '', x or '')

Q = '''
SELECT a.id, a.texte_titre, a.num, c.id, c.texte_titre, c.num, c.etat, c.date_fin, l.libelle, a.contenu
FROM articles a
JOIN liens l ON l.source = a.id AND l.typelien = 'CITATION' AND l.sens = 'source'
JOIN articles c ON c.id = l.cible_id
WHERE a.etat = 'VIGUEUR' AND a.chemin LIKE 'legi/global/code_et_TNC_en_vigueur/%'
  AND c.etat IN ('ABROGE', 'ANNULE', 'PERIME', 'DISJOINT')
  AND NOT EXISTS (SELECT 1 FROM articles v WHERE v.texte_cid = c.texte_cid AND v.num = c.num
                  AND v.etat IN ('VIGUEUR', 'VIGUEUR_DIFF'))
ORDER BY a.texte_titre, a.num
'''

def main(db, outdir):
    con = sqlite3.connect(db)
    brut = con.execute(Q).fetchall()
    # Filtre : le numéro cité doit figurer dans le texte actuel de l'article
    # (LEGI conserve des liens hérités de versions antérieures).
    rows = []
    for r in brut:
        if r[5] and norm(r[5]) in norm(r[9]):
            rows.append(r[:9])
    print(len(brut), 'liens candidats,', len(rows), 'confirmés dans le texte')
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f'refs_mortes_{datetime.date.today()}.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['article_id', 'texte', 'num', 'cible_id', 'texte_cible', 'num_cible', 'etat_cible', 'fin_cible', 'libelle_lien'])
        w.writerows(rows)
    par_texte = {}
    for r in rows:
        par_texte[r[1]] = par_texte.get(r[1], 0) + 1
    print(len(rows), 'références mortes ->', out)
    for t, n in sorted(par_texte.items(), key=lambda x: -x[1])[:30]:
        print(f'{n:6d}  {t}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
