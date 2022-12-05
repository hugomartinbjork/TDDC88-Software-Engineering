
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
        '''Retrieve supplier for an article.'''
        try:
            supplier = ArticleHasSupplier.objects.get(
                        article=article).article_supplier
            return supplier
        except Exception:
            return None

    def get_supplier_article_nr(self, article: Article) -> Supplier:
        '''Returns supplier_article_nr for an article.'''
        try:
            supplier_article_nr = ArticleHasSupplier.objects.get(
                                    article=article).supplier_article_nr
            return supplier_article_nr
        except Exception:
            return None

    def get_article_by_name(self, name: str) -> Article:
        '''Returns article based on name'''
        try:
            article = Article.objects.get(name=name)
            return article
        except:
            return None

    def get_articles_by_search_name(self, search_string: str) -> Article:
        try:
            articles = Article.objects.filter(name__contains=search_string)
            return articles
        except:
            return None

    def get_articles_by_search_lio(self, search_string: str) -> Article:
        try:
            articles = Article.objects.filter(lio_id__contains=search_string)
            return articles
        except:
            return None
    
    def get_all_articles(self):
        try:
            all_articles = Article.objects.all()
            return all_articles
        except Exception:
            return None
