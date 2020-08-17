# loi-française-code-source
**Code source pour le dépôt loi-française**

Pour reproduire le dépôt loi-française, il vous faut:

```
# avec legi.py
python -m legi.download ./tarballs # télécharger les données
python -m legi.tar2sqlite legi.sqlite ./tarballs --pragma="journal_mode=WAL" --skip-checks --skip-links # ingérer les données (ceci m'a pris environ une semaine)
   # ceci prenant du temps j'ai ajouté une barre de progression: https://github.com/Legilibre/legi.py/pull/83
# avec archeo-lex
./archeo-lex --textes="code" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
./archeo-lex --textes="loi" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
./archeo-lex --textes="loi_organique" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
./archeo-lex --textes="ordonnance" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
./archeo-lex --textes="loi_constit" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
./archeo-lex --textes="constitution" --bddlegi=../legi.py/legi.sqlite --dates-git-pre-1970
	# pour surveiller la progression, je fais une requête SQL sur la base:
	SELECT count(*) from textes_versions where nature="<NATURE>"
	# que je compare avec
	ls textes/<type>/ | wc -l
# et pour finir
python combiner-depots.py <chemin-vers-le-repertoire-des-textes-d-archeo-lex>
cp README-repo.md combined/README.md; cd combined;git add README.md; git commit -m "ajoute README"
```