
# football corpus

un projet python qui collecte et organise des documents liés au football depuis hacker news et arxiv.

## installation

installer les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

## utilisation

lancer le programme :

```bash
python main.py
```

au premier lancement, le programme récupère les données depuis les api de hacker news et arxiv, puis les sauvegarde localement dans `data/football_corpus.tsv`.

lors des lancements suivants, les données sont chargées directement depuis ce fichier, sans interroger les api.

### Utiliser le menu

| Option | Résultat |
| --- | --- |
| `1` | Affiche le nom du corpus et le nombre de documents et d’auteurs. |
| `2` | Demande combien de documents afficher, puis indique leur source, leur titre, leur auteur et leur date. |
| `3` | Demande le nom d’un auteur, puis affiche son nombre de documents et leur longueur moyenne en caractères. |
| `4` | Affiche les nombres de mots et de phrases par document. |
| `5` | Lance une nouvelle collecte et sauvegarde les résultats dans le fichier TSV. |
| `0` | Quitte le programme. |

Pour consulter les statistiques d’un auteur, choisis `2`, saisis `3`, puis reprends un nom affiché dans la liste pour l’option `3`. Recopie le nom tel qu’il apparaît. Si le nom ne figure pas dans le corpus, le programme affiche « Auteur introuvable. ».

Si tu saisis `abc` à la place d’un nombre à l’option `2`, le programme affiche « Veuillez saisir un nombre valide. » et revient au menu.

## fonctionnalités

- collecte de documents depuis hacker news et arxiv
- gestion des documents et des auteurs
- sauvegarde et chargement du corpus
- statistiques sur les documents et les auteurs
- interface en ligne de commande
