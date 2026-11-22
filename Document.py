class Document:
    def __init__(self, title, author, date, url, text, doc_type):
        self.title = title
        self.author = author
        self.date = date
        self.url = url
        self.text = text
        self.type = doc_type

    def display(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Date:", self.date)
        print("URL:", self.url)
        print("Type:", self.getType())
        print("Text:", self.text)

    def getType(self):
        return self.type

    def __str__(self):
        return self.title


class HackerNewsDocument(Document):
    def __init__(self, title, author, date, url, text, comments):
        super().__init__(title, author, date, url, text, "hackernews")
        self.comments = comments

    def getComments(self):
        return self.comments

    def setComments(self, comments):
        self.comments = comments

    def getType(self):
        return "Hacker News"

    def __str__(self):
        return f"{self.title} (Hacker News, {self.comments} comments)"


class ArxivDocument(Document):
    def __init__(self, title, author, date, url, text, coauthors):
        super().__init__(title, author, date, url, text, "arxiv")
        self.coauthors = coauthors

    def getCoauthors(self):
        return self.coauthors

    def setCoauthors(self, coauthors):
        self.coauthors = coauthors

    def getType(self):
        return "Arxiv"

    def __str__(self):
        return f"{self.title} (Arxiv)"
