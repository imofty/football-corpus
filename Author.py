class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    def add(self, doc_id, document):
        self.production[doc_id] = document
        self.ndoc = len(self.production)

    def average_length(self):
        if self.ndoc == 0:
            return 0
        return sum(len(doc.text) for doc in self.production.values()) / self.ndoc

    def __str__(self):
        return f"{self.name}: {self.ndoc} document(s)"
