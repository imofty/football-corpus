import json
import pandas as pd

from Author import Author
from DocumentFactory import DocumentFactory


class Corpus:
    # Singleton: only one Corpus instance is created.
    _instance = None

    def __new__(cls, name="Football"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="Football"):
        if getattr(self, "_initialized", False):
            return
        self.name = name
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self._initialized = True

    def clear(self):
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add_document(self, doc_id, document):
        self.id2doc[str(doc_id)] = document

        author_names = [document.author or "Unknown"]
        author_names.extend(getattr(document, "coauthors", []))
        for author_name in set(author_names):
            if author_name not in self.authors:
                self.authors[author_name] = Author(author_name)
            self.authors[author_name].add(str(doc_id), document)

        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

    def display_documents(self, number=10):
        documents = sorted(
            self.id2doc.values(),
            key=lambda doc: (doc.date or "", doc.title or ""),
            reverse=True
        )
        for document in documents[:number]:
            print(f"[{document.getType()}] {document.title} — {document.author} — {document.date}")

    def author_statistics(self, author_name):
        author = self.authors.get(author_name)
        if author is None:
            return None
        return author.ndoc, author.average_length()

    def corpus_size(self):
        return self.ndoc

    def word_and_sentence_counts(self):
        results = {}
        for doc_id, document in self.id2doc.items():
            words = len(document.text.split())
            sentences = len(document.text.split("."))
            results[doc_id] = (words, sentences)
        return results

    def remove_short_documents(self, minimum_length=20):
        to_remove = [
            doc_id for doc_id, doc in self.id2doc.items()
            if len(doc.text) < minimum_length
        ]
        for doc_id in to_remove:
            document = self.id2doc.pop(doc_id)
            author_names = [document.author or "Unknown"]
            author_names.extend(getattr(document, "coauthors", []))
            for author_name in set(author_names):
                author = self.authors.get(author_name)
                if author:
                    author.production.pop(doc_id, None)
                    author.ndoc = len(author.production)
                    if author.ndoc == 0:
                        self.authors.pop(author.name)
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)
        return len(to_remove)

    def joined_text(self):
        return " ".join(doc.text for doc in self.id2doc.values())

    def save(self, filename):
        rows = []
        for doc_id, doc in self.id2doc.items():
            rows.append({
                "id": doc_id,
                "text": doc.text,
                "origin": doc.type,
                "title": doc.title,
                "author": doc.author,
                "date": doc.date,
                "url": doc.url,
                "comments": getattr(doc, "comments", 0),
                "coauthors": json.dumps(getattr(doc, "coauthors", []), ensure_ascii=False)
            })

        columns = [
            "id", "text", "origin", "title", "author",
            "date", "url", "comments", "coauthors"
        ]
        pd.DataFrame(rows, columns=columns).to_csv(
            filename, sep="\t", index=False, encoding="utf-8"
        )

    def load(self, filename):
        dataframe = pd.read_csv(filename, sep="\t").fillna("")
        self.clear()

        for _, row in dataframe.iterrows():
            data = row.to_dict()
            try:
                data["coauthors"] = json.loads(data.get("coauthors") or "[]")
            except (TypeError, json.JSONDecodeError):
                data["coauthors"] = []

            document = DocumentFactory.create_document(data)
            self.add_document(data["id"], document)

    def __repr__(self):
        return (
            f"Corpus : {self.name}\n"
            f"Documents : {self.ndoc}\n"
            f"Auteurs : {self.naut}"
        )
