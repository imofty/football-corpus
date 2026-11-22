from pathlib import Path

from Corpus import Corpus
from DataCollector import DataCollector
from DocumentFactory import DocumentFactory

DATA_FILE = Path(__file__).parent / "data" / "football_corpus.tsv"


def recuperer_et_sauvegarder(corpus):
    print("\nRécupération des documents sur le football...")
    collecteur = DataCollector("football")
    documents, erreurs = collecteur.fetch_all()

    corpus.clear()
    for numero, donnees in enumerate(documents, start=1):
        document = DocumentFactory.create_document(donnees)
        corpus.add_document(numero, document)

    corpus.remove_short_documents(20)
    corpus.save(DATA_FILE)

    print(f"{corpus.ndoc} document(s) sauvegardé(s) dans : {DATA_FILE}")
    for erreur in erreurs:
        print("Attention :", erreur)
    if not documents:
        print("Aucun document reçu. Vérifiez votre connexion Internet et réessayez.")


def afficher_statistiques_auteur(corpus):
    nom = input("Nom de l'auteur : ").strip()
    statistiques = corpus.author_statistics(nom)

    if statistiques is None:
        print("Auteur introuvable.")
    else:
        nombre, longueur_moyenne = statistiques
        print(f"Nombre de documents : {nombre}")
        print(f"Longueur moyenne des documents : {longueur_moyenne:.1f} caractères")


def main():
    corpus = Corpus("Football")

    if DATA_FILE.exists():
        try:
            corpus.load(DATA_FILE)
            print("Corpus chargé depuis le fichier local.")
        except Exception as erreur:
            print("Impossible de charger le fichier sauvegardé :", erreur)
            recuperer_et_sauvegarder(corpus)
    else:
        recuperer_et_sauvegarder(corpus)

    while True:
        print("\n========== CORPUS FOOTBALL ==========")
        print("1. Afficher les informations du corpus")
        print("2. Afficher les documents")
        print("3. Consulter les statistiques d'un auteur")
        print("4. Afficher le nombre de mots et de phrases")
        print("5. Récupérer de nouvelles données depuis les API")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            print(corpus)
        elif choix == "2":
            try:
                nombre = int(input("Combien de documents voulez-vous afficher ? "))
                corpus.display_documents(max(0, nombre))
            except ValueError:
                print("Veuillez saisir un nombre valide.")
        elif choix == "3":
            afficher_statistiques_auteur(corpus)
        elif choix == "4":
            for identifiant, comptes in corpus.word_and_sentence_counts().items():
                print(f"Document {identifiant} : {comptes[0]} mot(s), {comptes[1]} phrase(s)")
        elif choix == "5":
            recuperer_et_sauvegarder(corpus)
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()
