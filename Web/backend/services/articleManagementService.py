from backend.coremodels.supplier import Supplier
from backend.coremodels.article import Article
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from ..dataAccess.articleAccess import ArticleAccess


@si.register(name='ArticleManagementService')
class ArticleManagementService():
    '''Article management service.'''

    @di.inject
    def __init__(self, _deps, *args):
        self.article_operations: ArticleAccess = _deps["ArticleAccess"]()

    def get_articles(self):
        return self.article_operations.get_all_articles()

    def get_article_by_lio_id(self, lio_id: str) -> Article:
        '''Returns article using lio-id.'''
        return self.article_operations.get_article_by_lio_id(lio_id)

    def get_alternative_articles(self, lio_id: str) -> Article:
        '''Returns "similar" articles.'''
        return self.article_operations.get_alternative_articles(lio_id)

    def get_supplier(self, article: Article) -> Supplier:
        '''Return supplicer of specific article.'''
        return self.article_operations.get_supplier(article)

    def get_supplier_article_nr(self, article: Article) -> str:
        '''Returns supplier article nr.'''
        return self.article_operations.get_supplier_article_nr(article)

    def get_article_by_name(self, name: str) -> Article:
        '''Returns article using the name of the article'''
        return self.article_operations.get_article_by_name(name)

    def get_articles_by_search_name(self, search_string: str) -> Article:
        '''Returns articles using the name of the article even if name is not complete'''
        return self.article_operations.get_articles_by_search_name(search_string)

    def get_articles_by_search_lio(self, search_string: str) -> Article:
        '''Returns article using the lio of the article even if lio is not complete'''
        return self.article_operations.get_articles_by_search_lio(search_string)
