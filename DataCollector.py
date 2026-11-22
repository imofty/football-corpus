import json
import re
from html import unescape
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xmltodict


class DataCollector:
    def __init__(self, theme="football"):
        self.theme = theme

    def _read_url(self, url):
        request = Request(url, headers={"User-Agent": "FootballCorpusStudentProject/1.0"})
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8")

    def fetch_hackernews(self):
        parameters = urlencode({
            "query": self.theme,
            "tags": "story",
            "hitsPerPage": 50
        })
        url = "https://hn.algolia.com/api/v1/search?" + parameters
        result = json.loads(self._read_url(url))
        documents = []

        for hit in result.get("hits", []):
            title = hit.get("title") or hit.get("story_title") or "Untitled"
            text = hit.get("story_text") or title
            text = unescape(re.sub(r"</?p[^>]*>", " ", text))
            text = " ".join(text.split())

            object_id = hit.get("objectID", "")
            source_url = hit.get("url") or hit.get("story_url")
            if not source_url and object_id:
                source_url = f"https://news.ycombinator.com/item?id={object_id}"

            documents.append({
                "title": title,
                "author": hit.get("author") or "Unknown",
                "date": hit.get("created_at") or "",
                "url": source_url or "",
                "text": text,
                "origin": "hackernews",
                "comments": hit.get("num_comments") or 0,
                "coauthors": []
            })

        return documents

    def fetch_arxiv(self):
        parameters = urlencode({
            "search_query": f"all:{self.theme}",
            "start": 0,
            "max_results": 50
        })
        url = "https://export.arxiv.org/api/query?" + parameters
        result = xmltodict.parse(self._read_url(url))
        entries = result.get("feed", {}).get("entry", [])

        # xmltodict returns a dictionary instead of a list for one result.
        if isinstance(entries, dict):
            entries = [entries]

        documents = []
        for entry in entries:
            title = " ".join((entry.get("title") or "").split())
            text = " ".join((entry.get("summary") or "").split())

            raw_authors = entry.get("author", [])
            if isinstance(raw_authors, dict):
                raw_authors = [raw_authors]

            names = []
            for author in raw_authors:
                if isinstance(author, dict) and author.get("name"):
                    names.append(author["name"])

            main_author = names[0] if names else "Unknown"
            coauthors = names[1:]

            link = entry.get("id", "")
            if isinstance(link, dict):
                link = link.get("#text", "")

            documents.append({
                "title": title or "Untitled",
                "author": main_author,
                "date": entry.get("published") or "",
                "url": link,
                "text": text or title,
                "origin": "arxiv",
                "comments": 0,
                "coauthors": coauthors
            })

        return documents

    def fetch_all(self):
        documents = []
        errors = []

        for source_name, fetch_method in [
            ("Hacker News", self.fetch_hackernews),
            ("Arxiv", self.fetch_arxiv)
        ]:
            try:
                documents.extend(fetch_method())
            except Exception as error:
                errors.append(f"{source_name}: {error}")

        return documents, errors
