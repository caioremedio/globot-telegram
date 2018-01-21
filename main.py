#!/usr/bin/python3

import os
import models
import decoders
from globo_helper import GloboHelper

def main():
    articles = GloboHelper.get_articles()
    print(GloboHelper.get_popular_comments_from_article(articles[0])[0].author_name)
    print(articles[0].id_for_request)

if __name__ == '__main__':
    main()