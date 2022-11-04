from backend.coremodels.article_has_supplier import ArticleHasSupplier
from backend.coremodels.supplier import Supplier
from ..coremodels.article import Article
from ..__init__ import dataAccessInjector as di


@di.register(name="ArticleAccess")
class ArticleAccess():
    '''Article access.'''
    def get_article_by_lio_id(self, lio_id: str) -> Article:
        '''Retrieve article by lio-id.'''
        try:
            article = Article.objects.get(lio_id=lio_id)
            return article
        except Exception:
            return None

    def get_alternative_articles(self, lio_id: str) -> Article:
        '''Retrieve alternative articles.'''
        try:
            article = Article.objects.get(lio_id=lio_id)
            alternative_articles = article.alternative_articles.all()
            return alternative_articles
        except Exception:
            return None

    def get_supplier(self, article: Article) -> Supplier:
        try:
            supplier = ArticleHasSupplier.objects.get(
                        article=article).article_supplier
            return supplier
        except Exception:
            return None

    def get_supplier_article_nr(self, article: Article) -> Supplier:
        try:
            supplier_article_nr = ArticleHasSupplier.objects.get(
                                    article=article).supplier_article_nr
            return supplier_article_nr
        except Exception:
            return None
