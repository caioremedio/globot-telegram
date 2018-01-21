import json
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

    @staticmethod
    def get_articles():
        response = get(
            'http://falkor-cda.bastian.globo.com/feeds/b904b430-123a-4f93-8cf4-5365adf97892/posts/ssi',
            headers=GloboHelper.DEFAULT_HEADERS
        )

        json_response = response.json()

        if json_response is None or not 'items' in json_response:
            return None

        return Article.initializeFromList(json_response['items'])

    @staticmethod
    def get_popular_comments_from_article(article):

        response = get(
            '/'.join((
                "https://comentarios.globo.com/comentarios",
                article.uri,
                article.id_for_request,
                article.url_for_request,
                'shorturl/titlef/populares/1.json',
            )),
            headers=GloboHelper.DEFAULT_HEADERS
        )

        # Remove function name and last parenteses
        json_str = response.text.replace('__callback_listacomentarios(','')[:-1]
        json_response = json.loads(json_str)

        if json_response is None or not 'itens' in json_response:
            return None

        return Comment.initializeFromList(json_response['itens'])

    @staticmethod
    def get_html_content_for_article(article):
        response = get(
            article.url,
            headers=GloboHelper.DEFAULT_HEADERS
        )
        return response.text