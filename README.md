
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

pour récupérer de nouvelles données, sélectionner l'option `5` dans le menu principal.

## fonctionnalités

- collecte de documents depuis hacker news et arxiv
- gestion des documents et des auteurs
- sauvegarde et chargement du corpus
- statistiques sur les documents et les auteurs
- interface en ligne de commande
