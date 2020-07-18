from rake_nltk import Rake
from text_toolkit.url2text.url2text import Url2Text


class ExtractKeywords:

    def __init__(self, text):
        """
        Extract top n keywords from string that contains sentences.
        """
        self._text = text

        self.keywords_with_scores = []

    def extract_keywords(self):

        r = Rake()
        r.extract_keywords_from_text(self._text)
        self.keywords = r.get_ranked_phrases_with_scores()


if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Great_Depression"
    print(url)

    extractText = Url2Text(url)
    text = extractText.extract_text_from_html()

    extractKeywords = ExtractKeywords(text)
    extractKeywords.extract_keywords()
    keywords = extractKeywords.keywords

    print(text[:300])
    print(keywords)
