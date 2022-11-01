from backend.coremodels.article import Article
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from ..dataAccess.articleAccess import articleAccess


@si.register(name='articleManagementService')
class articleManagementService():

    @di.inject
    def __init__(self, _deps, *args):
        self._articleOperations: articleAccess = _deps["articleAccess"]()

    def getArticleByLioId(self, lioId: str) -> Article:
        return self._articleOperations.getArticleByLioId(lioId)

    def getAlternativeArticles(self, lioId: str) -> Article:
        return self._articleOperations.getAlternativeArticles(lioId)

    def search_article_by_name(self, search_query: str) -> Article:
        return self._articleOperations.search_article_by_name(search_query)
