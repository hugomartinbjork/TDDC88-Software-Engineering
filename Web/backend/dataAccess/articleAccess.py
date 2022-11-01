from ..coremodels.article import Article
from ..__init__ import dataAccessInjector as di


@di.register(name="articleAccess")
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
            # print(alternative_articles.values())
            return alternative_articles
        except:
            return None

    def search_article_by_name(self, search_query: str) -> Article:
        """
        returns a queryset of articles which matches the string search_query.
        if no articles are found, None is returned.
        """
        try:
            articles = Article.objects.filter(
                name__contains=search_query).values()
            return articles
        except:
            return None
