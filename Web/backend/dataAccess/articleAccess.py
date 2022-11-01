from backend.coremodels.article_has_supplier import ArticleHasSupplier
from backend.coremodels.supplier import Supplier
from ..coremodels.article import Article
from ..__init__ import dataAccessInjector as di

@di.register(name = "articleAccess")
class articleAccess():
    def getArticleByLioId(self, lioId: str) -> Article:
        try:
            article = Article.objects.get(lioId=lioId)  
            return article
        except:
            return None

    def getAlternativeArticles(self, lioId: str) -> Article:
        try:
            article = Article.objects.get(lioId=lioId)
            alternative_articles = article.alternative_articles.all()
            return alternative_articles
        except:
            return None

    def getSupplier(self, article: Article) -> Supplier:
        try:
            supplier = ArticleHasSupplier.objects.get(article=article).article_supplier
            return supplier
        except:
            return None

    def getSupplierArticleNr(self, article: Article) -> Supplier:
        try:
            supplier_article_nr = ArticleHasSupplier.objects.get(article=article).supplier_article_nr
            return supplier_article_nr
        except:
            return None