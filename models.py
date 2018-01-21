from requests import get
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class Article:
    """docstring for Article"""
    def __init__(self, id, title, url):
        self.id = id
        self.title = title
        self.url = url

    @property
    def uri(self):
        url_path = urlparse(self.url).path

        if not url_path:
            return None

        url_paths = url_path.split('/')[1:]
        final_uri = '@@jornalismo@@g1'

        for path in url_paths:
            if path == 'noticia':
                break
            final_uri += f"@@{path}"

        return final_uri

    @property
    def id_for_request(self):
        from globo_helper import GloboHelper
        html_text = GloboHelper.get_html_content_for_article(self)

        soup = BeautifulSoup(html_text, 'html.parser')
        attributes = soup.find(class_='multicontent').attrs

        if attributes is None or 'data-content-id' not in attributes:
            return None

        return f"multi-content@@{attributes['data-content-id']}"

    @property
    def url_for_request(self):
        return self.url.replace("/", '@@')

    @classmethod
    def initializeFromList(cls, article_list):
        filtered = list(filter(lambda article: article['content'], article_list))
        return list(map(lambda article: Article(article['id'],
                                                article['content']['title'],
                                                article['content']['url']),
                                        filtered))

class Comment:
    def __init__(self, text, upvotes_value, downvotes_value, author_name, article):
        self.text = text
        self.upvotes_value = upvotes_value # Deprecated
        self.downvotes_value = downvotes_value # Deprecated
        self.author_name = author_name
        self.article = article

    @classmethod
    def initializeFromList(cls, comment_list, article):
        filtered = list(filter(lambda comment: comment['texto'], comment_list))
        return list(map(lambda comment: Comment(comment['texto'],
                                                comment['VotosThumbsUp'],
                                                comment['VotosThumbsDown'],
                                                comment['Usuario']['nomeFormatado'],
                                                article),
                                        filtered))