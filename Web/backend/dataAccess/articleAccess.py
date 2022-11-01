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
            #print(alternative_articles.values())
            return alternative_articles
        except:
            return None