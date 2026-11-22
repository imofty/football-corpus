from Document import HackerNewsDocument, ArxivDocument


class DocumentFactory:
    @staticmethod
    def create_document(data):
        origin = data.get("origin", "").lower()

        if origin == "hackernews":
            return HackerNewsDocument(
                data.get("title", ""),
                data.get("author", "Unknown"),
                data.get("date", ""),
                data.get("url", ""),
                data.get("text", ""),
                int(data.get("comments", 0) or 0)
            )

        if origin == "arxiv":
            return ArxivDocument(
                data.get("title", ""),
                data.get("author", "Unknown"),
                data.get("date", ""),
                data.get("url", ""),
                data.get("text", ""),
                data.get("coauthors", [])
            )

        raise ValueError(f"Unknown document origin: {origin}")
