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
