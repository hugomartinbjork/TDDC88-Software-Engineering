from backend.coremodels.article import Article
from backend.__init__ import serviceInjector as si 
from ..__init__ import dataAccessInjector as di
from ..dataAccess.articleAccess import articleAccess

@si.register(name = 'articleManagementService')
class articleManagementService():

    @di.inject
    def __init__(self, _deps):
        self._articleOperations : articleAccess = _deps["articleAccess"]()
    
    def getArticleByLioId(self, lioId: str) -> Article:
        return self._articleOperations.getArticleByLioId(lioId)
            