#!/usr/bin/env python3
"""Ingestion en flux de l'archive LEGI (DILA) vers SQLite, sans extraire les millions de fichiers.

Usage: python3 -I scripts/ingest.py <archive.tar.gz> <sortie.sqlite>
Tables: articles, textes, liens.
"""
import sqlite3, sys, tarfile, re
import xml.etree.ElementTree as ET

def txt(el, path):
    x = el.find(path)
    return (x.text or '').strip() if x is not None and x.text else None

def main(archive, dbpath):
    db = sqlite3.connect(dbpath)
    db.executescript('''
    PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF;
    CREATE TABLE IF NOT EXISTS articles(id TEXT PRIMARY KEY, num TEXT, etat TEXT, date_debut TEXT, date_fin TEXT,
        texte_cid TEXT, texte_nature TEXT, texte_titre TEXT, contenu TEXT, nota TEXT, chemin TEXT);
    CREATE TABLE IF NOT EXISTS textes(id TEXT PRIMARY KEY, cid TEXT, nature TEXT, num TEXT, titre TEXT, titrefull TEXT,
        etat TEXT, date_debut TEXT, date_fin TEXT, date_texte TEXT, chemin TEXT);
    CREATE TABLE IF NOT EXISTS liens(source TEXT, cible_id TEXT, cible_cid TEXT, cible_num TEXT, nature TEXT,
        typelien TEXT, sens TEXT, libelle TEXT);
    ''')
    n = 0
    with tarfile.open(archive, 'r|gz') as tf:
        for m in tf:
            if not m.isfile() or not m.name.endswith('.xml'):
                continue
            kind = '/article/' in m.name and 'A' or ('/texte/version/' in m.name and 'T' or None)
            if not kind:
                continue
            try:
                root = ET.fromstring(tf.extractfile(m).read())
            except ET.ParseError:
                continue
            if kind == 'A':
                aid = txt(root, 'META/META_COMMUN/ID')
                ma = 'META/META_SPEC/META_ARTICLE/'
                t = root.find('CONTEXTE/TEXTE')
                tt = root.find('CONTEXTE/TEXTE/TITRE_TXT')
                bloc = root.find('BLOC_TEXTUEL/CONTENU')
                contenu = ''.join(bloc.itertext()).strip() if bloc is not None else None
                nota_el = root.find('NOTA/CONTENU')
                nota = ''.join(nota_el.itertext()).strip() if nota_el is not None else None
                db.execute('INSERT OR REPLACE INTO articles VALUES(?,?,?,?,?,?,?,?,?,?,?)', (
                    aid, txt(root, ma+'NUM'), txt(root, ma+'ETAT'), txt(root, ma+'DATE_DEBUT'), txt(root, ma+'DATE_FIN'),
                    t.get('cid') if t is not None else None, t.get('nature') if t is not None else None,
                    (tt.text or '').strip() if tt is not None else None, contenu, nota or None, m.name))
                src = aid
            else:
                src = txt(root, 'META/META_COMMUN/ID')
                mv = 'META/META_SPEC/META_TEXTE_VERSION/'
                mc = 'META/META_SPEC/META_TEXTE_CHRONICLE/'
                db.execute('INSERT OR REPLACE INTO textes VALUES(?,?,?,?,?,?,?,?,?,?,?)', (
                    src, txt(root, mc+'CID'), txt(root, 'META/META_COMMUN/NATURE'), txt(root, mc+'NUM'),
                    txt(root, mv+'TITRE'), txt(root, mv+'TITREFULL'), txt(root, mv+'ETAT'),
                    txt(root, mv+'DATE_DEBUT'), txt(root, mv+'DATE_FIN'), txt(root, mc+'DATE_TEXTE'), m.name))
            for l in root.iter('LIEN'):
                db.execute('INSERT INTO liens VALUES(?,?,?,?,?,?,?,?)', (src, l.get('id'), l.get('cidtexte'),
                    l.get('num'), l.get('naturetexte'), l.get('typelien'), l.get('sens'), (l.text or '').strip()))
            n += 1
            if n % 100000 == 0:
                db.commit(); print(n, m.name[:80], flush=True)
    db.executescript('''CREATE INDEX IF NOT EXISTS i_l_src ON liens(source); CREATE INDEX IF NOT EXISTS i_l_cib ON liens(cible_id);
        CREATE INDEX IF NOT EXISTS i_a_cid ON articles(texte_cid); CREATE INDEX IF NOT EXISTS i_t_cid ON textes(cid);''')
    db.commit(); print('fini', n)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
