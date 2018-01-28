import json
import random
from sys import exit
from requests import get
from models import Article, Comment

class GloboHelper:

    DEFAULT_HEADERS = {
        'Accept': '*/*',
        'Accept-Language': 'pt-br',
        'Connection': 'keep-alive',
        'Cookie': 'hsid=2018-01-15T23:07:21-02:00; glb_uid="XRLsZji9UfcMJHlyOD2wfVEME8NlXALkx3uwD57YWT8="',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'G1NativeApp/5.4 Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Mobile/15C153 G1MobApp_iOS/5.4/2',
        'glbuid': 'XRLsZji9UfcMJHlyOD2wfVEME8NlXALkx3uwD57YWT8=',
    }

    @classmethod
    def get_articles(cls, request_type_id):
        response = get(
            f"http://falkor-cda.bastian.globo.com/feeds/{request_type_id}/posts/ssi",
            headers=cls.DEFAULT_HEADERS
        )

        json_response = response.json()

        if json_response is None or not 'items' in json_response:
            return None

        return Article.initializeFromList(json_response['items'])

    @classmethod
    def get_random_article(cls):
        articles = cls.get_articles()
        return random.choice(articles) if articles is not None else None

    @classmethod
    def get_random_comment_for_request_type(cls, request_type_id):
        articles = cls.get_articles(request_type_id)
        while True:
            article = random.choice(articles)
            comments = cls.get_popular_comments_from_article(article)
            if comments is not None and comments:
                return random.choice(comments)

    @classmethod
    def get_popular_comments_from_article(cls, article):

        if article is None or article.id_for_request is None:
            return None

        response = get(
            '/'.join((
                "https://comentarios.globo.com/comentarios",
                article.uri,
                article.id_for_request,
                article.url_for_request,
                'shorturl/titlef/populares/1.json',
            )),
            headers=cls.DEFAULT_HEADERS
        )

        # Remove function name and last parenteses
        json_str = response.text.replace('__callback_listacomentarios(','')[:-1]
        json_response = json.loads(json_str)

        if json_response is None or not 'itens' in json_response:
            return None

        return Comment.initializeFromList(json_response['itens'], article)

    @classmethod
    def get_html_content_for_article(cls, article):
        response = get(
            article.url,
            headers=cls.DEFAULT_HEADERS
        )
        return response.text

class RequestCityType:
    TYPE_HOME_ID = 'b904b430-123a-4f93-8cf4-5365adf97892'
    TYPE_SP_ID = '6dc3ec71-7aa8-4d92-8728-6d0a29d41671'
    TYPE_RJ_ID = ''