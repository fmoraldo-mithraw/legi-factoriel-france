# Étape 1 — Références mortes (dump LEGI du 8 novembre 2026)

**Méthode** : articles EN VIGUEUR (dans `code_et_TNC_en_vigueur`) ayant un lien `CITATION`
(sens `source`) vers un article ABROGÉ / ANNULÉ / PÉRIMÉ / DISJOINT, sans version en vigueur
du même numéro dans le même texte, **et** dont le numéro cité figure encore dans le texte
actuel de l'article.

**Résultat** : 11 773 liens candidats → **10 323 signalements** (`refs_mortes_2026-11-13.csv`).
Codes les plus touchés : rural et pêche maritime (167), environnement (150), santé publique (87),
sécurité sociale (79), domaine de l'État (75), CGCT (71), travail (60), procédure pénale (56).

**Exemples vérifiés à la main** (texte actuel de l'article) :
- C. commerce **A123-66** renvoie à « l'article R. 123-153 », abrogé le 1er janvier 2023.
- C. santé publique **R5132-3-1** renvoie à « l'article L. 5121-3 », abrogé le 25 décembre 2014.
- C. monétaire et financier **R549-2** : « délai mentionné à l'article L. 549-4 », abrogé le 1er janvier 2022.
- C. forestier **D231-3** renvoie à l'art. R. 5212-17 du CGCT, abrogé le 1er février 2012.

**Limites / faux positifs connus**
- Renvois volontairement historiques (« dans sa rédaction antérieure à… », dispositions transitoires).
- Abrogation suivie d'une recodification ailleurs : la référence est obsolète, mais le contenu existe sous un autre numéro (correction de pure forme).
- Le filtre « numéro présent dans le texte » est faible pour les numéros courts (« 1 », « 2 ») des textes non codifiés.
- Le code du Conseil d'État / la jurisprudence peuvent donner un sens à un renvoi apparemment mort.

**Anomalie annexe** : 226 articles marqués `VIGUEUR` se trouvent dans des textes classés « non en vigueur » par la DILA.
